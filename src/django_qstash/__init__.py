from __future__ import annotations

__version__ = "0.0.12"

from django_qstash.app import shared_task
from django_qstash.app import stashed_task

__all__ = ["stashed_task", "shared_task"]
