package com.dsalgo.strings;


/**
 * Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

For example, "ace" is a subsequence of "abcde".
A common subsequence of two strings is a subsequence that is common to both strings.
*/
public class LongestCommonSubsequence {

	public static int lcs(String text1, String text2) {
		if(text1 == null || text2 == null) return 0;

		int length1 = text1.length();
		int length2 = text2.length();
		int dp[][] = new int[length1 + 1][length2 + 1]; // + 1 is for empty Strings case

		for (int row = 1; row <= length1; row++) {
			char c1 = text1.charAt(row - 1);
			for (int col = 1; col <= length2; col++) {
				char c2 = text2.charAt(col - 1);
				if (c1 == c2) {
					dp[row][col] = 1 + dp[row - 1][col - 1];
				} else {
					dp[row][col] = Math.max(dp[row - 1][col], dp[row][col - 1]);
				}
			}
			
		}

		return dp[length1][length2];

	}

	public static void main(String[] args) {
		LongestCommonSubsequence.lcs("abcde", "ace");
		LongestCommonSubsequence.lcs("abc", "abc");
		LongestCommonSubsequence.lcs("abc", "def");
	}

}