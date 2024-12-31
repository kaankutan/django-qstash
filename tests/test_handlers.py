from __future__ import annotations

import json
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from django.http import HttpRequest

from django_qstash.exceptions import PayloadError
from django_qstash.exceptions import SignatureError
from django_qstash.exceptions import TaskError
from django_qstash.handlers import QStashWebhook
from django_qstash.handlers import TaskPayload


class TestTaskPayload:
    def test_from_dict_valid(self):
        data = {
            "function": "test_func",
            "module": "test_module",
            "args": [1, 2],
            "kwargs": {"key": "value"},
        }
        payload = TaskPayload.from_dict(data)

        assert payload.function == "test_func"
        assert payload.module == "test_module"
        assert payload.args == [1, 2]
        assert payload.kwargs == {"key": "value"}
        assert payload.task_name == "test_module.test_func"
        assert payload.function_path == "test_module.test_func"

    def test_from_dict_invalid(self):
        data = {"invalid": "data"}
        with pytest.raises(PayloadError):
            TaskPayload.from_dict(data)


class TestQStashWebhook:
    @pytest.fixture
    def webhook(self):
        return QStashWebhook()

    def test_verify_signature_missing(self, webhook):
        with pytest.raises(SignatureError, match="Missing Upstash-Signature"):
            webhook.verify_signature("body", "", "http://example.com")

    def test_verify_signature_invalid(self, webhook):
        with pytest.raises(SignatureError, match="Invalid signature"):
            webhook.verify_signature("body", "invalid", "http://example.com")

    def test_parse_payload_invalid_json(self, webhook):
        with pytest.raises(PayloadError, match="Invalid JSON payload"):
            webhook.parse_payload("invalid json")

    def test_execute_task_import_error(self, webhook):
        payload = Mock(function_path="nonexistent.module")
        with pytest.raises(TaskError, match="Could not import task function"):
            webhook.execute_task(payload)

    def test_handle_request_success(self, webhook):
        request = Mock(spec=HttpRequest)
        request.body = json.dumps(
            {"function": "test_func", "module": "test_module", "args": [], "kwargs": {}}
        ).encode()
        request.headers = {"Upstash-Signature": "valid", "Upstash-Message-Id": "123"}
        request.build_absolute_uri.return_value = "https://example.com"

        with (
            patch.object(webhook, "verify_signature"),
            patch.object(webhook, "execute_task") as mock_execute,
        ):
            mock_execute.return_value = "result"
            response, status = webhook.handle_request(request)

        assert status == 200
        assert response["status"] == "success"
        assert response["result"] == "result"

    def test_handle_request_signature_error(self, webhook):
        request = Mock(spec=HttpRequest)
        request.body = json.dumps(
            {"function": "test_func", "module": "test_module", "args": [], "kwargs": {}}
        ).encode()
        request.headers = {}
        request.build_absolute_uri.return_value = "https://example.com"

        response, status = webhook.handle_request(request)

        assert status == 400
        assert response["status"] == "error"
        assert response["error_type"] == "SignatureError"
