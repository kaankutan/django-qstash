from __future__ import annotations

from django_qstash.discovery.utils import discover_tasks


def test_discovers_basic_task():
    """Test that basic task discovery works"""
    discover_tasks.cache_clear()
    tasks = discover_tasks()
    expected_tasks = [
        {
            "name": "Custom Name Task",
            "field_label": "Custom Name Task (tests.discovery.tasks)",
            "location": "tests.discovery.tasks.custom_name_task",
        },
        {
            "name": "debug_task",
            "field_label": "tests.discovery.tasks.debug_task",
            "location": "tests.discovery.tasks.debug_task",
        },
        {
            "name": "Cleanup Task Results",
            "field_label": "Cleanup Task Results (django_qstash.results.tasks)",
            "location": "django_qstash.results.tasks.clear_stale_results_task",
        },
        {
            "name": "replace_celery_decorator_task",
            "field_label": "tests.discovery.tasks.replace_celery_decorator_task",
            "location": "tests.discovery.tasks.replace_celery_decorator_task",
        },
    ]
    assert len(tasks) == len(expected_tasks)
    tasks_set = {tuple(sorted(t.items())) for t in tasks}
    expected_tasks_set = {tuple(sorted(t.items())) for t in expected_tasks}
    assert tasks_set == expected_tasks_set
