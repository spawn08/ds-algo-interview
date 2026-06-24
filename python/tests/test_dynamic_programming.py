"""Tests for the dynamic-programming solutions."""

import importlib

import pytest


def test_house_robber():
    mod = importlib.import_module("house_robber")
    solver = mod.Solution()
    assert solver.rob([1, 2, 3, 1]) == 4
    assert solver.rob([2, 7, 9, 3, 1]) == 12
    assert solver.rob([]) == 0
    assert solver.rob([5]) == 5


def test_longest_common_subsequence():
    mod = importlib.import_module("longest_common_sequence")
    solver = mod.Solution()
    assert solver.longestCommonSubsequence("abcde", "ace") == 3
    assert solver.longestCommonSubsequence("abc", "abc") == 3
    assert solver.longestCommonSubsequence("abc", "def") == 0


def test_longest_common_substring():
    mod = importlib.import_module("longest_common_substring")
    solver = mod.Solution()
    assert solver.longestCommonSubstring("abcde", "abfce") == 2  # "ab"
    assert solver.longestCommonSubstring("ABABC", "BABCA") == 4  # "BABC"
    assert solver.longestCommonSubstring("abc", "def") == 0


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
