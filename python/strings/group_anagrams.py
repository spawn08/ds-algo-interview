from collections import defaultdict
from typing import List


class Solution:
    """
    Group words by a canonical key (their sorted characters); anagrams share
    the same key. Both methods are equivalent (str vs tuple key).

    Let n = number of words, k = max word length.
    Time complexity:  O(n * k log k) -- sorting each word dominates.
    Space complexity: O(n * k) -- every word is stored in the map.
    """

    def group_anagrams(self, strs: List[str]) -> List[List[str]]:
        anagram_map = defaultdict(list)
        for s in strs:
            sorted_word = ''.join(sorted(s))
            anagram_map[sorted_word].append(s)
        return list(anagram_map.values())

    def group_anagrams_2(self, strs: list[str]) -> list[list[str]]:
        anagram_map = defaultdict(list)
        for s in strs:
            sorted_word = tuple(sorted(s))
            anagram_map[sorted_word].append(s)
        return list(anagram_map.values())


if __name__ == '__main__':
    input_list = ["eat", "tea", "tan", "ate", "nat", "bat"]
    solution = Solution()
    print(solution.group_anagrams(input_list))
    print(solution.group_anagrams_2(input_list))
