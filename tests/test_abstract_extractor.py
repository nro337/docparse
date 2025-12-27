"""Tests for abstract extraction functionality."""

import pytest

from src.abstract_extractor import extract_abstract


class TestExtractAbstract:
    """Test cases for extract_abstract function."""

    def test_extract_abstract_with_hash_heading(self):
        """Test extracting abstract with ## heading."""
        markdown = """# Paper Title

## Abstract

This is the abstract content.

## Introduction

This is the introduction.
"""
        result = extract_abstract(markdown)
        assert result == "This is the abstract content."

    def test_extract_abstract_with_single_hash(self):
        """Test extracting abstract with # heading."""
        markdown = """# Abstract

This is the abstract content.

# Introduction
"""
        result = extract_abstract(markdown)
        assert result == "This is the abstract content."

    def test_extract_abstract_case_insensitive(self):
        """Test that abstract extraction is case-insensitive."""
        markdown = """# Title

## ABSTRACT

This is the abstract.

## Next Section
"""
        result = extract_abstract(markdown)
        assert result == "This is the abstract."

    def test_extract_abstract_with_multiple_paragraphs(self):
        """Test extracting abstract with multiple paragraphs."""
        markdown = """# Title

## Abstract

First paragraph of abstract.

Second paragraph of abstract.

## Introduction
"""
        result = extract_abstract(markdown)
        assert "First paragraph of abstract." in result
        assert "Second paragraph of abstract." in result

    def test_extract_abstract_no_abstract_section(self):
        """Test when there is no abstract section."""
        markdown = """# Title

## Introduction

This is the introduction.
"""
        result = extract_abstract(markdown)
        assert result is None

    def test_extract_abstract_empty_string(self):
        """Test with empty string input."""
        result = extract_abstract("")
        assert result is None

    def test_extract_abstract_none_input(self):
        """Test with None input."""
        result = extract_abstract(None)
        assert result is None

    def test_extract_abstract_empty_abstract_section(self):
        """Test when abstract section exists but is empty."""
        markdown = """# Title

## Abstract

## Introduction

This is the introduction.
"""
        result = extract_abstract(markdown)
        assert result is None

    def test_extract_abstract_with_triple_hash(self):
        """Test extracting abstract with ### heading."""
        markdown = """# Title

### Abstract

This is the abstract.

### Introduction
"""
        result = extract_abstract(markdown)
        assert result == "This is the abstract."

    def test_extract_abstract_stops_at_next_heading(self):
        """Test that extraction stops at the next heading."""
        markdown = """# Title

## Abstract

This is the abstract.
This should be included.

## Introduction

This should not be included.
"""
        result = extract_abstract(markdown)
        assert "This is the abstract." in result
        assert "This should be included." in result
        assert "This should not be included." not in result

    def test_extract_abstract_whitespace_handling(self):
        """Test that extra whitespace is handled correctly."""
        markdown = """# Title

## Abstract

This    has    extra    spaces.

## Introduction
"""
        result = extract_abstract(markdown)
        # Extra spaces should be normalized to single spaces
        assert result == "This has extra spaces."

    def test_extract_abstract_with_mixed_case_heading(self):
        """Test abstract extraction with mixed case heading."""
        markdown = """# Title

## aBsTrAcT

This is the abstract.

## Introduction
"""
        result = extract_abstract(markdown)
        assert result == "This is the abstract."
