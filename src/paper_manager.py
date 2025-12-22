"""Paper management module for storing and exporting papers."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from docling.document_converter import DocumentConverter

from src.abstract_extractor import extract_abstract


class PaperManager:
    """Manages paper collection and export."""

    def __init__(self, storage_file: str = "papers_data.json"):
        """Initialize the paper manager.

        Args:
            storage_file: Path to JSON file for storing paper data
        """
        self.storage_file = storage_file
        self.papers: List[Dict] = []
        self.next_id = 1
        self.converter = DocumentConverter()
        self._load_papers()

    def _load_papers(self):
        """Load papers from storage file."""
        if Path(self.storage_file).exists():
            with open(self.storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.papers = data.get("papers", [])
                self.next_id = data.get("next_id", 1)

    def _save_papers(self):
        """Save papers to storage file."""
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump({"papers": self.papers, "next_id": self.next_id}, f, indent=2)

    def add_paper(self, url: str) -> Dict:
        """Add a new paper by URL.

        Args:
            url: URL of the paper to add

        Returns:
            Dictionary containing paper information

        Raises:
            Exception: If paper extraction fails
        """
        # Convert document
        result = self.converter.convert(url)
        markdown_text = result.document.export_to_markdown()

        # Extract title and abstract
        title = self._extract_title(markdown_text, url)
        abstract = extract_abstract(markdown_text)

        # Create paper entry
        paper = {
            "id": self.next_id,
            "url": url,
            "title": title,
            "abstract": abstract or "No abstract found",
            "added_date": datetime.now().isoformat(),
            "markdown": markdown_text,
        }

        self.papers.append(paper)
        self.next_id += 1
        self._save_papers()

        return paper

    def _extract_title(self, markdown_text: str, url: str) -> str:
        """Extract title from markdown text.

        Args:
            markdown_text: The markdown content
            url: The source URL (fallback if title not found)

        Returns:
            The extracted title or URL if not found
        """
        lines = markdown_text.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("# ") and len(line) > 2:
                return line[2:].strip()

        # Fallback to URL if no title found
        return url

    def get_all_papers(self) -> List[Dict]:
        """Get all papers.

        Returns:
            List of all paper dictionaries (without full markdown)
        """
        return [
            {
                "id": p["id"],
                "url": p["url"],
                "title": p["title"],
                "abstract": p["abstract"],
                "added_date": p["added_date"],
            }
            for p in self.papers
        ]

    def remove_paper(self, paper_id: int) -> bool:
        """Remove a paper by ID.

        Args:
            paper_id: ID of the paper to remove

        Returns:
            True if removed, False if not found
        """
        initial_length = len(self.papers)
        self.papers = [p for p in self.papers if p["id"] != paper_id]

        if len(self.papers) < initial_length:
            self._save_papers()
            return True
        return False

    def export_to_markdown(self, filename: Optional[str] = None) -> str:
        """Export all papers to a markdown file.

        Args:
            filename: Output filename (default: papers_export_TIMESTAMP.md)

        Returns:
            The filename that was created
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"papers_export_{timestamp}.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write("# Paper Collection\n\n")
            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total papers: {len(self.papers)}\n\n")
            f.write("---\n\n")

            for i, paper in enumerate(self.papers, 1):
                f.write(f"## {i}. {paper['title']}\n\n")
                f.write(f"**URL:** {paper['url']}\n\n")
                f.write(f"**Added:** {paper['added_date']}\n\n")
                f.write("### Abstract\n\n")
                f.write(f"{paper['abstract']}\n\n")
                f.write("---\n\n")

        return filename
