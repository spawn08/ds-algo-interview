package com.dsalgo.strings;

import com.dsalgo.TestHarness;

public final class StringsTest {

    public static void run(TestHarness h) {
        System.out.println("[strings]");

        h.assertEquals("Reverse 'Hola'", "aloH", ReverseString.reverseString("Hola"));
        h.assertEquals("Reverse 'abc'", "cba", ReverseString.reverseString("abc"));

        h.assertEquals("LCS abcde/ace", 3, LongestCommonSubsequence.lcs("abcde", "ace"));
        h.assertEquals("LCS abc/abc", 3, LongestCommonSubsequence.lcs("abc", "abc"));
        h.assertEquals("LCS abc/def", 0, LongestCommonSubsequence.lcs("abc", "def"));
        h.assertEquals("LCS null", 0, LongestCommonSubsequence.lcs(null, "x"));
    }
}
