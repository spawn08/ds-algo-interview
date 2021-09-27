package com.tutorials.leetcode;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

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
public class TwoSumJava {

    /**
     * Below methods finds the 2 numbers that adds upto the target given
     * @param nums array data containing integer numbers
     * @param target target value
     * @return indices of elements that adds upto target
     *
     * Time Complexity: O(n)
     * Space Complexity: O(n)
     */
    public static int[] twoSum(int[] nums, int target) {
        //initialize Map for storing the Value and Index
        Map<Integer, Integer> map = new HashMap<>();
        int difference = 0;

        //Loop through the array
        for (int index = 0; index < nums.length; index++) {
            //calculate the difference between target and array index value
            difference = target - nums[index];
            //check if difference is present in map. viz the array element
            if (map.containsKey(difference))
                return new int[]{map.get(difference), index};
            map.put(nums[index], index);

        }
        return null;
    }

    public static void main(String[] args) {
        //Sample data
        int[] data = {3,2,4};
        int[] result = twoSum(data, 6);
        System.out.println("Two Sum Result -->" + Arrays.toString(result));
    }
}
