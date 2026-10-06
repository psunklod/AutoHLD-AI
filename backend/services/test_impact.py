from backend.services.impact_service import ImpactAnalysisService


comparison = {
    "components": {
        "added": ["DiagnosticManager"],
        "removed": ["SensorManager"],
        "unchanged": ["EngineControl"]
    },

    "interfaces": {
        "added": ["VehicleStatus"],
        "removed": [],
        "unchanged": ["EngineStatus"]
    },

    "ports": {
        "added": [],
        "removed": [],
        "unchanged": []
    },

    "signals": {
        "added": ["VehicleSpeed"],
        "removed": [],
        "unchanged": ["EngineSpeed"]
    },

    "dependencies": {
        "added": [
            ("EngineControl", "DiagnosticManager")
        ],
        "removed": [
            ("EngineControl", "SensorManager")
        ],
        "unchanged": []
    }
}


service = ImpactAnalysisService()

result = service.analyze(comparison)


print("\n=== IMPACT ANALYSIS ===")

print(
    f"Total potential review items: "
    f"{result['total_impacts']}"
)


for impact in result["impacts"]:

    print("\n--------------------------------")

    print(
        f"Type: {impact['type']}"
    )

    print(
        f"Item: {impact['item']}"
    )

    print(
        f"Severity: {impact['severity']}"
    )

    print(
        f"Reason: {impact['reason']}"
    )

    print("Suggested checks:")

    for check in impact["checks"]:

        print(
            f"  - {check}"
        )