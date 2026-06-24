package com.dsalgo;

import java.util.Arrays;
import java.util.List;
import java.util.Objects;

/**
 * Tiny dependency-free test harness.
 *
 * The repository has no build tool (Maven/Gradle) wired up, so rather than pull
 * in JUnit we use a minimal assertion helper that tracks pass/fail counts and
 * lets {@link RunAllTests} exit with a non-zero status when anything breaks.
 */
public final class TestHarness {

    private int passed = 0;
    private int failed = 0;

    public void check(String name, boolean condition) {
        if (condition) {
            passed++;
            System.out.println("  PASS  " + name);
        } else {
            failed++;
            System.out.println("  FAIL  " + name);
        }
    }

    public void assertEquals(String name, Object expected, Object actual) {
        boolean ok = Objects.deepEquals(expected, actual);
        if (ok) {
            passed++;
            System.out.println("  PASS  " + name);
        } else {
            failed++;
            System.out.println("  FAIL  " + name
                    + "  (expected=" + stringify(expected) + ", actual=" + stringify(actual) + ")");
        }
    }

    public void assertArrayEquals(String name, int[] expected, int[] actual) {
        assertEquals(name, Arrays.toString(expected), Arrays.toString(actual));
    }

    public void assertListEquals(String name, List<?> expected, List<?> actual) {
        assertEquals(name, String.valueOf(expected), String.valueOf(actual));
    }

    private static String stringify(Object o) {
        if (o instanceof int[]) {
            return Arrays.toString((int[]) o);
        }
        return String.valueOf(o);
    }

    public int passed() {
        return passed;
    }

    public int failed() {
        return failed;
    }
}
