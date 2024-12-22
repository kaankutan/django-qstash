import functools
import json
from typing import Any, Callable, Dict, Optional, Tuple

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from qstash import QStash

QSTASH_TOKEN = getattr(settings, "QSTASH_TOKEN", None)
DJANGO_QSTASH_CALLBACK_URL = getattr(settings, "DJANGO_QSTASH_CALLBACK_URL", None)
DJANGO_QSTASH_WEBHOOK_PATH = getattr(
    settings, "DJANGO_QSTASH_WEBHOOK_PATH", "/qstash/webhook/"
)

if not QSTASH_TOKEN or not DJANGO_QSTASH_CALLBACK_URL:
    raise ImproperlyConfigured(
        "QSTASH_TOKEN and DJANGO_QSTASH_CALLBACK_URL must be set"
    )

# Initialize QStash client once
qstash_client = QStash(QSTASH_TOKEN)


class QStashTask:
    def __init__(
        self,
        func: Optional[Callable] = None,
        name: Optional[str] = None,
        delay_seconds: Optional[int] = None,
        deduplicated: bool = False,
        **options: Dict[str, Any],
    ):
        self.func = func
        self.name = name or (func.__name__ if func else None)
        self.delay_seconds = delay_seconds
        self.deduplicated = deduplicated
        self.options = options
        self.callback_url = DJANGO_QSTASH_CALLBACK_URL.rstrip("/")
        self.webhook_path = DJANGO_QSTASH_WEBHOOK_PATH.strip("/")

        if func is not None:
            functools.update_wrapper(self, func)

    def __get__(self, obj, objtype):
        """Support for instance methods"""
        return functools.partial(self.__call__, obj)

    def __call__(self, *args, **kwargs):
        """
        Execute the task, either directly or via QStash based on context
        """
        # Handle the case when the decorator is used without parameters
        if self.func is None:
            return self.__class__(
                args[0],
                name=self.name,
                delay_seconds=self.delay_seconds,
                deduplicated=self.deduplicated,
                **self.options,
            )

        # If called directly (not through delay/apply_async), execute the function
        if not getattr(self, "_is_delayed", False):
            return self.func(*args, **kwargs)

        # Reset the delayed flag
        self._is_delayed = False

        # Prepare the payload
        payload = {
            "function": self.func.__name__,
            "module": self.func.__module__,
            "args": args,  # Send args as-is
            "kwargs": kwargs,
            "task_name": self.name,
            "options": self.options,
        }

        # Ensure callback URL is properly formatted
        callback_url = self.callback_url
        if not callback_url.startswith(("http://", "https://")):
            callback_url = f"https://{callback_url}"

        url = f"{callback_url}/{self.webhook_path}/"
        # Send to QStash using the official SDK
        response = qstash_client.message.publish_json(
            url=url,
            body=payload,
            delay=f"{self.delay_seconds}s" if self.delay_seconds else None,
            retries=self.options.get("max_retries", 3),
            content_based_deduplication=self.deduplicated,
        )
        # Return an AsyncResult-like object for Celery compatibility
        return AsyncResult(response.message_id)

    def delay(self, *args, **kwargs) -> "AsyncResult":
        """Celery-compatible delay() method"""
        self._is_delayed = True
        return self(*args, **kwargs)

    def apply_async(
        self,
        args: Optional[Tuple] = None,
        kwargs: Optional[Dict] = None,
        countdown: Optional[int] = None,
        **options: Dict[str, Any],
    ) -> "AsyncResult":
        """Celery-compatible apply_async() method"""
        self._is_delayed = True
        if countdown is not None:
            self.delay_seconds = countdown
        self.options.update(options)

        # Fix: Ensure we're passing the arguments correctly
        args = args or ()
        kwargs = kwargs or {}
        return self(*args, **kwargs)


class AsyncResult:
    """Minimal Celery AsyncResult-compatible class"""

    def __init__(self, task_id: str):
        self.task_id = task_id

    def get(self, timeout: Optional[int] = None) -> Any:
        """Simulate Celery's get() method"""
        raise NotImplementedError("QStash doesn't support result retrieval")

    @property
    def id(self) -> str:
        return self.task_id


def shared_task(
    func: Optional[Callable] = None,
    name: Optional[str] = None,
    deduplicated: bool = False,
    **options: Dict[str, Any],
) -> QStashTask:
    """
    Decorator that mimics Celery's shared_task

    Can be used as:
        @shared_task
        def my_task():
            pass

        @shared_task(name="custom_name", deduplicated=True)
        def my_task():
            pass
    """
    if func is not None:
        return QStashTask(func, name=name, deduplicated=deduplicated, **options)
    return lambda f: QStashTask(f, name=name, deduplicated=deduplicated, **options)
