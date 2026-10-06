from backend.services.pdf_service import extract_text_from_pdf


pdf_path = r"data\uploads\AUTOSAR_HLD_Demo_v1.pdf"

pages = extract_text_from_pdf(pdf_path)

print(f"Pages: {len(pages)}")

for page in pages:
    print()
    print("=" * 60)
    print(f"PAGE {page['page']}")
    print("=" * 60)
    print(page["text"][:1200])