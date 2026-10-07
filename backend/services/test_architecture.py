from backend.services.pdf_service import extract_text_from_pdf
from backend.services.architecture_service import ArchitectureService


pdf_path = r"data\uploads\AUTOSAR_HLD_Demo_v1.pdf"

pages = extract_text_from_pdf(pdf_path)

architecture = ArchitectureService()

result = architecture.extract(pages)

print("\nSOFTWARE COMPONENTS:")
for component in result["components"]:
    print(f"- {component}")

print("\nINTERFACES:")
for interface in result["interfaces"]:
    print(f"- {interface}")

print("\nSIGNALS:")
for signal in result["signals"]:
    print(f"- {signal}")

print("\nDEPENDENCIES:")
for dependency in result["dependencies"]:
    print(
        f"- {dependency['source']} "
        f"-> {dependency['target']} "
        f"(Page {dependency['page']})"
    )
