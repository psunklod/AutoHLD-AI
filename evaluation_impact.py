import time
from backend.services.pdf_service import extract_text_from_pdf
from backend.services.architecture_service import ArchitectureService
from backend.services.comparison_service import ComparisonService
from backend.services.impact_service import ImpactAnalysisService

v1_path = "data/uploads/HLD_v1.pdf"
v2_path = "data/uploads/HLD_v2.pdf"

start = time.perf_counter()

# Extract architectures
v1_pages = extract_text_from_pdf(v1_path)
v2_pages = extract_text_from_pdf(v2_path)

architecture_service = ArchitectureService()
v1 = architecture_service.extract(v1_pages)
v2 = architecture_service.extract(v2_pages)

# Compare revisions
comparison = ComparisonService().compare(v1, v2)

# Analyze impact
impact = ImpactAnalysisService().analyze(comparison)

elapsed = time.perf_counter() - start

print("\n" + "="*60)
print("AUTOHLD AI - IMPACT ANALYSIS")
print("="*60)

print("\nIMPACT ANALYSIS RESULT:")
print(impact)

print(f"\nLATENCY: {elapsed:.2f} seconds")
print("="*60)
