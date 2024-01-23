package com.tutorials.leetcode.twosum;

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
 * @link <a href="https://leetcode.com/problems/two-sum/">...</a>
 */
public class TwoSumUsingPointers {

    public int[] findTwoSum(int[] input, int target) {
        Arrays.sort(input);
        int startIndex = 0;
        int endIndex = input.length - 1;
        while (startIndex < endIndex) {
            int currentSum = input[startIndex] + input[endIndex];
            if(currentSum == target) return new int[] {input[startIndex], input[endIndex]};
            else if (currentSum < target) startIndex++;
            else endIndex++;
        }

        return new int[0];
    }


    public static void main(String[] args) {
        int[] data = {3, 5, -4, 8, 11, 1, -1, 6};
        TwoSumUsingPointers twoSumUsingPointers = new TwoSumUsingPointers();
        int[] result = twoSumUsingPointers.findTwoSum(data, 10);
        System.out.println("TwoSumUsingPointers --> " + Arrays.toString(result));
    }
}
