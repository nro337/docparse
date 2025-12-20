"""_summary_"""

from docling.document_converter import DocumentConverter


def main():
    """_summary_"""
    # print("Hello from docparse!")
    # source = "https://arxiv.org/pdf/2408.09869"
    source = "https://www.nature.com/articles/s41746-025-02022-1"  # document per local path or URL
    converter = DocumentConverter()
    result = converter.convert(source)
    markdown_text = result.document.export_to_markdown()
    with open("output.md", "w", encoding="utf-8") as f:
        f.write(markdown_text)


if __name__ == "__main__":
    main()
