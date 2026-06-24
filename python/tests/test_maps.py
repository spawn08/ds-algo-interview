"""Tests for the hash-map solutions."""

import importlib

import pytest


def test_max_number_of_balloons():
    mod = importlib.import_module("max_num_balloons")
    solver = mod.Solution()
    assert solver.maxNumberOfBalloons("nlaebolko") == 1
    assert solver.maxNumberOfBalloons("loonbalxballpoon") == 2
    assert solver.maxNumberOfBalloons("leetcode") == 0


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
