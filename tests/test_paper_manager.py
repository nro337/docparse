"""Tests for paper management functionality."""

import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.paper_manager import PaperManager


class TestPaperManager:
    """Test cases for PaperManager class."""

    @pytest.fixture
    def temp_storage_file(self):
        """Create a temporary storage file for testing."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_file = f.name
        yield temp_file
        # Cleanup
        Path(temp_file).unlink(missing_ok=True)

    @pytest.fixture
    def paper_manager(self, temp_storage_file):
        """Create a PaperManager instance with temporary storage."""
        return PaperManager(storage_file=temp_storage_file)

    def test_initialization_creates_empty_manager(self, paper_manager):
        """Test that a new PaperManager starts empty."""
        assert len(paper_manager.papers) == 0
        assert paper_manager.next_id == 1

    def test_initialization_loads_existing_data(self, temp_storage_file):
        """Test that PaperManager loads existing data from file."""
        # Write test data to storage file
        test_data = {
            "papers": [
                {
                    "id": 1,
                    "url": "https://example.com/paper1",
                    "title": "Test Paper",
                    "abstract": "Test abstract",
                    "added_date": "2024-01-01T00:00:00",
                    "markdown": "# Test Paper",
                }
            ],
            "next_id": 2,
        }
        with open(temp_storage_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        # Create manager - should load the data
        manager = PaperManager(storage_file=temp_storage_file)
        assert len(manager.papers) == 1
        assert manager.next_id == 2
        assert manager.papers[0]["title"] == "Test Paper"

    def test_initialization_handles_corrupted_json(self, temp_storage_file):
        """Test that PaperManager handles corrupted JSON gracefully."""
        # Write invalid JSON
        with open(temp_storage_file, "w", encoding="utf-8") as f:
            f.write("{ invalid json }")

        # Should not raise, should start with empty data
        manager = PaperManager(storage_file=temp_storage_file)
        assert len(manager.papers) == 0
        assert manager.next_id == 1

    def test_add_paper_success(self, paper_manager):
        """Test adding a paper successfully."""
        mock_result = Mock()
        mock_result.document.export_to_markdown.return_value = "# Test Paper\n\n## Abstract\n\nTest abstract\n\n## Introduction\n\nTest intro"

        with patch.object(
            paper_manager.converter, "convert", return_value=mock_result
        ):
            paper = paper_manager.add_paper("https://example.com/paper")

            assert paper["id"] == 1
            assert paper["url"] == "https://example.com/paper"
            assert paper["title"] == "Test Paper"
            assert paper["abstract"] == "Test abstract"
            assert "added_date" in paper
            assert len(paper_manager.papers) == 1

    def test_add_paper_increments_id(self, paper_manager):
        """Test that adding papers increments the ID correctly."""
        mock_result = Mock()
        mock_result.document.export_to_markdown.return_value = "# Paper\n\n## Abstract\n\nAbstract text"

        with patch.object(
            paper_manager.converter, "convert", return_value=mock_result
        ):
            paper1 = paper_manager.add_paper("https://example.com/paper1")
            paper2 = paper_manager.add_paper("https://example.com/paper2")

            assert paper1["id"] == 1
            assert paper2["id"] == 2
            assert paper_manager.next_id == 3

    def test_add_paper_saves_to_storage(self, paper_manager, temp_storage_file):
        """Test that adding a paper saves to storage file."""
        mock_result = Mock()
        mock_result.document.export_to_markdown.return_value = "# Paper\n\n## Abstract\n\nAbstract"

        with patch.object(
            paper_manager.converter, "convert", return_value=mock_result
        ):
            paper_manager.add_paper("https://example.com/paper")

            # Verify file was written
            with open(temp_storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert len(data["papers"]) == 1
                assert data["next_id"] == 2

    def test_add_paper_without_abstract(self, paper_manager):
        """Test adding a paper that has no abstract."""
        mock_result = Mock()
        mock_result.document.export_to_markdown.return_value = "# Paper\n\n## Introduction\n\nSome text"

        with patch.object(
            paper_manager.converter, "convert", return_value=mock_result
        ):
            paper = paper_manager.add_paper("https://example.com/paper")

            assert paper["abstract"] == "No abstract found"

    def test_extract_title_from_markdown(self, paper_manager):
        """Test title extraction from markdown."""
        markdown = "# This is the Title\n\nSome content"
        title = paper_manager._extract_title(markdown, "fallback_url")
        assert title == "This is the Title"

    def test_extract_title_fallback_to_url(self, paper_manager):
        """Test that title falls back to URL when not found."""
        markdown = "No title here\n\nJust content"
        title = paper_manager._extract_title(markdown, "https://example.com/paper")
        assert title == "https://example.com/paper"

    def test_get_all_papers_excludes_markdown(self, paper_manager):
        """Test that get_all_papers excludes full markdown content."""
        mock_result = Mock()
        mock_result.document.export_to_markdown.return_value = "# Paper\n\n## Abstract\n\nAbstract"

        with patch.object(
            paper_manager.converter, "convert", return_value=mock_result
        ):
            paper_manager.add_paper("https://example.com/paper")

            papers = paper_manager.get_all_papers()
            assert len(papers) == 1
            assert "markdown" not in papers[0]
            assert "id" in papers[0]
            assert "title" in papers[0]
            assert "abstract" in papers[0]

    def test_remove_paper_success(self, paper_manager):
        """Test removing a paper successfully."""
        mock_result = Mock()
        mock_result.document.export_to_markdown.return_value = "# Paper\n\n## Abstract\n\nAbstract"

        with patch.object(
            paper_manager.converter, "convert", return_value=mock_result
        ):
            paper = paper_manager.add_paper("https://example.com/paper")
            paper_id = paper["id"]

            result = paper_manager.remove_paper(paper_id)
            assert result is True
            assert len(paper_manager.papers) == 0

    def test_remove_paper_not_found(self, paper_manager):
        """Test removing a paper that doesn't exist."""
        result = paper_manager.remove_paper(999)
        assert result is False

    def test_export_to_markdown_default_filename(self, paper_manager, tmp_path):
        """Test exporting papers to markdown with default filename."""
        mock_result = Mock()
        mock_result.document.export_to_markdown.return_value = "# Paper\n\n## Abstract\n\nAbstract"

        with patch.object(
            paper_manager.converter, "convert", return_value=mock_result
        ):
            paper_manager.add_paper("https://example.com/paper")

            # Change to tmp directory
            import os

            original_dir = os.getcwd()
            os.chdir(tmp_path)

            try:
                filename = paper_manager.export_to_markdown()
                assert filename.startswith("papers_export_")
                assert filename.endswith(".md")
                assert Path(filename).exists()

                # Verify content
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read()
                    assert "# Paper Collection" in content
                    assert "Total papers: 1" in content
            finally:
                os.chdir(original_dir)

    def test_export_to_markdown_custom_filename(self, paper_manager, tmp_path):
        """Test exporting papers to markdown with custom filename."""
        mock_result = Mock()
        mock_result.document.export_to_markdown.return_value = "# Paper\n\n## Abstract\n\nAbstract"

        with patch.object(
            paper_manager.converter, "convert", return_value=mock_result
        ):
            paper_manager.add_paper("https://example.com/paper")

            # Change to tmp directory
            import os

            original_dir = os.getcwd()
            os.chdir(tmp_path)

            try:
                filename = paper_manager.export_to_markdown("custom_export.md")
                assert filename == "custom_export.md"
                assert Path(filename).exists()
            finally:
                os.chdir(original_dir)

    def test_save_papers_handles_write_error(self, paper_manager):
        """Test that save_papers handles write errors gracefully."""
        # Set an invalid storage path
        paper_manager.storage_file = "/invalid/path/that/does/not/exist.json"

        # This should not raise an exception
        paper_manager._save_papers()
