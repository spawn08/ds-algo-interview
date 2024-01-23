package com.tutorials.problems;

/**
 * There are two wooden sticks of lengths A and B respectively. Each of them can be cut into shorter sticks of integer lengths. Our goal is to construct the largest possible square. In order to do this, we want to cut the sticks in such a way as to achieve four sticks of the same length (note that there can be some leftover pieces). What is the longest side of square that we can achieve?
 * Write a function:
 * def solution (A, B)
 * that, given two integers A, B, returns the side length of the largest square that we can obtain. If it is not possible to create any square, the function should return 0.
 * Examples:
 * 1. Given A = 10, B = 21, the function should return 7. We can split the second stick into three sticks of length 7 and shorten the first stick by 3.
 * 2. Given A = 13, B = 11, the function should return 5. We can cut two sticks of length 5 from each of the given sticks.
 * 3. Given A = 2, B = 1, the function should return 0. It is not possible to make any square from the given sticks.
 * 4. Given A = 1, B = 8, the function should return 2. We can cut stick B into four parts.
 * Write an efficient algorithm for the following assumptions:
 * A and B are integers within the range.
 */
public class WoodenSticksProblem {
    static int countPieces(int length, int stick1, int stick2) {
        return stick1 / length + stick2 / length;
    }

    static boolean canFormSquare(int length, int stick1, int stick2) {
        return countPieces(length, stick1, stick2) >= 4;
    }

    public static int solution(int A, int B) {
        // original code had: Math.min(A, B) instead of (A+B)/4. Possible solution could also be
        // to use Math.max(A, B) which is less optimized as compared to (A+B)/4
        for (int length = Math.max(A, B); length > 0; length--) {
            if (canFormSquare(length, A, B)) {
                return length;
            }
        }
        return 0;
    }

    public static void main(String[] args) {
        //Test cases:
        //A = 13, B = 11; A = 10, B = 21; A = 1, B = 8; A = 1, B = 2; A = 22, B = 2
        System.out.println(WoodenSticksProblem.solution(1, 8));
    }
}
