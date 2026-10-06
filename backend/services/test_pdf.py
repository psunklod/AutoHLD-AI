from backend.services.pdf_service import extract_text_from_pdf


pdf_path = r"data\uploads\sample.pdf"

pages = extract_text_from_pdf(pdf_path)

print(f"Total pages: {len(pages)}")

for page in pages[:3]:
    print("\n--- Page", page["page"], "---")
    print(page["text"][:500])