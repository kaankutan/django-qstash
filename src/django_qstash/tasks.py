from __future__ import annotations

import functools
import warnings
from typing import Any
from typing import Callable

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from qstash import QStash

QSTASH_TOKEN = getattr(settings, "QSTASH_TOKEN", None)
DJANGO_QSTASH_DOMAIN = getattr(settings, "DJANGO_QSTASH_DOMAIN", None)
DJANGO_QSTASH_WEBHOOK_PATH = getattr(
    settings, "DJANGO_QSTASH_WEBHOOK_PATH", "/qstash/webhook/"
)
if not QSTASH_TOKEN or not DJANGO_QSTASH_DOMAIN:
    warnings.warn(
        "QSTASH_TOKEN and DJANGO_QSTASH_DOMAIN should be set for QStash functionality",
        RuntimeWarning,
        stacklevel=2,
    )

# Initialize QStash client once
qstash_client = QStash(QSTASH_TOKEN)


class QStashTask:
    def __init__(
        self,
        func: Callable | None = None,
        name: str | None = None,
        delay_seconds: int | None = None,
        deduplicated: bool = False,
        **options: dict[str, Any],
    ):
        self.func = func
        self.name = name or (func.__name__ if func else None)
        self.delay_seconds = delay_seconds
        self.deduplicated = deduplicated
        self.options = options
        self.callback_domain = DJANGO_QSTASH_DOMAIN.rstrip("/")
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
        if not QSTASH_TOKEN or not DJANGO_QSTASH_DOMAIN:
            raise ImproperlyConfigured(
                "QSTASH_TOKEN and DJANGO_QSTASH_DOMAIN must be set to use django-qstash"
            )
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
        callback_domain = self.callback_domain
        if not callback_domain.startswith(("http://", "https://")):
            callback_domain = f"https://{callback_domain}"

        url = f"{callback_domain}/{self.webhook_path}/"
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

    def delay(self, *args, **kwargs) -> AsyncResult:
        """Celery-compatible delay() method"""
        self._is_delayed = True
        return self(*args, **kwargs)

    def apply_async(
        self,
        args: tuple | None = None,
        kwargs: dict | None = None,
        countdown: int | None = None,
        **options: dict[str, Any],
    ) -> AsyncResult:
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

    def get(self, timeout: int | None = None) -> Any:
        """Simulate Celery's get() method"""
        raise NotImplementedError("QStash doesn't support result retrieval")

    @property
    def id(self) -> str:
        return self.task_id


def shared_task(
    func: Callable | None = None,
    name: str | None = None,
    deduplicated: bool = False,
    **options: dict[str, Any],
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
