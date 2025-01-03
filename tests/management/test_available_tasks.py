from __future__ import annotations

from io import StringIO

import pytest
from django.core.management import call_command


@pytest.mark.django_db
class TestAvailableTasks:
    def test_available_tasks_basic(self):
        """Test that the available_tasks command outputs all task information"""
        out = StringIO()
        call_command("available_tasks", stdout=out)
        output = out.getvalue()

        # Check header
        assert "Available tasks:" in output

        # Updated assertions to match actual implementation
        assert "Name: Custom Name Task" in output
        assert "Location: tests.discovery.tasks.custom_name_task" in output
        assert "Field Label: Custom Name Task (tests.discovery.tasks)" in output

        assert "Name: debug_task" in output
        assert "Location: tests.discovery.tasks.debug_task" in output
        assert "Field Label: tests.discovery.tasks.debug_task" in output

        assert "Name: Cleanup Task Results" in output
        assert (
            "Location: django_qstash.results.tasks.clear_stale_results_task" in output
        )
        assert (
            "Field Label: Cleanup Task Results (django_qstash.results.tasks)" in output
        )

    def test_available_tasks_locations_only(self):
        """Test that the --locations flag only shows task paths"""
        out = StringIO()
        call_command("available_tasks", "--locations", stdout=out)
        output = out.getvalue()

        # Check header
        assert "Available tasks:" in output

        # Updated assertions to match actual output format
        assert "tests.discovery.tasks.custom_name_task" in output
        assert "tests.discovery.tasks.debug_task" in output

        # Verify other details are not present
        assert "Name:" not in output
        assert "Field Label:" not in output
