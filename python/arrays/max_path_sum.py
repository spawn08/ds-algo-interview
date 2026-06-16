"""
Given an integer array nums, find the subarray with the
largest sum, and return its sum.

Example 1:

Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.
Example 2:

Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.
Example 3:

Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.
"""

from typing import List


class Solution:
    """
    Time complexity: O(n)
    Space Complexity: O(1)
    """
    def max_sub_array(self, nums: List[int]) -> int:
        current_sum = nums[0]
        max_sum = nums[0]

        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)

        return max_sum


if __name__ == '__main__':
    solution = Solution()
    print(solution.max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
    print(solution.max_sub_array([5, 4, -1, 7, 8]))
