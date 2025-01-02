from __future__ import annotations

from django_qstash import shared_task


@shared_task
def debug_task(x, y):
    return x + y


@shared_task(name="Custom Name Task")
def custom_name_task(x, y):
    return x + y
