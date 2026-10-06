import pymupdf
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extract PDF content while preserving:
    - page number
    - detected section/heading
    - page text

    The section is inferred from numbered headings such as:
    1. System Overview
    2. Software Components
    6. Dependencies
    """

    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    pages = []

    with pymupdf.open(pdf_file) as document:

        for page_number, page in enumerate(
            document,
            start=1
        ):

            text = page.get_text("text").strip()

            current_section = None

            for line in text.splitlines():

                line = line.strip()

                if not line:
                    continue

                # Detect headings such as:
                # 1. System Overview
                # 6. Dependencies
                if _looks_like_section_heading(line):
                    current_section = line
                    break

            pages.append({
                "page": page_number,
                "section": current_section,
                "text": text
            })

    return pages


def _looks_like_section_heading(line: str) -> bool:
    """
    Detect simple numbered section headings.

    Examples:
        1. System Overview
        2. Software Components
        6. Dependencies
    """

    parts = line.split(".", 1)

    if len(parts) != 2:
        return False

    number = parts[0].strip()
    title = parts[1].strip()

    return (
        number.isdigit()
        and bool(title)
        and len(title) < 100
    )