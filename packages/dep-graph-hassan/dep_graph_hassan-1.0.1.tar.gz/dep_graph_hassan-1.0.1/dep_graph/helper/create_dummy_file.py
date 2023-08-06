"""
Create dummy file with unresolved depedency graph.

"""

import json
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='DummyFileCreator',
        description='Creates a dummy unresolved graph.')
    parser.add_argument('--path', default='/tmp/deps.json',
                        help='specify complete path for dummy file.')
    args = parser.parse_args()

    deps_file_path = args.path
    dummy_data = {
        "pkg1": ["pkg2", "pkg3"],
        "pkg2": ["pkg3"],
        "pkg3": []
    }
    with open(deps_file_path, 'w', encoding='UTF-8') as deps_file:
        json.dump(dummy_data, deps_file)
