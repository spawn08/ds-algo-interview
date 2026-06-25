
"""
There is an integer array nums sorted in non-decreasing
order (not necessarily with distinct values).
Before being passed to your function, nums is rotated at
an unknown pivot index k (0 <= k < nums.length) such that
the resulting array is
[nums[k], nums[k+1], ..., nums[n-1],
 nums[0], nums[1], ..., nums[k-1]] (0-indexed).
For example, [0,1,2,4,4,4,5,6,6,7] might be rotated at
pivot index 5 and become [4,5,6,6,7,0,1,2,4,4].
Given the array nums after the rotation and an integer
target, return true if target is in nums, or false if it
is not in nums.
You must decrease the overall operation steps as much as possible.

Example 1:

Input: nums = [2,5,6,0,0,1,2], target = 0
Output: true
Example 2:

Input: nums = [2,5,6,0,0,1,2], target = 3
Output: false
"""


class Solution:
    """
    Modified binary search that also handles duplicates. When
    nums[low] == nums[mid] == nums[high] we cannot tell which half is sorted,
    so we shrink both ends by one.

    Time complexity:  O(log n) average, O(n) worst case -- duplicates (e.g.
                      [1,1,1,1,1]) force the linear low++/high-- shrink.
    Space complexity: O(1) -- only a few index variables.
    """

    def search_target(self, nums: list[int], target: int) -> bool:
        size = len(nums)
        low = 0
        high = size - 1

        while low <= high:
            mid = low + (high - low) // 2

            if nums[mid] == target:
                return mid

            if nums[mid] == nums[low] and nums[mid] == nums[high]:
                low += 1
                high -= 1
                continue

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
    nums = [7, 8, 1, 2, 3, 3, 3, 4, 5, 6]
    solution = Solution()
    print(solution.search_target(nums, 3))
