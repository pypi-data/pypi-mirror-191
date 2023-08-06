import argparse
from .graph_resolver import reconstruct_full_dependency_graph
from .visualizations import CLIGraphVisualizer



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='DependencyResolver',
        description='Resolves a dependency graph.')
    parser.add_argument('--path', default='/tmp/deps.json',
                        help='specify complete path for package dependency file.')
    args = parser.parse_args()

    deps_file_path = args.path
    resolved_graph = reconstruct_full_dependency_graph(deps_file_path)
    graph_visualizer = CLIGraphVisualizer()
    graph_visualizer.visualize_dependency_graph(resolved_graph)
