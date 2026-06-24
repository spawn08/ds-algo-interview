
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
    """
    Fixed-size sliding window + a frequency map.

    Why a hash map (frequency counter)?  The window must contain k *distinct*
    values. A counter lets us check "are all k elements distinct?" in O(1) by
    comparing the number of unique keys to the window size, instead of
    re-scanning the window each time (which would be O(n*k)).

    Time complexity:  O(n) -- each element enters and leaves the window once.
    Space complexity: O(k) -- the frequency map holds at most k keys.
    """

    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        frequency = defaultdict(int)
        window_sum = 0
        max_sum = 0

        for right, value in enumerate(nums):
            # Grow the window by one element on the right.
            frequency[value] += 1
            window_sum += value

            # Once the window is larger than k, drop the leftmost element.
            if right >= k:
                left_value = nums[right - k]
                window_sum -= left_value
                frequency[left_value] -= 1
                if frequency[left_value] == 0:
                    del frequency[left_value]

            # A valid window has exactly k elements, all distinct.
            if right >= k - 1 and len(frequency) == k:
                max_sum = max(max_sum, window_sum)

        return max_sum


if __name__ == '__main__':
    solution = Solution()
    print(solution.maximumSubarraySum([1, 5, 4, 2, 9, 9, 9], 3))
