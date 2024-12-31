from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from django_qstash.views import qstash_webhook_view

from . import views

urlpatterns = [
    path("", views.index),
    path("admin/", admin.site.urls),
    path("qstash/webhook/", qstash_webhook_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
