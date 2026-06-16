
"""
There is an integer array nums sorted in ascending order
(with distinct values).
Prior to being passed to your function, nums is possibly
left rotated at an unknown index k (1 <= k < nums.length)
such that the resulting array is
[nums[k], nums[k+1], ..., nums[n-1],
 nums[0], nums[1], ..., nums[k-1]] (0-indexed).
For example, [0,1,2,4,5,6,7] might be left rotated by
3 indices and become [4,5,6,7,0,1,2].
Given the array nums after the possible rotation and an
integer target, return the index of target if it is in
nums, or -1 if it is not in nums.
You must write an algorithm with O(log n) runtime
complexity.

Example 1:

Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4
Example 2:

Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1
Example 3:

Input: nums = [1], target = 0
Output: -1
"""


class Solution:

    def search_target(self, nums: list[int], target: int) -> bool:
        size = len(nums)
        low = 0
        high = size - 1

        while low <= high:
            mid = low + (high - low) // 2

            if nums[mid] == target:
                return mid

            # case 1: The left half is sorted
            if nums[low] <= nums[mid]:
                if nums[low] <= target < nums[mid]:
                    high = mid - 1
                else:
                    low = mid + 1

            # case 2: The right half is sorted
            else:
                # Check if the target lies within this sorted right half
                if nums[mid] < target <= nums[high]:
                    low = mid + 1
                else:
                    high = mid - 1
        return -1


if __name__ == '__main__':
    nums = [4, 5, 6, 7, 0, 1, 2]
    solution = Solution()
    print(solution.search_target(nums, 4))
