import pymupdf
from pathlib import Path


OUTPUT_DIR = Path("data/uploads")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def add_page(document, title, sections):
    """
    Add a formatted page to the HLD document.
    """

    page = document.new_page()

    y = 60

    page.insert_text(
        (60, y),
        title,
        fontsize=18
    )

    y += 35

    for heading, lines in sections:

        page.insert_text(
            (60, y),
            heading,
            fontsize=13
        )

        y += 25

        for line in lines:

            page.insert_text(
                (75, y),
                line,
                fontsize=10
            )

            y += 18

        y += 15

    return page


def create_version_1():
    """
    Create AUTOSAR HLD demo Version 1.
    """

    document = pymupdf.open()

    # ========================================================
    # PAGE 1
    # ========================================================

    add_page(
        document,
        "AUTOSAR High-Level Design - Version 1",
        [
            (
                "1. System Overview",
                [
                    "Project: Vehicle Control Platform",
                    "Architecture Type: AUTOSAR Classic",
                    "Purpose: Coordinate vehicle control and sensor data."
                ]
            ),
            (
                "2. Software Components",
                [
                    "Software Component: EngineControl",
                    "Software Component: SensorManager",
                    "Software Component: CommunicationManager"
                ]
            ),
            (
                "3. Interfaces",
                [
                    "Interface: EngineStatus",
                    "Interface: SensorData",
                    "Interface: VehicleCommunication"
                ]
            )
        ]
    )

    # ========================================================
    # PAGE 2
    # ========================================================

    add_page(
        document,
        "AUTOSAR High-Level Design - Version 1",
        [
            (
                "4. Ports",
                [
                    "Port: EngineControl_StatusPort",
                    "Port: SensorManager_DataPort",
                    "Port: CommunicationManager_NetworkPort"
                ]
            ),
            (
                "5. Signals",
                [
                    "Signal: EngineSpeed",
                    "Signal: VehicleSpeed",
                    "Signal: EngineTemperature"
                ]
            ),
            (
                "6. Dependencies",
                [
                    "Dependency: EngineControl -> SensorManager",
                    "Dependency: SensorManager -> CommunicationManager"
                ]
            )
        ]
    )

    # ========================================================
    # PAGE 3
    # ========================================================

    add_page(
        document,
        "AUTOSAR High-Level Design - Version 1",
        [
            (
                "7. Functional Flow",
                [
                    "SensorManager acquires vehicle sensor information.",
                    "EngineControl consumes sensor information.",
                    "CommunicationManager handles external communication."
                ]
            ),
            (
                "8. Architecture Notes",
                [
                    "EngineControl uses EngineStatus for engine state information.",
                    "SensorManager provides sensor-related data to consumers.",
                    "CommunicationManager provides network communication services."
                ]
            ),
            (
                "9. Review Notes",
                [
                    "Architecture shall be reviewed before implementation.",
                    "Interfaces and dependencies shall remain traceable."
                ]
            )
        ]
    )

    output = OUTPUT_DIR / "AUTOSAR_HLD_Demo_v1.pdf"

    document.save(output)
    document.close()

    return output


def create_version_2():
    """
    Create AUTOSAR HLD demo Version 2 with architecture changes.
    """

    document = pymupdf.open()

    # ========================================================
    # PAGE 1
    # ========================================================

    add_page(
        document,
        "AUTOSAR High-Level Design - Version 2",
        [
            (
                "1. System Overview",
                [
                    "Project: Vehicle Control Platform",
                    "Architecture Type: AUTOSAR Classic",
                    "Purpose: Coordinate vehicle control and diagnostic data."
                ]
            ),
            (
                "2. Software Components",
                [
                    "Software Component: EngineControl",
                    "Software Component: CommunicationManager",
                    "Software Component: DiagnosticManager"
                ]
            ),
            (
                "3. Interfaces",
                [
                    "Interface: EngineStatus",
                    "Interface: VehicleStatus",
                    "Interface: VehicleCommunication"
                ]
            )
        ]
    )

    # ========================================================
    # PAGE 2
    # ========================================================

    add_page(
        document,
        "AUTOSAR High-Level Design - Version 2",
        [
            (
                "4. Ports",
                [
                    "Port: EngineControl_StatusPort",
                    "Port: DiagnosticManager_DiagnosticPort",
                    "Port: CommunicationManager_NetworkPort"
                ]
            ),
            (
                "5. Signals",
                [
                    "Signal: EngineSpeed",
                    "Signal: VehicleSpeed",
                    "Signal: DiagnosticStatus"
                ]
            ),
            (
                "6. Dependencies",
                [
                    "Dependency: EngineControl -> DiagnosticManager",
                    "Dependency: DiagnosticManager -> CommunicationManager"
                ]
            )
        ]
    )

    # ========================================================
    # PAGE 3
    # ========================================================

    add_page(
        document,
        "AUTOSAR High-Level Design - Version 2",
        [
            (
                "7. Functional Flow",
                [
                    "DiagnosticManager handles vehicle diagnostic information.",
                    "EngineControl provides engine state information.",
                    "CommunicationManager handles external communication."
                ]
            ),
            (
                "8. Architecture Notes",
                [
                    "EngineControl uses EngineStatus for engine state information.",
                    "DiagnosticManager provides diagnostic services.",
                    "CommunicationManager provides network communication services."
                ]
            ),
            (
                "9. Revision Notes",
                [
                    "SensorManager has been removed.",
                    "DiagnosticManager has been introduced.",
                    "VehicleStatus interface has been introduced.",
                    "Dependency structure has been updated."
                ]
            )
        ]
    )

    output = OUTPUT_DIR / "AUTOSAR_HLD_Demo_v2.pdf"

    document.save(output)
    document.close()

    return output


if __name__ == "__main__":

    version_1 = create_version_1()
    version_2 = create_version_2()

    print("Created:")
    print(version_1)
    print(version_2)