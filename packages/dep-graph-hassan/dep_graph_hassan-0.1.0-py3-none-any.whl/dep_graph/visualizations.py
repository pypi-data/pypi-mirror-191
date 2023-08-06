
""" Visualization Tools.
"""

from .types import ResolvedGraph

class CLIGraphVisualizer(object):
    """
    Class to visualize a resolved dependency graph to stdout.

    """

    def _visualize_package(self, package: str, depth: int, resolved_graph: ResolvedGraph) -> None:
        print(f"{depth * '  '}- {package}")

        for package in sorted(resolved_graph.keys()):
            self._visualize_package(package, depth + 1, resolved_graph[package])


    def visualize_dependency_graph(self, resolved_graph: ResolvedGraph) -> None:
        """ prints resolved dependency graph to stdout.

        Args:
            resolved_graph (ResolvedGraph): A resolved package dependency graph
        """
        for package in sorted(resolved_graph.keys()):
            self._visualize_package(package, 0, resolved_graph[package])
