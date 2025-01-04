from __future__ import annotations

from unittest.mock import Mock
from unittest.mock import patch

import pytest

from django_qstash.app import stashed_task


@stashed_task
def sample_task(x, y):
    return x + y


@stashed_task(name="custom_task", deduplicated=True)
def sample_task_with_options(x, y):
    return x * y


@pytest.fixture(autouse=True)
def mock_qstash_client():
    """Mock QStash client for all tests"""
    with patch("django_qstash.app.base.qstash_client") as mock_client:
        # Create a mock for the message object
        mock_message = Mock()
        mock_response = Mock()
        mock_response.message_id = "test-id-123"
        mock_message.publish_json = Mock(return_value=mock_response)

        # Attach the mock message object to the client
        mock_client.message = mock_message
        yield mock_client


@pytest.mark.django_db
class TestQStashTasks:
    def test_basic_task_execution(self):
        """Test that tasks can be executed directly"""
        result = sample_task(2, 3)
        assert result == 5

    def test_task_with_options(self):
        """Test that tasks with custom options work"""
        result = sample_task_with_options(4, 5)
        assert result == 20

    def test_task_delay(self, mock_qstash_client):
        """Test that delay() sends task to QStash"""
        result = sample_task.delay(2, 3)

        assert result.task_id == "test-id-123"
        mock_qstash_client.message.publish_json.assert_called_once()

    def test_task_apply_async(self, mock_qstash_client):
        """Test that apply_async() works with countdown"""
        result = sample_task.apply_async(args=(2, 3), countdown=60)

        assert result.task_id == "test-id-123"
        call_kwargs = mock_qstash_client.message.publish_json.call_args[1]
        assert call_kwargs["delay"] == "60s"
