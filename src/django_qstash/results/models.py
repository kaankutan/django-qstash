from __future__ import annotations

import uuid

from django.db import models
from django.utils import timezone


class TaskResult(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False, unique=True
    )
    task_id = models.CharField(max_length=255, unique=True, db_index=True)
    task_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=[
            ("PENDING", "Pending"),
            ("SUCCESS", "Success"),
            ("FAILURE", "Failure"),
        ],
        default="PENDING",
    )
    date_created = models.DateTimeField(default=timezone.now)
    date_done = models.DateTimeField(null=True)
    result = models.JSONField(null=True)
    traceback = models.TextField(null=True)
    args = models.JSONField(null=True)
    kwargs = models.JSONField(null=True)

    class Meta:
        app_label = "django_qstash_results"
        ordering = ["-date_done"]

    def __str__(self):
        return f"{self.task_name} ({self.task_id})"
