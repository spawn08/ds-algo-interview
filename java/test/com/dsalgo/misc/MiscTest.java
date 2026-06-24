package com.dsalgo.misc;

import com.dsalgo.TestHarness;

public final class MiscTest {

    public static void run(TestHarness h) {
        System.out.println("[misc]");

        // BucketsSolution2 is the corrected solution per the problem's expected outputs.
        h.assertEquals("Buckets 'BB.B.BBB...'", 4, BucketsSolution2.minMoves("BB.B.BBB..."));
        h.assertEquals("Buckets '..B....B.BB'", 2, BucketsSolution2.minMoves("..B....B.BB"));
        h.assertEquals("Buckets '..B.B..BB.'", 1, BucketsSolution2.minMoves("..B.B..BB."));
        // 3 balls need 2*3-1=5 buckets; "BB.B" has only 4 -> impossible.
        h.assertEquals("Buckets 'BB.B' (impossible)", -1, BucketsSolution2.minMoves("BB.B"));
        // "BB.B." has 5 buckets, so it IS solvable.
        h.assertEquals("Buckets 'BB.B.' (solvable)", 2, BucketsSolution2.minMoves("BB.B."));

        h.assertEquals("Wooden sticks (10,21)", 7, WoodenSticksProblem.solution(10, 21));
        h.assertEquals("Wooden sticks (13,11)", 5, WoodenSticksProblem.solution(13, 11));
        h.assertEquals("Wooden sticks (2,1)", 0, WoodenSticksProblem.solution(2, 1));
        h.assertEquals("Wooden sticks (1,8)", 2, WoodenSticksProblem.solution(1, 8));
    }
}
