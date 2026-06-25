"""
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. 
Alphanumeric characters include letters and numbers.
<link>https://leetcode.com/problems/valid-palindrome/description/</link>

Given a string s, return true if it is a palindrome, or false otherwise.

Example 1:

Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.
Example 2:

Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.
Example 3:

Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.
"""


class Solution:
	"""
	Strip non-alphanumerics, lowercase, then two-pointer compare ends inward.

	Time complexity:  O(n) -- one pass to clean, one pass to compare.
	Space complexity: O(n) -- the cleaned string (O(1) is possible by
	                  two-pointering over the original and skipping in place).
	"""

	def isPanlindrome(self, s: str) -> bool:
		cleaned = "".join(char.lower() for char in s if char.isalnum())
		start_index = 0
		end_index = len(cleaned) - 1

		while start_index < end_index:
			if cleaned[start_index] != cleaned[end_index]:
				return False
			start_index += 1
			end_index -= 1
		return True

if __name__ == '__main__':
	input_string = "A man, a plan, a canal: Panama"
	solution = Solution()
	print(solution.isPanlindrome(input_string))