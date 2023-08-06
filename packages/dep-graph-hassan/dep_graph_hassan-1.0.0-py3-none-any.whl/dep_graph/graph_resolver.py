""" Core class of module. provides DependencyResolver to resolved package dependency graphs.

    Raises:
        FileNotFoundError: raised when dependency graph file does not exist at the provided path.
        CircularDependencyException:
            raised when theres a circular dependency present inside the code.
        MissingDependencyException:
            raised when the given dependency graph has missing packages without its dependency list.

"""
import os
import json
import pathlib

from .exceptions import MissingDependencyException, CircularDependencyException
from .types import UnresolvedGraph, ResolvedGraph, PackageStates


class DependencyResolver(object):
    """DependencyResolver class to resolve package dependency graphs.

    """

    def __init__(self, deps_path: pathlib.Path):
        self.deps_path = deps_path
        self.unresolved_graph: UnresolvedGraph = {}
        self.resolved_graph: ResolvedGraph = {}

        if not os.path.exists(deps_path):
            raise FileNotFoundError(f"file at {deps_path} does not exists.")

    def _resolve_package_dependencies(self, package: str) -> ResolvedGraph:
        """Resolves the dependencies of a given package."""

        if self.resolved_graph.get(package) is None:
            self.resolved_graph[package] = {p: self._resolve_package_dependencies(
                p) for p in self.unresolved_graph[package]}

        return self.resolved_graph[package]

    def load_dependency_graph(self) -> None:
        """Loads Unresolved dependency graph from path given at object instantiation.
        """
        with open(self.deps_path, encoding='UTF-8') as deps_file:
            self.unresolved_graph = json.load(deps_file)

    def resolve_dependency_graph(self) -> ResolvedGraph:
        """Resolves the dependency graph and returns a resolved dependency graph.

        Raises:
            CircularDependencyException:
                raised when theres a circular dependency present inside the given dependency graph.

        Returns:
            ResolvedGraph: resolved dependency graph.
        """
        self.load_dependency_graph()
        if self.circular_dependency_check():
            raise CircularDependencyException(
                "Circular Dependency Found in Graph. Exiting")

        for package in self.unresolved_graph.keys():
            self.resolved_graph[package] = self._resolve_package_dependencies(
                package)

        return self.resolved_graph

    def _package_depenencies_contain_cycle(self, package: str, states: PackageStates) -> bool:
        """Checks if the given package has any circular dependencies.

        Args:
            package (str): package to check for circular dependencies.
            states (PackageStates): dictionary to keep track of package states.

        Raises:
            MissingDependencyException: 
                raised when the given package is not present in the dependency graph.

        Returns:
            bool: True if cycle is present, False otherwise.
        """
        if package not in states:
            states[package] = 'resolving'

            if package not in self.unresolved_graph.keys():
                raise MissingDependencyException()

            for deps in self.unresolved_graph[package]:
                if self._package_depenencies_contain_cycle(deps, states):
                    return True
            states[package] = 'resolved'

        if states[package] == 'resolved':
            return False
        if states[package] == 'resolving':
            return True

        return False

    def circular_dependency_check(self) -> bool:
        """Checks if the given dependency graph has any circular dependencies.

        Returns:
            bool: True if circular dependency is present, False otherwise.
        """
        states: PackageStates = {}
        for package in self.unresolved_graph:
            if self._package_depenencies_contain_cycle(package, states):
                return True
        return False
