# dep_graph

[![PyPI version](https://badge.fury.io/py/dep_graph.svg)](https://pypi.org/project/dep_graph_hassan/)

A simple Python package for generating resolved dependency graphs from JSON files.

## Running the Module

To run the module, use the following command:

    python -m dep_graph

By default, the module will read the dependencies from `/tmp/deps.json`.

To specify a different path to the dependencies, use the following command:

    python -m dep_graph  --path ./some_fir/deps.json

## Creating a Dummy Dependency JSON File

To create a dummy dependency JSON file, use the following command:

    python dep_graph/helper/create_dummy_file.py --path ./tests test_file.json

 By default it outputs to `/tmp/deps.json`
  
## Running Tests

To run the tests, use the following command:

    python -m unittest discover tests/

## Building the Package

You can build the package using either poetry or setup.py.

### Method 1: Using Poetry

To build the package using poetry, use the following commands:

1. Create a virtual environment:

        poetry install

2. Build the package:

        poetry build

### Method 2: Using setup.py

To build the package using setup.py, use the following command:

        python setup.py sdist bdist_wheel

## Installing Pre-commit Hooks

To install pre-commit hooks, use the following command:

    pre-commit install
