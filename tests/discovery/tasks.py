from __future__ import annotations

from django_qstash import shared_task
from django_qstash import stashed_task


@stashed_task
def debug_task(x, y):
    return x + y


@stashed_task(name="Custom Name Task")
def custom_name_task(x, y):
    return x + y


@shared_task
def replace_celery_decorator_task(x, y):
    return x + y
