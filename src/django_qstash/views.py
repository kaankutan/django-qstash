import json
import logging

from django.conf import settings
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from qstash import Receiver

from . import utils

DJANGO_QSTASH_FORCE_HTTPS = getattr(settings, "DJANGO_QSTASH_FORCE_HTTPS", True)

logger = logging.getLogger(__name__)


# Initialize the QStash receiver
receiver = Receiver(
    current_signing_key=settings.QSTASH_CURRENT_SIGNING_KEY,
    next_signing_key=settings.QSTASH_NEXT_SIGNING_KEY,
)


@csrf_exempt
@require_http_methods(["POST"])
def qstash_webhook_view(request: HttpRequest) -> HttpResponse:
    """
    Webhook handler for QStash callbacks.

    Expects a POST request with:
    - Upstash-Signature header for verification
    - JSON body containing task information:
        {
            "function": "full.path.to.function",
            "module": "module.path",
            "args": [...],
            "kwargs": {...},
            "task_name": "optional_task_name",
            "options": {...}
        }
    """
    try:
        # Get the signature from headers
        signature = request.headers.get("Upstash-Signature")
        if not signature:
            return HttpResponseForbidden("Missing Upstash-Signature header")

        # Verify the signature using the QStash SDK
        url = request.build_absolute_uri()
        if DJANGO_QSTASH_FORCE_HTTPS and not url.startswith("https://"):
            url = url.replace("http://", "https://")
        try:
            receiver.verify(
                body=request.body.decode(),
                signature=signature,
                url=url,
            )
        except Exception as e:
            logger.error(f"Signature verification failed: {e}")
            return HttpResponseForbidden("Invalid signature")

        # Parse the payload
        try:
            payload = json.loads(request.body.decode())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON payload: {e}")
            return HttpResponseBadRequest("Invalid JSON payload")

        # Validate payload structure
        is_valid, error_message = utils.validate_task_payload(payload)
        if not is_valid:
            logger.error(f"Invalid payload structure: {error_message}")
            return HttpResponseBadRequest(error_message)

        # Import the function
        try:
            function_path = f"{payload['module']}.{payload['function']}"
            task_func = utils.import_string(function_path)
        except ImportError as e:
            logger.error(f"Failed to import task function: {e}")
            return HttpResponseBadRequest(f"Could not import task function: {e}")

        # Execute the task
        try:
            if hasattr(task_func, "__call__") and hasattr(task_func, "actual_func"):
                # If it's a wrapped function, call the actual function directly
                result = task_func.actual_func(*payload["args"], **payload["kwargs"])
            else:
                result = task_func(*payload["args"], **payload["kwargs"])

            # Prepare the response
            response_data = {
                "status": "success",
                "task_name": payload.get("task_name", function_path),
                "result": result if result is not None else "null",
            }

            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )

        except Exception as e:
            logger.exception(f"Task execution failed: {e}")
            error_response = {
                "status": "error",
                "task_name": payload.get("task_name", function_path),
                "error": str(e),
            }
            return HttpResponse(
                json.dumps(error_response), status=500, content_type="application/json"
            )

    except Exception as e:
        logger.exception(f"Unexpected error in webhook handler: {e}")
        return HttpResponse(
            json.dumps({"status": "error", "error": "Internal server error"}),
            status=500,
            content_type="application/json",
        )
