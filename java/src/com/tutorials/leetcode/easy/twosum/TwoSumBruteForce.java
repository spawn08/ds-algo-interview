package com.tutorials.leetcode.easy.twosum;

import java.util.Arrays;

/**
 * Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
 * You may assume that each input would have exactly one solution, and you may not use the same element twice.
 * You can return the answer in any order.
 * <p>
 * Example:
 * 1. Input: nums = [2,7,11,15], target = 9
 * Output: [0,1]
 * Output: Because nums[0] + nums[1] == 9, we return [0, 1].
 *
 * @link https://leetcode.com/problems/two-sum/
 */
public class TwoSumBruteForce {

    /**
     * Below methods finds the 2 numbers that adds upto the target given using brute force solution
     * The idea is we loop through the entire using 2 for loops where first loop will start from ith index and
     * second loop start from i+1 index.
     *
     * @param nums   array data containing integer numbers
     * @param target target value
     * @return indices of elements that adds upto target
     * <p>
     * Time Complexity: O(n^2)
     * Space Complexity: O(1)
     */
    public int[] twoSumBruteForce(int[] nums, int target) {
        //Loop through an array starting from 0th index
        for (int i = 0; i < nums.length - 1; i++) {
            // Get the number at ith index
            int firstNumber = nums[i];
            // Inner Loop: Loop through the rest of the array
            for (int j = i + 1; j < nums.length; j++) {
                int secondNumber = nums[j];
                // Check if 2 number sums to the target
                if (firstNumber + secondNumber == target) return new int[]{i, j};
            }
        }

        return null;
    }

    public static void main(String[] args) {
        int[] inputData = {4, 6};
        TwoSumBruteForce twoSumBruteForce = new TwoSumBruteForce();
        int[] result = twoSumBruteForce.twoSumBruteForce(inputData, 10);
        System.out.println("Two Sum Bruteforce Result -->" + Arrays.toString(result));
    }
}
