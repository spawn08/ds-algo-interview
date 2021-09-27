package com.tutorials.leetcode;

import java.util.HashSet;
import java.util.Set;

/**
 * Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.
 * <p>
 * Example:
 * 1. Input: nums = [1,2,3,1]
 * Output: true
 * <p>
 * 2. Input: nums = [1,2,3,4]
 * Output: false
 *
 * @link https://leetcode.com/problems/contains-duplicate/
 */
public class ContainsDuplicate {

    /**
     * The below method checks whether the integer array contains duplicate
     *
     * @param nums integer array
     * @return true if contains duplicate else false
     *
     * Time Complexity: O(n)
     * Space Complexity: O(n)
     */
    public static boolean containsDuplicate(int[] nums) {
        //Initialize set datastructure
        Set<Integer> values = new HashSet<>();
        boolean containsDuplicate = false;
        //Loop through each value
        for (int num : nums) {
            //check whether values set contains num value.
            // If it does, return true else add this num to set.
            if (values.contains(num))
                containsDuplicate = true;

            else values.add(num);
        }

        return containsDuplicate;
    }

    public static void main(String[] args) {
        int[] data = {1, 2, 3, 4};
        boolean containsDuplicate = containsDuplicate(data);
        System.out.println("Does data array contains duplicate? -> " + containsDuplicate);
    }
}
