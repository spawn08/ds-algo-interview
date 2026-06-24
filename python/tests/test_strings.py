"""Tests for the string solutions."""

import importlib

import pytest


def test_group_anagrams():
    mod = importlib.import_module("group_anagrams")
    solver = mod.Solution()
    groups = solver.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    normalized = sorted(sorted(g) for g in groups)
    assert normalized == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]


def test_valid_anagram():
    mod = importlib.import_module("valid_anagrams")
    assert mod.valid_anagrams("anagram", "nagaram") is True
    assert mod.valid_anagrams("rat", "car") is False


def test_valid_palindrome():
    mod = importlib.import_module("valid_palindrome")
    solver = mod.Solution()
    assert solver.isPanlindrome("A man, a plan, a canal: Panama") is True
    assert solver.isPanlindrome("race a car") is False
    assert solver.isPanlindrome(" ") is True


def test_valid_parentheses():
    mod = importlib.import_module("valid_parentheses")
    solver = mod.ValidParentheses()
    assert solver.valid_parantheses("()") is True
    assert solver.valid_parantheses("()[]{}") is True
    assert solver.valid_parantheses("(]") is False
    assert solver.valid_parantheses("([])") is True
    assert solver.valid_parantheses("(") is False


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
