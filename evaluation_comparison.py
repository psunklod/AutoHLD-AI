import time
from backend.services.pdf_service import extract_text_from_pdf
from backend.services.architecture_service import ArchitectureService
from backend.services.comparison_service import ComparisonService

v1_path = "data/uploads/HLD_v1.pdf"
v2_path = "data/uploads/HLD_v2.pdf"

start = time.perf_counter()

# Extract PDF text
v1_pages = extract_text_from_pdf(v1_path)
v2_pages = extract_text_from_pdf(v2_path)

# Extract architecture
architecture_service = ArchitectureService()
v1 = architecture_service.extract(v1_pages)
v2 = architecture_service.extract(v2_pages)

# Compare architectures
comparison = ComparisonService().compare(v1, v2)

elapsed = time.perf_counter() - start

print("\n" + "="*60)
print("AUTOHLD AI - HLD REVISION COMPARISON")
print("="*60)

print("\nCOMPONENTS:")
print("  Added:     ", comparison["components"]["added"])
print("  Removed:   ", comparison["components"]["removed"])
print("  Unchanged: ", comparison["components"]["unchanged"])

print("\nINTERFACES:")
print("  Added:     ", comparison["interfaces"]["added"])
print("  Removed:   ", comparison["interfaces"]["removed"])
print("  Unchanged: ", comparison["interfaces"]["unchanged"])

print("\nPORTS:")
print("  Added:     ", comparison["ports"]["added"])
print("  Removed:   ", comparison["ports"]["removed"])
print("  Unchanged: ", comparison["ports"]["unchanged"])

print("\nSIGNALS:")
print("  Added:     ", comparison["signals"]["added"])
print("  Removed:   ", comparison["signals"]["removed"])
print("  Unchanged: ", comparison["signals"]["unchanged"])

print("\nDEPENDENCIES:")
print("  Added:     ", comparison["dependencies"]["added"])
print("  Removed:   ", comparison["dependencies"]["removed"])
print("  Unchanged: ", comparison["dependencies"]["unchanged"])

print(f"\nLATENCY: {elapsed:.2f} seconds")
print("="*60)
