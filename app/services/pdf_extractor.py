from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(file_path: str | Path) -> str:
    """Read a PDF file and return its combined text content as a string."""
    reader = PdfReader(str(file_path))
    pages: list[str] = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            pages.append(page_text.strip())

    combined = "\n\n".join(pages)
    return combined.strip()
