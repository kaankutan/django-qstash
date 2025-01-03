from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from django_qstash.discovery.utils import discover_tasks
from django_qstash.discovery.validators import task_exists_validator


class TestTaskExistsValidator(SimpleTestCase):
    def setUp(self):
        discover_tasks.cache_clear()

    def test_validates_existing_task(self):
        """Test that validator passes for existing tasks"""
        # Should not raise any exception
        task_exists_validator("tests.discovery.tasks.debug_task")
        task_exists_validator("tests.discovery.tasks.custom_name_task")

    def test_raises_for_non_existent_task(self):
        """Test that validator raises ValidationError for non-existent tasks"""
        with pytest.raises(ValidationError) as exc_info:
            task_exists_validator("non.existent.task")

        error_message = str(exc_info.value)
        assert "Task 'non.existent.task' not found" in error_message
        assert "Available tasks:" in error_message
        assert "tests.discovery.tasks.debug_task" in error_message
        assert "tests.discovery.tasks.custom_name_task" in error_message
