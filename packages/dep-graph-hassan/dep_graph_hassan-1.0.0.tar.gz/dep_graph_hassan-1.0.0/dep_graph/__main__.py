import argparse
from .graph_resolver import DependencyResolver
from .visualizations import CLIGraphVisualizer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='DependencyResolver',
        description='Resolves a dependency graph.')
    parser.add_argument('--path', default='/tmp/deps.json',
                        help='specify complete path for package dependency file.')
    args = parser.parse_args()

    deps_file_path = args.path
    dependency_resolver = DependencyResolver(deps_file_path)
    resolved_graph = dependency_resolver.resolve_dependency_graph()
    graph_visualizer = CLIGraphVisualizer()
    graph_visualizer.visualize_dependency_graph(resolved_graph)
