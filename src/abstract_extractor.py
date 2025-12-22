"""Abstract extraction module for markdown documents."""

import re
from typing import Optional


def extract_abstract(markdown_text: str) -> Optional[str]:
    """
    Extract the abstract section from markdown text.

    This function detects and extracts the abstract content from academic papers
    or documents formatted in markdown. It looks for common abstract patterns
    including headings like "Abstract", "## Abstract", "ABSTRACT", etc.

    Args:
        markdown_text: The full markdown content as a string

    Returns:
        The abstract text as a string if found, None otherwise

    Examples:
        >>> markdown = "# Title\\n\\n## Abstract\\n\\nThis is the abstract.\\n\\n## Introduction"
        >>> extract_abstract(markdown)
        'This is the abstract.'
    """
    if not markdown_text:
        return None

    # Pattern to match abstract heading (case-insensitive, with various markdown levels)
    # Matches: ## Abstract, # Abstract, ### Abstract, ABSTRACT, etc.
    abstract_pattern = r"^#{1,6}\s*Abstract\s*$"

    lines = markdown_text.split("\n")
    abstract_start_idx = None

    # Find the line with the abstract heading
    for i, line in enumerate(lines):
        if re.match(abstract_pattern, line.strip(), re.IGNORECASE):
            abstract_start_idx = i
            break

    if abstract_start_idx is None:
        return None

    # Extract content after the abstract heading until the next heading
    abstract_lines = []
    for i in range(abstract_start_idx + 1, len(lines)):
        line = lines[i].strip()

        # Stop if we hit another heading (lines starting with #)
        if re.match(r"^#{1,6}\s+\w+", line):
            break

        # Add non-empty lines to abstract
        if line:
            abstract_lines.append(line)

    if not abstract_lines:
        return None

    # Join lines and clean up extra whitespace
    abstract_text = " ".join(abstract_lines)
    abstract_text = re.sub(r"\s+", " ", abstract_text).strip()

    return abstract_text
