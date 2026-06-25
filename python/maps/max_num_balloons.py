"""
Given a string text, you want to use the characters of text to form as many instances of the word "balloon" as possible.
You can use each character in text at most once. Return the maximum number of instances that can be formed.

Example 1:

Input: text = "nlaebolko"
Output: 1
Example 2:

Input: text = "loonbalxballpoon"
Output: 2
Example 3:

Input: text = "leetcode"
Output: 0
"""

from collections import defaultdict

class Solution:
	"""
	Count the letters of "balloon" in text; the answer is limited by the
	scarcest letter (with 'l' and 'o' needed twice each).

	Time complexity:  O(n) -- single pass over text; the final min() is O(1).
	Space complexity: O(1) -- the counter holds at most 5 distinct letters.
	"""

	def maxNumberOfBalloons(self, text: str) -> int:

		counter = defaultdict(int)
		target = 'balloon'

		for c in text:
			if c in target:
				counter[c] += 1

		if any(c not in counter for c in target):
			return 0

		return min(counter['b'],counter['a'], counter['l']//2, counter['o']//2, counter['n'])


if __name__ == '__main__':
	solution = Solution()
	print(solution.maxNumberOfBalloons("nlaebolko"))         # 1
	print(solution.maxNumberOfBalloons("loonbalxballpoon"))  # 2
	print(solution.maxNumberOfBalloons("leetcode"))          # 0