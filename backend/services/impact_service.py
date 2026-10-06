class ImpactAnalysisService:
    """
    Identify potential engineering review areas from HLD revision changes.

    This service does not make design decisions.
    It only highlights areas that may require engineering review.
    """

    def analyze(self, comparison: dict) -> dict:
        impacts = []

        components = comparison.get("components", {})
        interfaces = comparison.get("interfaces", {})
        ports = comparison.get("ports", {})
        signals = comparison.get("signals", {})
        dependencies = comparison.get("dependencies", {})

        # ------------------------------------------------------
        # Removed components
        # ------------------------------------------------------

        for component in components.get("removed", []):

            impacts.append({
                "type": "Removed Component",
                "item": component,
                "severity": "Review",
                "reason": (
                    f"Component '{component}' was removed. "
                    "Check integrations and related architecture references."
                ),
                "checks": [
                    "Component integration",
                    "Related interfaces",
                    "Related ports",
                    "Related signals",
                    "Downstream test cases"
                ]
            })

        # ------------------------------------------------------
        # Added components
        # ------------------------------------------------------

        for component in components.get("added", []):

            impacts.append({
                "type": "Added Component",
                "item": component,
                "severity": "Review",
                "reason": (
                    f"Component '{component}' was added. "
                    "Check its integration into the existing architecture."
                ),
                "checks": [
                    "Component interfaces",
                    "Required/provided ports",
                    "Dependencies",
                    "Functional flow coverage",
                    "Test coverage"
                ]
            })

        # ------------------------------------------------------
        # Removed interfaces
        # ------------------------------------------------------

        for interface in interfaces.get("removed", []):

            impacts.append({
                "type": "Removed Interface",
                "item": interface,
                "severity": "Review",
                "reason": (
                    f"Interface '{interface}' was removed. "
                    "Check components that may depend on it."
                ),
                "checks": [
                    "Connected components",
                    "Ports",
                    "Data flow",
                    "Integration tests"
                ]
            })

        # ------------------------------------------------------
        # Added interfaces
        # ------------------------------------------------------

        for interface in interfaces.get("added", []):

            impacts.append({
                "type": "Added Interface",
                "item": interface,
                "severity": "Review",
                "reason": (
                    f"Interface '{interface}' was added. "
                    "Check its connected components and ports."
                ),
                "checks": [
                    "Connected components",
                    "Ports",
                    "Data flow",
                    "Integration tests"
                ]
            })

        # ------------------------------------------------------
        # Removed ports
        # ------------------------------------------------------

        for port in ports.get("removed", []):

            impacts.append({
                "type": "Removed Port",
                "item": port,
                "severity": "Review",
                "reason": (
                    f"Port '{port}' was removed. "
                    "Check component communication and interfaces."
                ),
                "checks": [
                    "Component communication",
                    "Interfaces",
                    "Data flow"
                ]
            })

        # ------------------------------------------------------
        # Added ports
        # ------------------------------------------------------

        for port in ports.get("added", []):

            impacts.append({
                "type": "Added Port",
                "item": port,
                "severity": "Review",
                "reason": (
                    f"Port '{port}' was added. "
                    "Check its interface connection and usage."
                ),
                "checks": [
                    "Component communication",
                    "Interfaces",
                    "Data flow"
                ]
            })

        # ------------------------------------------------------
        # Removed signals
        # ------------------------------------------------------

        for signal in signals.get("removed", []):

            impacts.append({
                "type": "Removed Signal",
                "item": signal,
                "severity": "Review",
                "reason": (
                    f"Signal '{signal}' was removed. "
                    "Check consumers and producers of the signal."
                ),
                "checks": [
                    "Signal producers",
                    "Signal consumers",
                    "Data flow",
                    "Test cases"
                ]
            })

        # ------------------------------------------------------
        # Added signals
        # ------------------------------------------------------

        for signal in signals.get("added", []):

            impacts.append({
                "type": "Added Signal",
                "item": signal,
                "severity": "Review",
                "reason": (
                    f"Signal '{signal}' was added. "
                    "Check its producer, consumers and test coverage."
                ),
                "checks": [
                    "Signal producer",
                    "Signal consumers",
                    "Data flow",
                    "Test cases"
                ]
            })

        # ------------------------------------------------------
        # Removed dependencies
        # ------------------------------------------------------

        for source, target in dependencies.get("removed", []):

            impacts.append({
                "type": "Removed Dependency",
                "item": f"{source} -> {target}",
                "severity": "Review",
                "reason": (
                    f"The dependency from '{source}' to '{target}' "
                    "was removed."
                ),
                "checks": [
                    "Integration flow",
                    "Component interaction",
                    "Functional flow",
                    "Related tests"
                ]
            })

        # ------------------------------------------------------
        # Added dependencies
        # ------------------------------------------------------

        for source, target in dependencies.get("added", []):

            impacts.append({
                "type": "Added Dependency",
                "item": f"{source} -> {target}",
                "severity": "Review",
                "reason": (
                    f"A new dependency from '{source}' to '{target}' "
                    "was introduced."
                ),
                "checks": [
                    "Coupling",
                    "Integration flow",
                    "Functional flow",
                    "Related tests"
                ]
            })

        return {
            "total_impacts": len(impacts),
            "impacts": impacts
        }