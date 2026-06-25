"""
Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

Example 1:

Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]

Example 2:

Input: nums = [1], k = 1
Output: [1]

Example 3:

Input: nums = [1,2,1,2,1,2,3,1,3,2], k = 2
Output: [1,2]
"""

from typing import List
from collections import Counter
import heapq


class Solution:
	"""
	Return the k most frequent elements using a frequency map + a bounded heap.

	Count occurrences with Counter, then let heapq.nlargest pick the k keys with
	the highest counts. Under the hood nlargest keeps a min-heap of size k over
	the distinct values, so it never sorts the whole frequency map.

	Let n = len(nums) and m = number of distinct values (m <= n).
	Time complexity:  O(n + m log k) -- O(n) to count, O(m log k) for nlargest
	                  to scan m keys against a size-k heap.
	Space complexity: O(n) -- the Counter stores up to m <= n entries, plus the
	                  O(k) heap and output.
	"""

	def topKFrequent(self, nums: List[int], k: int) -> List[int]:
		if k == len(nums):
			return nums
		counter = Counter(nums)
		return heapq.nlargest(k, counter.keys(), key=counter.get)


if __name__ == '__main__':
	input_list = [1, 1, 1, 2, 2, 3]
	solution = Solution()
	print(solution.topKFrequent(input_list, 2))
	print(solution.topKFrequent([1], 1))
	print(solution.topKFrequent([1, 2, 1, 2, 1, 2, 3, 1, 3, 2], 2))