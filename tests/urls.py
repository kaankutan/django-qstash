from django.urls import path

from django_qstash.views import qstash_webhook_view

urlpatterns = [
    path("qstash/webhook/", qstash_webhook_view, name="qstash-webhook"),
]
