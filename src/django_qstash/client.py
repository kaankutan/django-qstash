from __future__ import annotations

import os
import warnings

from qstash import QStash

from django_qstash.settings import QSTASH_TOKEN

QSTASH_URL = os.environ.get("QSTASH_URL", None)


def init_qstash():
    kwargs = {
        "token": QSTASH_TOKEN,
    }
    if QSTASH_URL is not None:
        warning_msg = f"\n\n\033[93mUsing {QSTASH_URL} as your QStash URL. \
            \nThis configuration should only be used in development.\n\033[0m"
        warnings.warn(warning_msg, RuntimeWarning, stacklevel=2)
        kwargs["base_url"] = QSTASH_URL
    return QStash(**kwargs)


qstash_client = init_qstash()
