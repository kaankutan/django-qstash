from __future__ import annotations

import re

from django_qstash.schedules.exceptions import InvalidDurationStringValidationError


def validate_duration_string(value):
    if not re.match(r"^\d+[smhd]$", value):
        raise InvalidDurationStringValidationError(
            'Invalid duration format. Must be a number followed by s (seconds), m (minutes), h (hours), or d (days). E.g., "60s", "5m", "2h", "7d"'
        )

    # Extract number and unit
    number = int(value[:-1])
    unit = value[-1]

    # Convert to days
    days = {
        "s": number / (24 * 60 * 60),  # seconds to days
        "m": number / (24 * 60),  # minutes to days
        "h": number / 24,  # hours to days
        "d": number,  # already in days
    }[unit]

    if days > 7:
        raise InvalidDurationStringValidationError(
            "Duration too long. Maximum allowed: 7 days (equivalent to: 604800s, 10080m, 168h, 7d)"
        )
