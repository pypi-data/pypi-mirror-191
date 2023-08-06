"""Types for the dependency graph.
"""
import typing

UnresolvedGraph = typing.Dict[str, typing.List[str]]

ResolvedGraph = typing.Dict[str, typing.Dict[str, 'ResolvedGraph']]

PackageStates = typing.Dict[str, typing.Literal["resolving", "resolved"]]
