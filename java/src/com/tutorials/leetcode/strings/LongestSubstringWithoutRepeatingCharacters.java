package com.tutorials.leetcode.strings;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

/**
 * Given a string s, find the length of the longest substring without duplicate characters.
 * <p>
 * Example 1:
 * Input: s = "abcabcbb"
 * Output: 3
 * Explanation: The answer is "abc", with the length of 3.
 * <p>
 * Example 2:
 * Input: s = "bbbbb"
 * Output: 1
 * Explanation: The answer is "b", with the length of 1.
 * Example 3:
 * <p>
 * Input: s = "pwwkew"
 * Output: 3
 * Explanation: The answer is "wke", with the length of 3.
 * Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
 */
public class LongestSubstringWithoutRepeatingCharacters {

    public static void longestSubstringSet(String s) {
        int maxLength = 0;
        int startIndex = 0;
        Set<Character> charMap = new HashSet<>();

        for (int endIndex = 0; endIndex < s.length(); endIndex++) {
            char currentChar = s.charAt(endIndex);
            while (charMap.contains(currentChar)) {
                charMap.remove(s.charAt(startIndex));
                startIndex++;
            }

            charMap.add(currentChar);
            maxLength = Math.max(maxLength, endIndex - startIndex + 1);
        }

        System.out.println(maxLength);
    }

    public static void longestSubstringMap(String s) {
        int startIndex = 0;
        int maxLength = 0;
        HashMap<Character, Integer> charMap = new HashMap<>(256);

        for (int endIndex = 0; endIndex < s.length(); endIndex++) {
            char currentChar = s.charAt(endIndex);
            if (charMap.containsKey(currentChar) && charMap.get(currentChar) >= startIndex) {
                startIndex = charMap.get(currentChar) + 1;
            }

            charMap.put(currentChar, endIndex);
            maxLength = Math.max(maxLength, endIndex - startIndex + 1);
        }

        System.out.println(maxLength);
    }

    // most optimal approach compared to above 2 approaches
    public static void longestSubstringArray(String s) {
        int startIndex = 0;
        int maxLength = 0;

        int[] charIndex = new int[256];
        for (int i = 0; i < 256; i++) {
            charIndex[i] = -1;
        }

        for (int endIndex = 0; endIndex < s.length(); endIndex++) {
            char currentChar = s.charAt(endIndex);
            if (charIndex[currentChar] >= startIndex) {
                startIndex = charIndex[currentChar] + 1;
            }

            charIndex[currentChar] = endIndex;
            maxLength = Math.max(maxLength, endIndex - startIndex + 1);
        }
        System.out.println(maxLength);
    }

    public static void main(String[] args) {
        String test1 = "pwwkew";
        LongestSubstringWithoutRepeatingCharacters.longestSubstringSet(test1);
        LongestSubstringWithoutRepeatingCharacters.longestSubstringMap(test1);
        LongestSubstringWithoutRepeatingCharacters.longestSubstringArray(test1);
    }
}
