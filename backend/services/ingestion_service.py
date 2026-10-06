from pathlib import Path

from backend.services.pdf_service import extract_text_from_pdf
from backend.rag.chunker import chunk_pages
from backend.rag.vector_store import VectorStore


class IngestionService:
    def __init__(self):
        self.vector_store = VectorStore()

    def process_pdf(self, pdf_path: str) -> dict:
        """
        Extract, chunk and index a PDF.
        """

        pages = extract_text_from_pdf(pdf_path)

        chunks = chunk_pages(
            pages,
            chunk_size=800
        )

        self.vector_store.reset()
        self.vector_store.add_chunks(chunks)

        return {
            "pages": len(pages),
            "chunks": len(chunks)
        }