from __future__ import annotations

from django.urls import path

from django_qstash.views import qstash_webhook_view
from example import views

urlpatterns = [
    path("", views.index),
    path("qstash/webhook/", qstash_webhook_view),
]
