from pathlib import Path

from backend.services.pdf_service import extract_text_from_pdf
from backend.services.architecture_service import ArchitectureService
from backend.rag.chunker import chunk_pages
from backend.rag.vector_store import VectorStore
from backend.rag.rag_service import RAGService
from backend.services.comparison_service import ComparisonService
from backend.services.impact_service import ImpactAnalysisService


PROJECT_ROOT = Path(__file__).resolve().parents[2]

V1_PATH = (
    PROJECT_ROOT
    / "data"
    / "uploads"
    / "AUTOSAR_HLD_Demo_v1.pdf"
)

V2_PATH = (
    PROJECT_ROOT
    / "data"
    / "uploads"
    / "AUTOSAR_HLD_Demo_v2.pdf"
)


def check(condition: bool, message: str):
    if condition:
        print(f"[PASS] {message}")
    else:
        print(f"[FAIL] {message}")


print()
print("=" * 70)
print("AutoHLD AI - SYSTEM VALIDATION")
print("=" * 70)


# ============================================================
# 1. CHECK FILES
# ============================================================

print()
print("1. DOCUMENT CHECK")

check(
    V1_PATH.exists(),
    "Version 1 HLD exists"
)

check(
    V2_PATH.exists(),
    "Version 2 HLD exists"
)


# ============================================================
# 2. PDF EXTRACTION
# ============================================================

print()
print("2. PDF EXTRACTION")

v1_pages = extract_text_from_pdf(
    str(V1_PATH)
)

v2_pages = extract_text_from_pdf(
    str(V2_PATH)
)

check(
    len(v1_pages) == 3,
    "Version 1 contains 3 pages"
)

check(
    len(v2_pages) == 3,
    "Version 2 contains 3 pages"
)


# ============================================================
# 3. SECTION-AWARE CHUNKING
# ============================================================

print()
print("3. SECTION-AWARE CHUNKING")

v1_chunks = chunk_pages(
    v1_pages,
    chunk_size=800
)

check(
    len(v1_chunks) > 0,
    "Chunks were created"
)

sections = [
    chunk.get("section")
    for chunk in v1_chunks
]

check(
    any(
        section == "6. Dependencies"
        for section in sections
    ),
    "Dependencies section metadata detected"
)


# ============================================================
# 4. ARCHITECTURE EXTRACTION
# ============================================================

print()
print("4. ARCHITECTURE EXTRACTION")

architecture_service = ArchitectureService()

v1_architecture = architecture_service.extract(
    v1_pages
)

v2_architecture = architecture_service.extract(
    v2_pages
)

check(
    len(v1_architecture["components"]) == 3,
    "Version 1 has 3 software components"
)

check(
    len(v1_architecture["interfaces"]) == 3,
    "Version 1 has 3 interfaces"
)

check(
    len(v1_architecture["ports"]) == 3,
    "Version 1 has 3 ports"
)

check(
    len(v1_architecture["signals"]) == 3,
    "Version 1 has 3 signals"
)

check(
    len(v1_architecture["dependencies"]) == 2,
    "Version 1 has 2 dependencies"
)


# ============================================================
# 5. DEPENDENCY CONTENT
# ============================================================

print()
print("5. DEPENDENCY CHECK")

dependency_pairs = {
    (
        dependency["source"],
        dependency["target"]
    )
    for dependency
    in v1_architecture["dependencies"]
}

check(
    (
        "EngineControl",
        "SensorManager"
    )
    in dependency_pairs,
    "EngineControl -> SensorManager detected"
)

check(
    (
        "SensorManager",
        "CommunicationManager"
    )
    in dependency_pairs,
    "SensorManager -> CommunicationManager detected"
)


# ============================================================
# 6. VECTOR STORE / RAG
# ============================================================

print()
print("6. RAG CHECK")

vector_store = VectorStore()

check(
    vector_store.collection.count() > 0,
    "Vector store contains indexed HLD data"
)

rag = RAGService()

rag_result = rag.prepare_question(
    "What dependencies are defined?",
    top_k=3
)

check(
    len(rag_result["results"]) > 0,
    "RAG returned relevant evidence"
)

check(
    len(rag_result["sources"]) > 0,
    "RAG returned source metadata"
)

check(
    any(
        source.get("section") == "6. Dependencies"
        for source in rag_result["sources"]
    ),
    "RAG returned Dependencies section evidence"
)


# ============================================================
# 7. REVISION COMPARISON
# ============================================================

print()
print("7. REVISION COMPARISON")

comparison_service = ComparisonService()

comparison = comparison_service.compare(
    v1_architecture,
    v2_architecture
)

check(
    "DiagnosticManager"
    in comparison["components"]["added"],
    "DiagnosticManager detected as added"
)

check(
    "SensorManager"
    in comparison["components"]["removed"],
    "SensorManager detected as removed"
)

check(
    "VehicleStatus"
    in comparison["interfaces"]["added"],
    "VehicleStatus detected as added"
)

check(
    "DiagnosticStatus"
    in comparison["signals"]["added"],
    "DiagnosticStatus detected as added"
)

check(
    "EngineTemperature"
    in comparison["signals"]["removed"],
    "EngineTemperature detected as removed"
)

check(
    "VehicleSpeed"
    in comparison["signals"]["unchanged"],
    "VehicleSpeed detected as unchanged"
)


# ============================================================
# 8. DEPENDENCY REVISION CHECK
# ============================================================

print()
print("8. DEPENDENCY REVISION CHECK")

added_dependencies = set(
    comparison["dependencies"]["added"]
)

removed_dependencies = set(
    comparison["dependencies"]["removed"]
)

check(
    (
        "EngineControl",
        "DiagnosticManager"
    )
    in added_dependencies,
    "New dependency detected"
)

check(
    (
        "EngineControl",
        "SensorManager"
    )
    in removed_dependencies,
    "Removed dependency detected"
)


# ============================================================
# 9. IMPACT ANALYSIS
# ============================================================

print()
print("9. IMPACT ANALYSIS")

impact_service = ImpactAnalysisService()

impact_result = impact_service.analyze(
    comparison
)

check(
    impact_result["total_impacts"] > 0,
    "Potential engineering impacts detected"
)

check(
    any(
        impact["item"] == "SensorManager"
        for impact
        in impact_result["impacts"]
    ),
    "Removed SensorManager appears in impact analysis"
)


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)
print()