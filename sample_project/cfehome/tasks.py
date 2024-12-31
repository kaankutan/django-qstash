from __future__ import annotations

import logging

from django_qstash import shared_task

logger = logging.getLogger(__name__)

"""
from cfehome.tasks import *
math_add_task.apply_async(args=(12, 454))
math_add_task.apply_async(args=(12, 12), delay=10)
"""


@shared_task
def math_add_task(a, b):
    logger.info("Adding %s and %s", a, b)
    with open("test.txt", "w") as f:
        f.write(f"{a} + {b} = {a + b}")
    return a + b
