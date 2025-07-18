package com.tutorials.leetcode.valid_parantheses;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
 * <p>
 * An input string is valid if:
 * <p>
 * 1. Open brackets must be closed by the same type of brackets.
 * 2. Open brackets must be closed in the correct order.
 * <p>
 * Examples:
 * 1. Input: s = "()"
 * Output: true
 * <p>
 * 2. Input: s = "([)]"
 * Output: false
 *
 * @link <a href="https://leetcode.com/problems/valid-parentheses/">...</a>
 */
public class ValidParantheses {

    public static void main(String[] args) {
        String s = "()";
        System.out.println("Valid parentheses using Stacks? -> " + checkValidParenthesesUsingStack(s));
        System.out.println("Valid parentheses using Arrays? -> " + checkValidParentheses(s));
    }

    /**
     * Method checks whether the given string has valid parentheses or not.
     *
     * @param s input string
     * @return true is parentheses occurrence is as per question
     */
    public static boolean checkValidParentheses(String s) {
        //Check whether String length is even, if not return false
        //Why are we doing this? If it's a valid parentheses then string's length will always be even.
        if (s.length() % 2 != 0)
            return false;
        //initialize char array with size equals to string length
        char[] stack = new char[s.length()];
        // initialize head
        int head = 0;
        for (char c : s.toCharArray()) {
            switch (c) {
                case '{':
                case '[':
                case '(':
                    stack[head++] = c;
                    break;
                case '}':
                    if (head == 0 || stack[--head] != '{') return false;
                    break;
                case ')':
                    if (head == 0 || stack[--head] != '(') return false;
                    break;
                case ']':
                    if (head == 0 || stack[--head] != '[') return false;
                    break;
            }
        }
        return head == 0;
    }

    public static boolean checkValidParenthesesUsingStack(String s) {
        //Check whether String length is even, if not return false
        //Why are we doing this? If it's a valid parentheses then string's length will always be even.
        if (s.length() % 2 != 0)
            return false;
        //initialize stack
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            switch (c) {
                case '{':
                case '[':
                case '(':
                    stack.push(c);
                    break;
                case '}':
                    if (stack.isEmpty() || stack.pop() != '{') return false;
                    break;
                case ')':
                    if (stack.isEmpty() || stack.pop() != '(') return false;
                    break;
                case ']':
                    if (stack.isEmpty() || stack.pop() != '[') return false;
                    break;
            }
        }
        return stack.isEmpty();
    }
}
