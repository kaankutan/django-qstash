from __future__ import annotations

from django.test import TestCase

from django_qstash.discovery.fields import TaskChoiceField
from django_qstash.discovery.models import TaskField
from django_qstash.discovery.utils import discover_tasks


# @override_settings(INSTALLED_APPS=["tests.discovery"])
class TestTaskChoiceField(TestCase):
    def setUp(self):
        discover_tasks.cache_clear()

    def test_field_initialization(self):
        """Test that the field initializes with correct choices and validators"""
        field = TaskChoiceField()

        expected_choices = [
            (
                "tests.discovery.tasks.custom_name_task",
                "Custom Name Task (tests.discovery.tasks)",
            ),
            (
                "tests.discovery.tasks.debug_task",
                "tests.discovery.tasks.debug_task",
            ),
            (
                "django_qstash.results.tasks.clear_stale_results_task",
                "Cleanup Task Results (django_qstash.results.tasks)",
            ),
        ]
        print(field.choices, expected_choices)
        # Check choices are set correctly
        self.assertEqual(len(field.choices), len(expected_choices))
        self.assertEqual(
            sorted([choice[1] for choice in field.choices]),
            sorted([choice[1] for choice in expected_choices]),
        )

        # Check validator is present
        self.assertEqual(len(field.validators), 1)

    def test_get_task(self):
        """Test that get_task returns correct task path"""
        field = TaskChoiceField()

        # Set value using bound field data
        field.data = "Custom Name Task (tests.discovery.tasks)"

        # Should return the actual task path
        self.assertEqual(field.get_task(), "tests.discovery.tasks.custom_name_task")

    def test_get_task_with_no_value(self):
        """Test that get_task returns None when no value is set"""
        field = TaskChoiceField()
        field.data = None
        self.assertIsNone(field.get_task())

    def test_get_task_with_invalid_value(self):
        """Test that get_task returns None when value doesn't match any task"""
        field = TaskChoiceField()
        field.data = "NonexistentTask"
        self.assertIsNone(field.get_task())

    def test_field_initialization_with_extra_kwargs(self):
        """Test that the field handles extra kwargs properly"""
        field = TaskChoiceField(max_length=100, validators=[lambda x: None])

        # Check that max_length was removed and custom validator was added
        self.assertNotIn("max_length", field.__dict__)
        self.assertEqual(
            len(field.validators), 2
        )  # Default validator + custom validator


# @override_settings(INSTALLED_APPS=["tests.discovery"])
class TestTaskField(TestCase):
    def setUp(self):
        discover_tasks.cache_clear()

    def test_field_initialization(self):
        """Test that the field initializes with correct default max_length"""
        # Test default max_length
        field = TaskField()
        self.assertEqual(field.max_length, 255)

        # Test custom max_length
        field = TaskField(max_length=100)
        self.assertEqual(field.max_length, 100)

    def test_formfield(self):
        """Test that formfield returns TaskChoiceField with correct parameters"""
        field = TaskField()
        form_field = field.formfield()

        # Check that the form field is of correct type
        self.assertIsInstance(form_field, TaskChoiceField)

        # Test with custom parameters
        custom_attrs = {"required": False, "label": "Custom Label"}
        form_field = field.formfield(**custom_attrs)
        self.assertIsInstance(form_field, TaskChoiceField)
        self.assertEqual(form_field.required, False)
        self.assertEqual(form_field.label, "Custom Label")
