from typing import Dict


class LCSWithOutRepeatingChar:
    """
    Longest substring without repeating characters via a sliding window;
    last_seen jumps the left edge past any repeated character.

    Time complexity:  O(n) -- each index is visited once by the right pointer.
    Space complexity: O(min(n, c)) -- last_seen holds at most one entry per
                      distinct character (c = size of the character set).
    """

    def lcs(self, input_str: str) -> int:
        if not input_str:
            return 0

        left = 0
        max_length = 0
        last_seen: Dict[str, int] = {}

        for right in range(len(input_str)):
            char = input_str[right]

            if char in last_seen and last_seen[char] >= left:
                left = last_seen[char] + 1

            last_seen[char] = right
            max_length = max(max_length, right - left + 1)

        return max_length


if __name__ == '__main__':
    solver = LCSWithOutRepeatingChar()
    print(solver.lcs("abcabcbb"))  # 3  -> "abc"
    print(solver.lcs("bbbbb"))     # 1  -> "b"
    print(solver.lcs("pwwkew"))    # 3  -> "wke"
