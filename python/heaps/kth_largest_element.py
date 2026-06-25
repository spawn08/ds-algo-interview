"""
Given an integer array nums and an integer k, return the kth largest element in the array.
Note that it is the kth largest element in the sorted order, not the kth distinct element.
Can you solve it without sorting?

Example 1:

Input: nums = [3,2,1,5,6,4], k = 2
Output: 5

Example 2:

Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4
"""

import heapq


class Solution:
    """
    Find the kth largest element using a bounded min-heap of size k.

    Why a min-heap of size k (and not sorting)?  We keep only the k largest
    elements seen so far. The heap's root is the smallest of those k, so once
    the heap exceeds size k we pop the root -- discarding an element that can
    never be the kth largest. After scanning every number, the root is exactly
    the kth largest. This beats sorting's O(n log n) and uses only O(k) memory,
    which matters when n is huge but k is small (a streaming-friendly pattern).

    Time complexity:  O(n log k) -- each of the n elements triggers a push and
                      possibly a pop, each O(log k) on a heap capped at size k.
    Space complexity: O(k) -- the heap never holds more than k elements.
    """

    def kth_largest_element(self, nums: list[int], k: int) -> int:
        '''
        The method finds kth largest element in an array using heap datastructure
        param:
            nums: list of integers
            k: kth largest element
        Time Complexity: O(nlogk)
        Space Complexity: O(k)
        '''
        if k < 0 or k > len(nums):
            raise ValueError("k is out of range")

        heap: list[int] = []

        for num in nums:
            if len(heap) < k:
                heapq.heappush(heap, num)
            elif num > heap[0]:
                heapq.heapreplace(heap, num)
        return heap[0]


if __name__ == '__main__':

    input_list = [3, 2, 3, 1, 2, 4, 5, 5, 6]
    solution = Solution()
    print(solution.kth_largest_element(input_list, 4))
    print(solution.kth_largest_element([3, 2, 1, 5, 6, 4], 2))