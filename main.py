"""_summary_"""

from docling.document_converter import DocumentConverter

from src.abstract_extractor import extract_abstract


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

    # Extract and display the abstract
    abstract = extract_abstract(markdown_text)
    if abstract:
        print("\n=== ABSTRACT ===")
        print(abstract)
        print("\n")
    else:
        print("No abstract found in the document.")


if __name__ == "__main__":
    main()
