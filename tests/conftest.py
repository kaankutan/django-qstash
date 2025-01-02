from __future__ import annotations

import pytest
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete

from django_qstash.schedules.models import TaskSchedule
from django_qstash.schedules.signals import delete_schedule_from_qstash_receiver
from django_qstash.schedules.signals import sync_schedule_to_qstash_receiver


@pytest.fixture
def task_schedule(db):
    """Fixture that creates a basic TaskSchedule for testing"""
    schedule = TaskSchedule.objects.create(
        name="Test Schedule",
        task="myapp.tasks.sample_task",  # Default task path
        cron="*/5 * * * *",  # Default cron expression
        args=[],
        kwargs={},
        retries=3,
        timeout="30s",
    )
    return schedule


@pytest.fixture(autouse=True)
def disable_qstash_signals():
    """Temporarily disconnect QStash signals."""
    post_save.disconnect(sync_schedule_to_qstash_receiver, sender=TaskSchedule)
    pre_delete.disconnect(delete_schedule_from_qstash_receiver, sender=TaskSchedule)

    yield

    post_save.connect(sync_schedule_to_qstash_receiver, sender=TaskSchedule)
    pre_delete.connect(delete_schedule_from_qstash_receiver, sender=TaskSchedule)
