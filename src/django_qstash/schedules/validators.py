from __future__ import annotations

import re

from django_qstash.schedules.exceptions import InvalidDurationStringValidationError


def validate_duration_string(value):
    if not re.match(r"^\d+[smhd]$", value):
        raise InvalidDurationStringValidationError(
            'Invalid duration format. Must be a number followed by s (seconds), m (minutes), h (hours), or d (days). E.g., "60s", "5m", "2h", "7d"'
        )
