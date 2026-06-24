"""
pytest configuration for the Python solutions.

The solution files were written as standalone scripts (each module lives in a
category folder and some import a sibling like ``from tree import TreeNode``).
To import them from the test suite without restructuring the repo, we add every
category directory to ``sys.path`` so the modules resolve by their bare names.
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_ROOT = os.path.dirname(TESTS_DIR)

_CATEGORY_DIRS = [
    "arrays",
    "binary_search",
    "dynamic_programming",
    "graphs",
    "maps",
    "sliding_window",
    "strings",
    "trees",
]

for _category in _CATEGORY_DIRS:
    _path = os.path.join(PYTHON_ROOT, _category)
    if _path not in sys.path:
        sys.path.insert(0, _path)
