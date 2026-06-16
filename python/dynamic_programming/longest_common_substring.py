class Solution:
    def longestCommonSubstring(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)

        max_length = 0
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                    max_length = max(max_length, dp[i][j])
                else:
                    dp[i][j] = 0

        return max_length
