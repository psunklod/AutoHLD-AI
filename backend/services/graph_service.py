from graphviz import Digraph


class GraphService:
    """
    Build a visual dependency graph from extracted HLD dependencies.
    """

    def create_dependency_graph(self, dependencies: list[dict]) -> Digraph:
        graph = Digraph("AUTOSAR Dependency Graph")

        graph.attr(
            rankdir="LR",
            splines="ortho"
        )

        graph.attr(
            "node",
            shape="box"
        )

        for dependency in dependencies:
            source = dependency["source"]
            target = dependency["target"]

            graph.node(source)
            graph.node(target)

            graph.edge(
                source,
                target
            )

        return graph