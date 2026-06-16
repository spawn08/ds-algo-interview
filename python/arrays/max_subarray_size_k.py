
"""
You are given an integer array nums and an integer k.
Find the maximum subarray sum of all the subarrays of nums
that meet the following conditions:
The length of the subarray is k, and
All the elements of the subarray are distinct.
Return the maximum subarray sum of all the subarrays that
meet the conditions. If no subarray meets the conditions,
return 0.

A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:

Input: nums = [1,5,4,2,9,9,9], k = 3
Output: 15
Explanation: The subarrays of nums with length 3 are:
- [1,5,4] meets the requirements, sum of 10.
- [5,4,2] meets the requirements, sum of 11.
- [4,2,9] meets the requirements, sum of 15.
- [2,9,9] does not meet the requirements
  because the element 9 is repeated.
- [9,9,9] does not meet the requirements
  because the element 9 is repeated.
We return 15 because it is the maximum subarray sum
of all the subarrays that meet the conditions
Example 2:

Input: nums = [4,4,4], k = 3
Output: 0
Explanation: The subarrays of nums with length 3 are:
- [4,4,4] does not meet the requirements
  because the element 4 is repeated.
We return 0 because no subarrays meet the conditions.
"""

from collections import defaultdict
from typing import List


class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        frequency = defaultdict(int)

        return max_sum


if __name__ == '__main__':
    solution = Solution()
    print(solution.maximumSubarraySum([1, 5, 4, 2, 9, 9, 9], 3))
