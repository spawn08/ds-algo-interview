package com.dsalgo;

import com.dsalgo.arrays.ArraysTest;
import com.dsalgo.misc.MiscTest;
import com.dsalgo.searching.SearchingTest;
import com.dsalgo.stacks.StacksTest;
import com.dsalgo.strings.StringsTest;
import com.dsalgo.trees.TreesTest;

/**
 * Entry point for the Java test suite.
 *
 * Compile and run from the {@code java/} directory:
 * <pre>
 *   javac -d bin-test $(find src test -name '*.java')
 *   java -cp bin-test com.dsalgo.RunAllTests
 * </pre>
 * Exits with status 1 if any assertion fails, so it works in CI.
 */
public final class RunAllTests {

    public static void main(String[] args) {
        TestHarness h = new TestHarness();

        ArraysTest.run(h);
        StringsTest.run(h);
        SearchingTest.run(h);
        StacksTest.run(h);
        TreesTest.run(h);
        MiscTest.run(h);

        System.out.println();
        System.out.println("====================================");
        System.out.println("Passed: " + h.passed() + "   Failed: " + h.failed());
        System.out.println("====================================");

        if (h.failed() > 0) {
            System.exit(1);
        }
    }
}
