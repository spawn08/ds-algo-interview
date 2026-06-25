from collections import Counter

"""
Given two strings s and t, return true if t is an anagram
of s, and false otherwise.

Example 1:

Input: s = "anagram", t = "nagaram"
Output: true

Example 2:

Input: s = "rat", t = "car"
Output: false
"""


def valid_anagrams(str1: str, str2: str):
    """
    Two strings are anagrams iff they have identical character frequencies.

    Time complexity:  O(n) -- building and comparing the two counters.
    Space complexity: O(1) -- bounded by the (fixed) alphabet size, O(k) in
                      general for k distinct characters.
    """
    if len(str1) != len(str2):
        return False

    return Counter(str1) == Counter(str2)


if __name__ == '__main__':
    print(valid_anagrams("anagram", "nagaram"))
    print(valid_anagrams("rat", "car"))
