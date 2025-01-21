from __future__ import annotations

from django.urls import include
from django.urls import path

urlpatterns = [
    path("qstash/webhook/", include("django_qstash.urls")),
]
