package com.dsalgo.stacks;

import com.dsalgo.TestHarness;

public final class StacksTest {

    public static void run(TestHarness h) {
        System.out.println("[stacks]");

        h.check("Valid '()' (array)", ValidParentheses.checkValidParentheses("()"));
        h.check("Valid '()[]{}' (array)", ValidParentheses.checkValidParentheses("()[]{}"));
        h.check("Invalid '([)]' (array)", !ValidParentheses.checkValidParentheses("([)]"));
        h.check("Valid '([])' (array)", ValidParentheses.checkValidParentheses("([])"));

        h.check("Valid '()' (stack)", ValidParentheses.checkValidParenthesesUsingStack("()"));
        h.check("Invalid '([)]' (stack)", !ValidParentheses.checkValidParenthesesUsingStack("([)]"));
        h.check("Valid '([])' (stack)", ValidParentheses.checkValidParenthesesUsingStack("([])"));
    }
}
