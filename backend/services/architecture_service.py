import re


class ArchitectureService:
    """
    Extract basic architecture entities from HLD text.

    Prototype entities:
    - Software Components
    - Interfaces
    - Ports
    - Signals
    - Dependencies

    The extractor is intentionally conservative.
    It reports information explicitly identifiable in the text.
    """

    def __init__(self):
        self.patterns = {
            "components": [
                r"Software\s+Component\s*:\s*([A-Za-z0-9_.-]+)",
                r"SW\s+Component\s*:\s*([A-Za-z0-9_.-]+)",
                r"Component\s*:\s*([A-Za-z0-9_.-]+)",
            ],
            "interfaces": [
                r"Software\s+Interface\s*:\s*([A-Za-z0-9_.-]+)",
                r"Interface\s*:\s*([A-Za-z0-9_.-]+)",
            ],
            "ports": [
                r"Port\s*:\s*([A-Za-z0-9_.-]+)",
                r"Port\s+Name\s*:\s*([A-Za-z0-9_.-]+)",
            ],
            "signals": [
                r"Signal\s*:\s*([A-Za-z0-9_.-]+)",
                r"Signal\s+Name\s*:\s*([A-Za-z0-9_.-]+)",
            ],
        }

    @staticmethod
    def _extract_names(text: str, patterns: list[str]) -> set[str]:
        names = set()

        for pattern in patterns:
            matches = re.findall(
                pattern,
                text,
                re.IGNORECASE
            )

            for name in matches:
                cleaned = name.strip()

                if cleaned:
                    names.add(cleaned)

        return names

    def extract(self, pages: list[dict]) -> dict:
        components = set()
        interfaces = set()
        ports = set()
        signals = set()
        dependencies = []

        for page in pages:
            text = page["text"]
            page_number = page["page"]

            components.update(
                self._extract_names(
                    text,
                    self.patterns["components"]
                )
            )

            interfaces.update(
                self._extract_names(
                    text,
                    self.patterns["interfaces"]
                )
            )

            ports.update(
                self._extract_names(
                    text,
                    self.patterns["ports"]
                )
            )

            signals.update(
                self._extract_names(
                    text,
                    self.patterns["signals"]
                )
            )

            # Examples:
            # Dependency: EngineControl -> EngineStatus
            # Dependency: ComponentA -> ComponentB
            dependency_matches = re.findall(
                r"Dependency\s*:\s*"
                r"([A-Za-z0-9_.-]+)"
                r"\s*(?:->|→|to)\s*"
                r"([A-Za-z0-9_.-]+)",
                text,
                re.IGNORECASE,
            )

            for source, target in dependency_matches:
                dependencies.append({
                    "source": source.strip(),
                    "target": target.strip(),
                    "page": page_number,
                })

        return {
            "components": sorted(components),
            "interfaces": sorted(interfaces),
            "ports": sorted(ports),
            "signals": sorted(signals),
            "dependencies": dependencies,
        }