from __future__ import annotations

from unittest.mock import patch

import pytest
from qstash.schedule import Schedule

from django_qstash.schedules.services import delete_task_schedule_from_qstash
from django_qstash.schedules.services import get_task_schedule_from_qstash
from django_qstash.schedules.services import sync_state_changes
from django_qstash.schedules.services import sync_task_schedule_instance_to_qstash


@pytest.mark.django_db
def test_sync_task_schedule_instance_to_qstash(task_schedule):
    """Test syncing a task schedule to QStash"""
    with patch(
        "django_qstash.schedules.services.qstash_client.schedule.create"
    ) as mock_create:
        result = sync_task_schedule_instance_to_qstash(task_schedule)

        mock_create.assert_called_once()  # Verify the mock was called
        assert result == task_schedule


@pytest.mark.django_db
def test_sync_state_changes_resume(task_schedule):
    """Test syncing state changes when resuming"""
    with (
        patch(
            "django_qstash.schedules.services.qstash_client.schedule.resume"
        ) as mock_resume,
        patch.object(task_schedule, "did_just_resume", return_value=True),
        patch.object(task_schedule, "did_just_pause", return_value=False),
    ):
        sync_state_changes(task_schedule)
        mock_resume.assert_called_once_with(task_schedule.schedule_id)


@pytest.mark.django_db
def test_sync_state_changes_pause(task_schedule):
    """Test syncing state changes when pausing"""
    with (
        patch(
            "django_qstash.schedules.services.qstash_client.schedule.pause"
        ) as mock_pause,
        patch.object(task_schedule, "did_just_resume", return_value=False),
        patch.object(task_schedule, "did_just_pause", return_value=True),
    ):
        sync_state_changes(task_schedule)
        mock_pause.assert_called_once_with(task_schedule.schedule_id)


@pytest.mark.django_db
def test_get_task_schedule_from_qstash(task_schedule):
    """Test getting a schedule from QStash"""
    # Create a Schedule instance with required arguments in positional order
    mock_schedule = Schedule(
        "https://example.com/task",  # url
        "test body",  # body
        3,  # retries
        "*/5 * * * *",  # cron
        "2024-01-01T00:00:00Z",  # created_at
        "2024-01-01T00:05:00Z",  # next_run
        "2024-01-01T00:00:00Z",  # last_run
        "POST",  # method
        {},  # headers
        None,  # delay
        None,  # callback
        "active",  # status
        None,  # failure_callback
        None,  # not_before
    )
    # Set id after creation
    mock_schedule.id = "test-id"

    with patch(
        "django_qstash.schedules.services.qstash_client.schedule.get",
        return_value=mock_schedule,
    ) as mock_get:
        # Test normal response
        result = get_task_schedule_from_qstash(task_schedule)
        assert isinstance(result, Schedule)
        mock_get.assert_called_once_with(task_schedule.schedule_id)

        # Test dict response
        result_dict = get_task_schedule_from_qstash(task_schedule, as_dict=True)
        assert isinstance(result_dict, dict)

        # Test error handling
        mock_get.side_effect = Exception("API Error")
        result = get_task_schedule_from_qstash(task_schedule)
        assert result is None


@pytest.mark.django_db
def test_delete_task_schedule_from_qstash(task_schedule):
    """Test deleting a schedule from QStash"""
    with patch(
        "django_qstash.schedules.services.qstash_client.schedule.delete"
    ) as mock_delete:
        delete_task_schedule_from_qstash(task_schedule)
        mock_delete.assert_called_once_with(task_schedule.schedule_id)

        # Test error handling
        mock_delete.side_effect = Exception("API Error")
        delete_task_schedule_from_qstash(task_schedule)  # Should not raise
