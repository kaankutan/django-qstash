from __future__ import annotations

import json
import logging
from typing import Any

from django.apps import apps
from django.utils import timezone

from django_qstash.db.models import TaskStatus

logger = logging.getLogger(__name__)


def function_result_to_json(result: Any) -> str:
    """Convert a function result to a JSON string"""
    try:
        data = {"result": result}
        return json.dumps(data)
    except Exception as e:
        logger.exception("Failed to convert function result to JSON: %s", str(e))
        return None


def store_task_result(
    task_id,
    task_name,
    status,
    result=None,
    traceback=None,
    args=None,
    kwargs=None,
    error=None,
    function_path=None,
):
    """Helper function to store task results if the results app is installed"""
    if status not in TaskStatus.values:
        status = TaskStatus.UNKNOWN

    try:
        TaskResult = apps.get_model("django_qstash_results", "TaskResult")
        task_result = TaskResult.objects.create(
            task_id=task_id,
            task_name=task_name,
            status=status,
            date_done=timezone.now(),
            result=function_result_to_json(result),
            traceback=traceback,
            args=args,
            kwargs=kwargs,
            function_path=function_path,
        )
        return task_result
    except LookupError:
        # Model isn't installed, skip storage
        logger.debug(
            "Django QStash Results not installed. Add `django_qstash.results` to INSTALLED_APPS and run migrations."
        )
        return None
