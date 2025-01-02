from __future__ import annotations

from django import forms

from django_qstash.discovery.fields import TaskChoiceField
from django_qstash.schedules.models import TaskSchedule


class TaskScheduleForm(forms.ModelForm):
    task = TaskChoiceField()

    class Meta:
        model = TaskSchedule
        fields = [
            "name",
            "task",
            "task_name",
            "args",
            "kwargs",
            "schedule_id",
            "cron",
            "retries",
            "timeout",
        ]
