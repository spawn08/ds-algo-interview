from typing import Dict


class LCSWithOutRepeatingChar:

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
