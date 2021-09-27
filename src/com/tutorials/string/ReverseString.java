package com.tutorials.string;

import java.util.Stack;

/**
 * You are given a string s. You need to reverse the string.
 * Ex. 1:
 * Input:
 * s = Geeks
 * Output: skeeG
 *
 * Ex.2:
 * Input:
 * s = for
 * Output: rof
 *
 * @link https://practice.geeksforgeeks.org/problems/reverse-a-string/
 */
public class ReverseString {

    /**
     * Method revers the string for given string input
     * @param s String input
     * @return Reversed String
     *
     * Time Complexity: O(n)
     * Space Complexity: O(n) why? we are storing the string character in chars array
     */
    public static String reverseString(String s) {
        //conver string to chars
        char[] chars = s.toCharArray();
        //initialize start index
        int startIndex = 0;
        StringBuilder
        //loop through char array and perform swap
        for (int index = chars.length - 1; index>=0; index--) {
            //get the last element from the char array
            char c = chars[index];
            //swap the last char with first char
            chars[index] = chars[startIndex];
            chars[startIndex] = c;

            //increment start index
            startIndex++;

            //This is important
            // If startIndex becomes greater than or equal to index then terminate loop.
            // once the startIndex  becomes equal to index, it means we have traversed the entire string.
            if (startIndex >= index)
                break;
        }

        return new String(chars);
    }

    public static void main(String[] args) {
        String testString = "Hola";
        System.out.println("Reversed String -->" + reverseString(testString));
    }
}
