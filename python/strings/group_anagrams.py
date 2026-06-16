from collections import defaultdict
from typing import List


class Solution:

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
