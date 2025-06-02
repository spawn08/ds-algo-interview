package com.tutorials.datastructures.arrays;

/**
 * You are given an array of N positive integers and integer K. Your task is to find
 * and return the length of the smallest possible special subarray. If no special subarray is possible then return -1.
 * <p>
 * A Special subarray is one having a bitwise OR of all its elements greater than or equal to an integer K.
 * {@link - https://www.geeksforgeeks.org/smallest-subarray-such-that-its-bitwise-or-is-at-least-k/}
 */
public class SubarrayOR {

    /**
     * Bruteforce solution with time complexity of O(n^2)
     *
     * @param input input array
     * @param k     target k
     * @return minimum of length of subarray
     */
    public static int findLengthOfSmallestSubarrayBruteForce(int[] input, int k) {
        int minLength = Integer.MAX_VALUE;
        int n = input.length;

        for (int start = 0; start < n; start++) {
            int or = 0;
            for (int end = start; end < n; end++) {
                or |= input[end];
                if (or >= k) {
                    minLength = Math.min(minLength, end - start + 1);
                    break;
                }
            }
        }

        return minLength == Integer.MAX_VALUE ? -1 : minLength;
    }

    /**
     * Optimal solution for finding length of smallest special subarray
     *
     * @param input input array
     * @param k     target k
     */
    public static int findLengthOfSmallestSubarrayOptimal(int[] input, int k) {
        int size = input.length;
        int minLength = size + 1;
        int currentOr = 0;
        int[] bitCount = new int[32];
        int left = 0;

        for (int right = 0; right < size; right++) {
            currentOr |= input[right];
            updateBitCount(bitCount, input[right], true);
            // Try to shrink the window from the left as long as OR is valid
            while (left <= right && currentOr >= k) {
                // Update minimum subarray length
                minLength = Math.min(minLength, right - left + 1);

                // Remove nums[left] from the window
                updateBitCount(bitCount, input[left], false);
                currentOr = rebuildOR(bitCount);
                left++;
            }
        }

        return  minLength == size + 1 ? -1 : minLength;
    }

    private static void updateBitCount(int[] bitCount, int num, boolean add) {
        for (int i = 0; i < 32; i++) {
            int mask = 1 << i;
            if ((num & mask) != 0) {
                bitCount[i] += add ? 1 : -1;
            }
        }
    }

    private static int rebuildOR(int[] bitCount) {
        int result = 0;
        for (int i = 0; i < 32; i++) {
            if (bitCount[i] > 0) {
                result |= (1 << i);
            }
        }
        return result;
    }

    public static void main(String[] args) {
        int[] data = {1, 2, 1, 5, 4};
        int k = 6;
        System.out.println(findLengthOfSmallestSubarrayBruteForce(data, k));
        System.out.println(findLengthOfSmallestSubarrayOptimal(data, k));
    }
}
