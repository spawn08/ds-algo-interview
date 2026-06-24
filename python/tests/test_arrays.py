"""Tests for the array solutions."""

import importlib

import pytest


def _two_sum_basic():
    mod = importlib.import_module("two_sum")
    return mod.TwoSum()


def test_two_sum_hashmap():
    solver = _two_sum_basic()
    assert solver.two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert solver.two_sum([3, 2, 4], 6) == [1, 2]
    assert solver.two_sum([3, 3], 6) == [0, 1]
    assert solver.two_sum([1, 2, 3], 7) == []


def test_two_sum_ii_sorted_two_pointer():
    mod = importlib.import_module("two_sum_II")
    solver = mod.TwoSum()
    assert solver.two_sum([2, 7, 11, 15], 9) == [1, 2]
    assert solver.two_sum([2, 3, 4], 6) == [1, 3]
    assert solver.two_sum([-1, 0], -1) == [1, 2]


def test_longest_consecutive_sequence():
    mod = importlib.import_module("longest_consecutive_sequence")
    solver = mod.Solution()
    assert solver.longestConsecutiveSequence([100, 4, 200, 1, 3, 2]) == 4
    assert solver.longestConsecutiveSequence([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert solver.longestConsecutiveSequence([]) == 0


def test_max_subarray_kadane():
    mod = importlib.import_module("max_path_sum")
    solver = mod.Solution()
    assert solver.max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert solver.max_sub_array([1]) == 1
    assert solver.max_sub_array([5, 4, -1, 7, 8]) == 23
    assert solver.max_sub_array([-1, -2, -3]) == -1


def test_max_subarray_distinct_window():
    mod = importlib.import_module("max_subarray_size_k")
    solver = mod.Solution()
    assert solver.maximumSubarraySum([1, 5, 4, 2, 9, 9, 9], 3) == 15
    assert solver.maximumSubarraySum([4, 4, 4], 3) == 0
    assert solver.maximumSubarraySum([1, 1, 1, 7, 8, 9], 3) == 24


def test_rotate_image_in_place():
    mod = importlib.import_module("rotate_image")
    solver = mod.Solution()

    m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    solver.rotate(m1)
    assert m1 == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

    m2 = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
    solver.rotate(m2)
    assert m2 == [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
