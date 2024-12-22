from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from decouple import config
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).parent

DEBUG = os.environ.get("DEBUG", "") == "1"

SECRET_KEY = get_random_secret_key()

QSTASH_TOKEN = config("QSTASH_TOKEN")
QSTASH_CURRENT_SIGNING_KEY = config("QSTASH_CURRENT_SIGNING_KEY")
QSTASH_NEXT_SIGNING_KEY = config("QSTASH_NEXT_SIGNING_KEY")

DJANGO_QSTASH_DOMAIN = config("DJANGO_QSTASH_DOMAIN")
DJANGO_QSTASH_WEBHOOK_PATH = config(
    "DJANGO_QSTASH_WEBHOOK_PATH", default="/qstash/webhook/"
)
# Dangerous: disable host header validation
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "example",
    "django_qstash",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "example.urls"

DATABASES: dict[str, dict[str, Any]] = {}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "example.context_processors.debug",
            ]
        },
    }
]

USE_TZ = True


STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
