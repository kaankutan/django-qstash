from __future__ import annotations

from typing import Any
from typing import Callable

from django_qstash.app.base import QStashTask


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
