import re


def _is_section_heading(line: str) -> bool:
    """
    Detect numbered section headings such as:

    1. System Overview
    2. Software Components
    6. Dependencies
    """

    match = re.match(
        r"^\s*\d+\.\s+.+$",
        line
    )

    if not match:
        return False

    title = line.strip()

    return len(title) <= 120


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 800
) -> list[dict]:
    """
    Create section-aware chunks from extracted PDF pages.

    Each chunk preserves:
    - page number
    - section heading
    - text

    A new section starts a new chunk.
    Large sections are further split by character length.
    """

    chunks = []

    for page in pages:

        page_number = page["page"]
        text = page.get("text", "")

        if not text.strip():
            continue

        current_section = (
            page.get("section")
            or "Unknown section"
        )

        current_lines = []
        current_length = 0

        def flush_chunk():
            nonlocal current_lines
            nonlocal current_length

            if not current_lines:
                return

            chunk_text = "\n".join(
                current_lines
            ).strip()

            if chunk_text:

                chunks.append({
                    "page": page_number,
                    "section": current_section,
                    "text": chunk_text
                })

            current_lines = []
            current_length = 0

        for raw_line in text.splitlines():

            line = raw_line.strip()

            if not line:
                continue

            # --------------------------------------------------
            # Detect a new section
            # --------------------------------------------------

            if _is_section_heading(line):

                # Finish the previous section's chunk first
                flush_chunk()

                current_section = line

                # Keep the heading inside the new chunk
                current_lines.append(line)

                current_length = len(line)

                continue

            # --------------------------------------------------
            # Normal content
            # --------------------------------------------------

            line_length = len(line) + 1

            # If adding this line would exceed the chunk size,
            # finish the current chunk first.
            if (
                current_lines
                and current_length + line_length > chunk_size
            ):

                flush_chunk()

                # Start the new chunk with the current section
                current_lines.append(
                    f"[Section: {current_section}]"
                )

                current_length = (
                    len(current_section) + 13
                )

            current_lines.append(line)

            current_length += line_length

        # Flush the final chunk of the page
        flush_chunk()

    return chunks