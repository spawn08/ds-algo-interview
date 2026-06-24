"""Tests for the sliding-window solutions."""

import importlib

import pytest


def test_longest_substring_without_repeating():
    mod = importlib.import_module("lcs_without_repeating_character")
    solver = mod.LCSWithOutRepeatingChar()
    assert solver.lcs("abcabcbb") == 3
    assert solver.lcs("bbbbb") == 1
    assert solver.lcs("pwwkew") == 3
    assert solver.lcs("") == 0


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
