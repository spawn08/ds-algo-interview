package com.tutorials.problems;

import java.util.*;

public class BucketsSolution2 {
    public static int minMoves(String buckets) {
        int n = buckets.length();
        int k = 0;
        // Count the total number of balls
        for (int i = 0; i < n; i++) {
            if (buckets.charAt(i) == 'B') {
                k++;
            }
        }
        // No balls to move
        if (k == 0) return 0;
        // To place k balls with a gap of one empty bucket between consecutive balls,
        // we need at least 2*k - 1 buckets.
        if (n < 2 * k - 1) return -1;

        int maxMatched = 0;
        // Check both even (p = 0) and odd (p = 1) starting positions.
        for (int p = 0; p < 2; p++) {
            ArrayList<Integer> indices = new ArrayList<>();
            // Build a list of all indices with parity p
            for (int i = p; i < n; i += 2) {
                indices.add(i);
            }
            // If there aren’t enough positions with this parity, skip.
            if (indices.size() < k) continue;

            int m = indices.size();
            // Build a prefix sum array for quick range sum queries.
            // prefix[i] will be the number of balls in the positions indices[0..i-1].
            int[] prefix = new int[m + 1];
            for (int i = 0; i < m; i++) {
                int pos = indices.get(i);
                prefix[i + 1] = prefix[i] + (buckets.charAt(pos) == 'B' ? 1 : 0);
            }

            // Slide a window of length k over the list of indices.
            // Every contiguous block corresponds to a valid arithmetic progression.
            for (int i = 0; i <= m - k; i++) {
                int currMatched = prefix[i + k] - prefix[i];
                maxMatched = Math.max(maxMatched, currMatched);
            }
        }

        // The minimal moves required is the number of balls that are NOT already in a target bucket.
        return k - maxMatched > 0 ? k - maxMatched : -1;
    }

    public static void main(String[] args) {
        // Sample test cases:
        String input1 = "BB.B.BBB..."; // Sample Input 1, expected output: 4
        String input2 = "..B....B.BB"; // Sample Input 2, expected output: 2
        String input3 = "..B.B..BB."; // Sample Input 3, expected output: 1
        String input4 = "BB.B."; // Sample Input 4 (here "BB.B" has 4 characters so that 3 balls require at least 5 buckets), expected output: -1
        String input5 = "B.B.B.";

        System.out.println(minMoves(input1)); // prints 4
        System.out.println(minMoves(input2)); // prints 2
        System.out.println(minMoves(input3)); // prints 1
        System.out.println(minMoves(input4)); // prints -1
        System.out.println(minMoves(input5));
    }
}
