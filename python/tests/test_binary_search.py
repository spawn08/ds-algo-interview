"""Tests for the binary-search solutions."""

import importlib

import pytest


def test_search_rotated_sorted_array():
    mod = importlib.import_module("rotated_sorted_array")
    solver = mod.Solution()
    assert solver.search_target([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert solver.search_target([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert solver.search_target([1], 0) == -1
    assert solver.search_target([4, 5, 6, 7, 0, 1, 2], 4) == 0


def test_search_rotated_sorted_array_with_duplicates():
    mod = importlib.import_module("rotated_sorted_array_ii")
    solver = mod.Solution()
    # returns the index when found (truthy) and -1 when not found.
    assert solver.search_target([2, 5, 6, 0, 0, 1, 2], 0) != -1
    assert solver.search_target([2, 5, 6, 0, 0, 1, 2], 3) == -1
    assert solver.search_target([1, 0, 1, 1, 1], 0) != -1


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
