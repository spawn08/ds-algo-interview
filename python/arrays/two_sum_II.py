
"""
Given a 1-indexed array of integers numbers that is already
sorted in non-decreasing order, find two numbers such that
they add up to a specific target number.
Let these two numbers be numbers[index1] and
numbers[index2] where 1 <= index1 < index2 <= numbers.length.
Return the indices of the two numbers index1 and index2,
each incremented by one, as an integer array [index1, index2]
of length 2.
The tests are generated such that there is exactly one
solution. You may not use the same element twice.

Your solution must use only constant extra space.
Example 1:

Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9.
Therefore, index1 = 1, index2 = 2. We return [1, 2].
Example 2:

Input: numbers = [2,3,4], target = 6
Output: [1,3]
Explanation: The sum of 2 and 4 is 6.
Therefore index1 = 1, index2 = 3. We return [1, 3].
Example 3:

Input: numbers = [-1,0], target = -1
Output: [1,2]
Explanation: The sum of -1 and 0 is -1.
Therefore index1 = 1, index2 = 2. We return [1, 2].
"""


class TwoSum:
    """
    Two-pointer scan over a sorted array.

    Time complexity:  O(n log n) -- dominated by the sort; the two-pointer
                      sweep that follows is O(n).
    Space complexity: O(n) -- Timsort's working space (O(1) extra beyond it).
    """

    def two_sum(self, nums: list, target: int) -> list[int]:
        nums.sort()
        start_index = 0
        end_index = len(nums) - 1

        while start_index < end_index:
            current_sum = nums[start_index] + nums[end_index]
            if current_sum == target:
                # If the questions asks about one based indexing
                return [start_index + 1, end_index + 1]
            elif current_sum < target:
                start_index += 1
            else:
                end_index -= 1
        return []


if __name__ == '__main__':
    input_nums = [2, 7, 11, 15]
    two_sum = TwoSum()
    print(two_sum.two_sum(input_nums, 6))
