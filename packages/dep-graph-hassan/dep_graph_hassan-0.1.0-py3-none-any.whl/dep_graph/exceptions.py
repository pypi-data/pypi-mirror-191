
class CircularDependencyException(Exception):
    """Exception raised when theres a circular dependency present inside the given dependency graph.

    """


class MissingDependencyException(Exception):
    """Exception raised when theres a missing dependency present inside the given dependency graph.
    """
