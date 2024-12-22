import json
from unittest.mock import patch

import pytest
from django.test import Client


@pytest.mark.django_db
class TestQStashWebhook:
    def setup_method(self):
        self.client = Client()
        self.url = "/qstash/webhook/"  # Adjust if your URL is different

    @patch("django_qstash.views.receiver")
    def test_valid_webhook_request(self, mock_receiver):
        """Test webhook with valid signature and payload"""
        payload = {
            "function": "sample_task",
            "module": "tests.test_tasks",
            "args": [2, 3],
            "kwargs": {},
            "task_name": "test_task",
        }

        # Mock signature verification
        mock_receiver.verify.return_value = True

        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/json",
            headers={"upstash-signature": "mock-signature"},
        )

        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data["status"] == "success"

    def test_missing_signature(self):
        """Test webhook request without signature header"""
        response = self.client.post(
            self.url, data=json.dumps({}), content_type="application/json"
        )
        assert response.status_code == 403

    @patch("django_qstash.views.receiver")
    def test_invalid_json_payload(self, mock_receiver):
        """Test webhook with invalid JSON payload"""
        mock_receiver.verify.return_value = True

        response = self.client.post(
            self.url,
            data="invalid json",
            content_type="application/json",
            headers={"upstash-signature": "mock-signature"},
        )
        assert response.status_code == 400

    @patch("django_qstash.views.receiver")
    def test_invalid_payload_structure(self, mock_receiver):
        """Test webhook with missing required fields"""
        mock_receiver.verify.return_value = True

        payload = {
            "function": "sample_task",
            # missing required fields
        }

        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/json",
            headers={"upstash-signature": "mock-signature"},
        )
        assert response.status_code == 400
