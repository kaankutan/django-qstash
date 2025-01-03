from __future__ import annotations

from django.test import override_settings

from django_qstash.discovery.utils import discover_tasks


@override_settings(INSTALLED_APPS=["tests.discovery"])
def test_discovers_basic_task():
    """Test that basic task discovery works"""
    tasks = discover_tasks()
    expected_tasks = [
        (
            "tests.discovery.tasks.custom_name_task",
            "Custom Name Task (tests.discovery.tasks)",
        ),
        (
            "tests.discovery.tasks.debug_task",
            "tests.discovery.tasks.debug_task",
        ),
    ]
    assert len(tasks) == len(expected_tasks)

    task_values = [task[0] for task in tasks]
    expected_task_values = [task[0] for task in expected_tasks]
    assert expected_task_values == task_values
    task_labels = [task[1] for task in tasks]
    expected_task_labels = [task[1] for task in expected_tasks]
    assert expected_task_labels == task_labels
