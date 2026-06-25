class Solution:
    """
    2-D DP where dp[i][j] is the length of the common substring ending exactly
    at text1[i-1] and text2[j-1]; resets to 0 on a mismatch.

    Time complexity:  O(m * n) -- every cell of the table is filled once.
    Space complexity: O(m * n) -- the full table (reducible to O(min(m, n))
                      with a rolling row).
    """

    def longestCommonSubstring(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)

        max_length = 0
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                    max_length = max(max_length, dp[i][j])
                else:
                    dp[i][j] = 0

        return max_length


if __name__ == '__main__':
    solution = Solution()
    print(solution.longestCommonSubstring("ABABC", "BABCA"))  # 4  -> "BABC"
    print(solution.longestCommonSubstring("abcde", "abfce"))  # 2  -> "ab"
    print(solution.longestCommonSubstring("abc", "def"))      # 0
