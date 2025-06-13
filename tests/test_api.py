"""Tests for the API client module."""

from unittest.mock import Mock, patch

import pytest

from reader.api import ApiClient, ApiResponse


class TestApiResponse:
    """Tests for ApiResponse dataclass."""

    def test_api_response_creation(self):
        """Test basic ApiResponse creation."""
        response = ApiResponse(status_code=200, data=[{"test": "value"}])
        assert response.status_code == 200
        assert response.data == [{"test": "value"}]
        assert response.message is None

    def test_api_response_with_message(self):
        """Test ApiResponse creation with message."""
        response = ApiResponse(status_code=400, data=[], message="Error occurred")
        assert response.status_code == 400
        assert response.data == []
        assert response.message == "Error occurred"

    def test_api_response_immutable(self):
        """Test that ApiResponse is immutable."""
        response = ApiResponse(status_code=200, data=[])
        with pytest.raises(AttributeError):
            response.status_code = 404  # type: ignore


class TestApiClient:
    """Tests for ApiClient class."""

    def test_client_initialization(self):
        """Test ApiClient initialization."""
        client = ApiClient("https://api.example.com")
        assert client.base_url == "https://api.example.com"

    def test_client_initialization_strips_trailing_slash(self):
        """Test that trailing slash is stripped from base URL."""
        client = ApiClient("https://api.example.com/")
        assert client.base_url == "https://api.example.com"

    @patch("requests.get")
    def test_get_request_success(self, mock_get):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "test"}]
        mock_get.return_value = mock_response

        client = ApiClient("https://api.example.com")
        response = client.get("/endpoint")

        assert response.status_code == 200
        assert response.data == [{"id": 1, "name": "test"}]
        assert response.message is None
        mock_get.assert_called_once_with("https://api.example.com/endpoint", params=None)

    @patch("requests.get")
    def test_get_request_with_params(self, mock_get):
        """Test GET request with parameters."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        client = ApiClient("https://api.example.com")
        params = {"limit": 10, "offset": 0}
        client.get("/endpoint", params=params)

        mock_get.assert_called_once_with("https://api.example.com/endpoint", params=params)

    @patch("requests.post")
    def test_post_request_success(self, mock_post):
        """Test successful POST request."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 1, "created": True}
        mock_post.return_value = mock_response

        client = ApiClient("https://api.example.com")
        data = {"name": "test"}
        response = client.post("/endpoint", data)

        assert response.status_code == 201
        assert response.data == [{"id": 1, "created": True}]
        mock_post.assert_called_once_with("https://api.example.com/endpoint", json=data)

    @patch("requests.get")
    def test_get_request_failure(self, mock_get):
        """Test failed GET request."""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mock_get.return_value = mock_response

        client = ApiClient("https://api.example.com")
        response = client.get("/nonexistent")

        assert response.status_code == 404
        assert response.data == []
        assert response.message == "Not found"

    @patch("requests.get")
    def test_get_request_invalid_json(self, mock_get):
        """Test GET request with invalid JSON response."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        client = ApiClient("https://api.example.com")
        response = client.get("/endpoint")

        assert response.status_code == 200
        assert response.data == []
        assert response.message is None

    @patch("requests.get")
    def test_get_request_non_list_response(self, mock_get):
        """Test GET request that returns non-list JSON."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"single": "object"}
        mock_get.return_value = mock_response

        client = ApiClient("https://api.example.com")
        response = client.get("/endpoint")

        assert response.status_code == 200
        assert response.data == [{"single": "object"}]
