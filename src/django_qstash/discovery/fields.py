from __future__ import annotations

from django import forms

from django_qstash.discovery.utils import discover_tasks
from django_qstash.discovery.validators import task_exists_validator


class TaskChoiceField(forms.ChoiceField):
    """
    A form field that provides choices from discovered QStash tasks
    """

    def __init__(self, *args, **kwargs):
        # Remove max_length if it's present since ChoiceField doesn't use it
        kwargs.pop("max_length", None)

        # Get tasks before calling parent to set choices
        tasks = discover_tasks()

        # Convert tasks to choices using (task_name, task_name) format
        task_choices = [(task_value, task_label) for task_value, task_label in tasks]

        kwargs["choices"] = task_choices
        kwargs["validators"] = [task_exists_validator] + kwargs.get("validators", [])
        super().__init__(*args, **kwargs)

    def get_task(self):
        """
        Returns the actual task dot notation path for the selected value
        """
        if self.data:
            tasks = discover_tasks()

            for task_value, task_label in tasks:
                if task_label == self.data:
                    return task_value
        return None
