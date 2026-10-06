from backend.services.comparison_service import ComparisonService


old_architecture = {
    "components": [
        "EngineControl",
        "SensorManager"
    ],
    "interfaces": [
        "EngineStatus"
    ],
    "ports": [
        "EnginePort"
    ],
    "signals": [
        "EngineSpeed"
    ],
    "dependencies": [
        {
            "source": "EngineControl",
            "target": "SensorManager",
            "page": 1
        }
    ]
}


new_architecture = {
    "components": [
        "EngineControl",
        "DiagnosticManager"
    ],
    "interfaces": [
        "EngineStatus",
        "VehicleStatus"
    ],
    "ports": [
        "EnginePort"
    ],
    "signals": [
        "EngineSpeed",
        "VehicleSpeed"
    ],
    "dependencies": [
        {
            "source": "EngineControl",
            "target": "DiagnosticManager",
            "page": 2
        }
    ]
}


comparison_service = ComparisonService()

result = comparison_service.compare(
    old_architecture,
    new_architecture
)


print("\n=== COMPONENT CHANGES ===")
print("Added:", result["components"]["added"])
print("Removed:", result["components"]["removed"])
print("Unchanged:", result["components"]["unchanged"])


print("\n=== INTERFACE CHANGES ===")
print("Added:", result["interfaces"]["added"])
print("Removed:", result["interfaces"]["removed"])


print("\n=== PORT CHANGES ===")
print("Added:", result["ports"]["added"])
print("Removed:", result["ports"]["removed"])


print("\n=== SIGNAL CHANGES ===")
print("Added:", result["signals"]["added"])
print("Removed:", result["signals"]["removed"])


print("\n=== DEPENDENCY CHANGES ===")
print("Added:", result["dependencies"]["added"])
print("Removed:", result["dependencies"]["removed"])