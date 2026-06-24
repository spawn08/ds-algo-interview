package com.dsalgo.searching;

import com.dsalgo.TestHarness;

public final class SearchingTest {

    public static void run(TestHarness h) {
        System.out.println("[searching]");

        int[] sorted = {1, 2, 3, 4, 5, 7, 9, 10};
        h.check("Binary search finds 7", BinarySearch.binarySearchIterative(sorted, 7));
        h.check("Binary search finds 1", BinarySearch.binarySearchIterative(sorted, 1));
        h.check("Binary search finds 10", BinarySearch.binarySearchIterative(sorted, 10));
        h.check("Binary search misses 6", !BinarySearch.binarySearchIterative(sorted, 6));
        h.check("Binary search misses 0", !BinarySearch.binarySearchIterative(sorted, 0));
    }
}
