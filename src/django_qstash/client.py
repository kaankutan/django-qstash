from __future__ import annotations

from qstash import QStash

from django_qstash.settings import QSTASH_TOKEN

qstash_client = QStash(QSTASH_TOKEN)
