class ComparisonService:
    """
    Compare two extracted AUTOSAR HLD architecture structures.
    """

    def _compare_lists(
        self,
        old_items: list[str],
        new_items: list[str]
    ) -> dict:

        old_set = set(old_items)
        new_set = set(new_items)

        return {
            "added": sorted(new_set - old_set),
            "removed": sorted(old_set - new_set),
            "unchanged": sorted(old_set & new_set)
        }

    def _dependency_key(self, dependency: dict) -> tuple:
        return (
            dependency["source"],
            dependency["target"]
        )

    def compare(
        self,
        old_architecture: dict,
        new_architecture: dict
    ) -> dict:

        result = {
            "components": self._compare_lists(
                old_architecture.get("components", []),
                new_architecture.get("components", [])
            ),

            "interfaces": self._compare_lists(
                old_architecture.get("interfaces", []),
                new_architecture.get("interfaces", [])
            ),

            "ports": self._compare_lists(
                old_architecture.get("ports", []),
                new_architecture.get("ports", [])
            ),

            "signals": self._compare_lists(
                old_architecture.get("signals", []),
                new_architecture.get("signals", [])
            ),

            "dependencies": {
                "added": [],
                "removed": [],
                "unchanged": []
            }
        }

        old_dependencies = {
            self._dependency_key(dep)
            for dep in old_architecture.get(
                "dependencies", []
            )
        }

        new_dependencies = {
            self._dependency_key(dep)
            for dep in new_architecture.get(
                "dependencies", []
            )
        }

        result["dependencies"]["added"] = sorted(
            new_dependencies - old_dependencies
        )

        result["dependencies"]["removed"] = sorted(
            old_dependencies - new_dependencies
        )

        result["dependencies"]["unchanged"] = sorted(
            old_dependencies & new_dependencies
        )

        return result