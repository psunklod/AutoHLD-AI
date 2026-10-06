from backend.services.pdf_service import extract_text_from_pdf
from backend.rag.chunker import chunk_pages


pdf_path = r"data\uploads\AUTOSAR_HLD_Demo_v1.pdf"

pages = extract_text_from_pdf(
    pdf_path
)

chunks = chunk_pages(
    pages,
    chunk_size=800
)


print(
    f"Total pages: {len(pages)}"
)

print(
    f"Total chunks: {len(chunks)}"
)


for index, chunk in enumerate(
    chunks,
    start=1
):

    print()
    print(
        "=" * 70
    )

    print(
        f"CHUNK {index}"
    )

    print(
        f"Page: {chunk['page']}"
    )

    print(
        f"Section: {chunk['section']}"
    )

    print(
        "=" * 70
    )

    print(
        chunk["text"]
    )