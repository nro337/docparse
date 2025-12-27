"""Tests for Flask web application."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from app import app


class TestFlaskApp:
    """Test cases for Flask application endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app."""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def temp_storage_file(self):
        """Create a temporary storage file for testing."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_file = f.name
            # Initialize with empty data
            json.dump({"papers": [], "next_id": 1}, f)
        yield temp_file
        # Cleanup
        Path(temp_file).unlink(missing_ok=True)

    @pytest.fixture
    def mock_paper_manager(self):
        """Mock the paper_manager instance."""
        with patch("app.paper_manager") as mock_pm:
            yield mock_pm

    def test_index_route(self, client):
        """Test the index route returns the main page."""
        response = client.get("/")
        assert response.status_code == 200

    def test_get_papers_empty(self, client, mock_paper_manager):
        """Test getting papers when none exist."""
        mock_paper_manager.get_all_papers.return_value = []

        response = client.get("/api/papers")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_get_papers_with_data(self, client, mock_paper_manager):
        """Test getting papers when some exist."""
        mock_papers = [
            {
                "id": 1,
                "url": "https://example.com/paper1",
                "title": "Paper 1",
                "abstract": "Abstract 1",
                "added_date": "2024-01-01T00:00:00",
            },
            {
                "id": 2,
                "url": "https://example.com/paper2",
                "title": "Paper 2",
                "abstract": "Abstract 2",
                "added_date": "2024-01-02T00:00:00",
            },
        ]
        mock_paper_manager.get_all_papers.return_value = mock_papers

        response = client.get("/api/papers")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]["title"] == "Paper 1"
        assert data[1]["title"] == "Paper 2"

    def test_add_paper_success(self, client, mock_paper_manager):
        """Test adding a paper successfully."""
        mock_paper = {
            "id": 1,
            "url": "https://example.com/paper",
            "title": "Test Paper",
            "abstract": "Test abstract",
            "added_date": "2024-01-01T00:00:00",
            "markdown": "# Test Paper",
        }
        mock_paper_manager.add_paper.return_value = mock_paper

        response = client.post(
            "/api/papers",
            data=json.dumps({"url": "https://example.com/paper"}),
            content_type="application/json",
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["id"] == 1
        assert data["title"] == "Test Paper"
        mock_paper_manager.add_paper.assert_called_once_with("https://example.com/paper")

    def test_add_paper_missing_url(self, client, mock_paper_manager):
        """Test adding a paper without providing a URL."""
        response = client.post(
            "/api/papers", data=json.dumps({}), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert data["error"] == "URL is required"

    def test_add_paper_empty_url(self, client, mock_paper_manager):
        """Test adding a paper with an empty URL."""
        response = client.post(
            "/api/papers", data=json.dumps({"url": ""}), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_add_paper_whitespace_url(self, client, mock_paper_manager):
        """Test adding a paper with a whitespace-only URL."""
        response = client.post(
            "/api/papers",
            data=json.dumps({"url": "   "}),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_add_paper_exception(self, client, mock_paper_manager):
        """Test adding a paper when an exception occurs."""
        mock_paper_manager.add_paper.side_effect = Exception("Failed to convert document")

        response = client.post(
            "/api/papers",
            data=json.dumps({"url": "https://example.com/paper"}),
            content_type="application/json",
        )

        assert response.status_code == 500
        data = json.loads(response.data)
        assert "error" in data
        assert "Failed to convert document" in data["error"]

    def test_delete_paper_success(self, client, mock_paper_manager):
        """Test deleting a paper successfully."""
        mock_paper_manager.remove_paper.return_value = True

        response = client.delete("/api/papers/1")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        mock_paper_manager.remove_paper.assert_called_once_with(1)

    def test_delete_paper_not_found(self, client, mock_paper_manager):
        """Test deleting a paper that doesn't exist."""
        mock_paper_manager.remove_paper.return_value = False

        response = client.delete("/api/papers/999")

        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data
        assert data["error"] == "Paper not found"

    def test_export_papers_success(self, client, mock_paper_manager):
        """Test exporting papers successfully."""
        mock_paper_manager.export_to_markdown.return_value = "papers_export_20240101_120000.md"

        response = client.post("/api/export")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert "filename" in data
        assert data["filename"] == "papers_export_20240101_120000.md"

    def test_export_papers_exception(self, client, mock_paper_manager):
        """Test exporting papers when an exception occurs."""
        mock_paper_manager.export_to_markdown.side_effect = Exception("Export failed")

        response = client.post("/api/export")

        assert response.status_code == 500
        data = json.loads(response.data)
        assert "error" in data
        assert "Export failed" in data["error"]
