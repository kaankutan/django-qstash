from __future__ import annotations

import os

from qstash import QStash

from django_qstash.settings import QSTASH_TOKEN

QSTASH_URL = os.environ.get("QSTASH_URL", None)


def init_qstash():
    kwargs = {
        "token": QSTASH_TOKEN,
    }
    if QSTASH_URL is not None:
        kwargs["base_url"] = QSTASH_URL
    return QStash(**kwargs)


qstash_client = init_qstash()
