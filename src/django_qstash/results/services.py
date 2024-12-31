from __future__ import annotations

import logging

from django.apps import apps
from django.utils import timezone

logger = logging.getLogger(__name__)


def store_task_result(
    task_id, task_name, status, result=None, traceback=None, args=None, kwargs=None
):
    """Helper function to store task results if the results app is installed"""
    try:
        TaskResult = apps.get_model("django_qstash_results", "TaskResult")
        task_result = TaskResult.objects.create(
            task_id=task_id,
            task_name=task_name,
            status=status,
            date_done=timezone.now(),
            result=result,
            traceback=traceback,
            args=args,
            kwargs=kwargs,
        )
        return task_result
    except LookupError:
        # Model isn't installed, skip storage
        logger.debug(
            "Django QStash Results not installed. Add `django_qstash.results` to INSTALLED_APPS and run migrations."
        )
        return None
