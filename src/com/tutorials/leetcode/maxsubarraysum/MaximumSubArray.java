package com.tutorials.leetcode.maxsubarraysum;

/**
 * Given an integer array nums, find the subarray with the largest sum, and return its sum.
 * Example 1:
 * Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
 * Output: 6
 * Explanation: The subarray [4,-1,2,1] has the largest sum 6.
 * -------------------------------------
 * Example 2:
 * Input: nums = [1]
 * Output: 1
 * Explanation: The subarray [1] has the largest sum 1.
 * -------------------------------------
 * Constraints:
 * 1 <= nums.length <= 105
 * -104 <= nums[i] <= 104
 */
public class MaximumSubArray {

    /**
     * Below method returns the maximum value sum for the subarray on contiguous location
     *
     * @param array input array
     * @return maxValue returns the maximum value for the contiguous subarray
     */
    public int findMaxSubArray(int[] array) {
        int maxValue = Integer.MIN_VALUE;
        int currentSum = 0;

        for (int j : array) {
            currentSum += j;
            maxValue = Math.max(currentSum, maxValue);

            if (currentSum < 0) currentSum = 0;
        }

        return maxValue;
    }

    public static void main(String[] args) {
        MaximumSubArray maximumSubArray = new MaximumSubArray();
        int[] nums = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        System.out.println(maximumSubArray.findMaxSubArray(nums));
    }
}
