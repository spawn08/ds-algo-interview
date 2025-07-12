package com.tutorials.leetcode.maxsubarraysum;

/**
 * Given an array of integers Arr of size N and a number K. Return the maximum sum of a subarray of size K.
 * NOTE*: A subarray is a contiguous part of any given array.
 * <p>
 * Example 1:
 * Input:
 * N = 4, K = 2
 * Arr = [100, 200, 300, 400]
 * Output:
 * 700
 * Explanation:
 * Arr3  + Arr4 =700, which is maximum.
 * <p>
 * Example 2:
 * Input:
 * N = 4, K = 4
 * Arr = [100, 200, 300, 400]
 * Output:
 * 1000
 * Explanation:
 * Arr1 + Arr2 + Arr3 + Arr4 =1000,
 * which is maximum.
 */
public class MaximumSumSubArrayWithK {

    /**
     * The function calculates the maximum sum of a subarray with length n and window size k
     * The function uses sliding window technique to calculate the maximum sum of a subarray.
     *
     * @param arr input arrau
     * @param k   window size
     * @param n   length of the array
     * @return maxValue returns maximum sum value
     */
    public int maximumSumSubArray(int[] arr, int k, int n) {
        int maxValue = Integer.MIN_VALUE;
        int currentSum = 0;

        for (int index = 0; index < n; index++) {
            currentSum += arr[index];
            if (index >= k - 1) {
                maxValue = Math.max(currentSum, maxValue);
                currentSum -= arr[index - (k - 1)];
            }
            if (currentSum < 0) currentSum = 0;
        }

        return maxValue;
    }

    public static void main(String[] args) {
        int[] input = {100, 200, 300, -1001, 400};
        int n = input.length;
        int k = 4;
        MaximumSumSubArrayWithK maximumSumSubArrayWithK = new MaximumSumSubArrayWithK();
        System.out.println(maximumSumSubArrayWithK.maximumSumSubArray(input, k, n));
    }
}
