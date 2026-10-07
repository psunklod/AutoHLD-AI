from backend.services.pdf_service import extract_text_from_pdf
from backend.rag.chunker import chunk_pages
from backend.rag.vector_store import VectorStore


pdf_path = r"data\uploads\AUTOSAR_HLD_Demo_v1.pdf"

pages = extract_text_from_pdf(pdf_path)
chunks = chunk_pages(pages, chunk_size=300)

store = VectorStore()

store.add_chunks(chunks)

results = store.search("Which software component is mentioned?", top_k=2)

print("\nSearch results:")

for result in results:
    print(f"\nPage: {result['page']}")
    print(f"Distance: {result['distance']:.4f}")
    print(result["text"])
