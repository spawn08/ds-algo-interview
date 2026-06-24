package com.dsalgo.arrays;

import com.dsalgo.TestHarness;
import com.dsalgo.arrays.subarray.MaximumSubArray;
import com.dsalgo.arrays.subarray.MaximumSumSubArrayWithK;
import com.dsalgo.arrays.subarray.SubarrayOR;
import com.dsalgo.arrays.twosum.TwoSumBruteForce;
import com.dsalgo.arrays.twosum.TwoSumHashTable;
import com.dsalgo.arrays.twosum.TwoSumUsingPointers;

public final class ArraysTest {

    public static void run(TestHarness h) {
        System.out.println("[arrays]");

        h.check("ContainsDuplicate true", ContainsDuplicate.containsDuplicate(new int[]{1, 2, 3, 1}));
        h.check("ContainsDuplicate false", !ContainsDuplicate.containsDuplicate(new int[]{1, 2, 3, 4}));

        TwoSumBruteForce brute = new TwoSumBruteForce();
        h.assertArrayEquals("TwoSum brute force", new int[]{0, 1}, brute.twoSumBruteForce(new int[]{2, 7, 11, 15}, 9));

        TwoSumHashTable hash = new TwoSumHashTable();
        h.assertArrayEquals("TwoSum hash table", new int[]{0, 1}, hash.twoSumHashTable(new int[]{2, 7, 11, 15}, 9));

        // Two-pointer variant returns the matching VALUES (after sorting), not indices.
        TwoSumUsingPointers ptr = new TwoSumUsingPointers();
        h.assertArrayEquals("TwoSum two pointers (values)", new int[]{2, 7}, ptr.findTwoSum(new int[]{2, 7, 11, 15}, 9));

        MaximumSubArray maxSub = new MaximumSubArray();
        h.assertEquals("Kadane (running)", 6, maxSub.findMaxSubArray(new int[]{-2, 1, -3, 4, -1, 2, 1, -5, 4}));
        h.assertEquals("Kadane (DP form)", 6, maxSub.findMaxSubArray2(new int[]{-2, 1, -3, 4, -1, 2, 1, -5, 4}));
        h.assertEquals("Kadane all negative", -1, maxSub.findMaxSubArray2(new int[]{-1, -2, -3}));

        MaximumSumSubArrayWithK windowK = new MaximumSumSubArrayWithK();
        h.assertEquals("Max sum window k=2", 700, windowK.maximumSumSubArray(new int[]{100, 200, 300, 400}, 2, 4));
        h.assertEquals("Max sum window k=4", 1000, windowK.maximumSumSubArray(new int[]{100, 200, 300, 400}, 4, 4));

        h.assertEquals("Smallest subarray OR (brute)", 3,
                SubarrayOR.findLengthOfSmallestSubarrayBruteForce(new int[]{1, 2, 1, 5, 4}, 6));
        h.assertEquals("Smallest subarray OR (optimal)", 3,
                SubarrayOR.findLengthOfSmallestSubarrayOptimal(new int[]{1, 2, 1, 5, 4}, 6));
    }
}
