from typing import List

"""
Given a string s containing just the characters
'(', ')', '{', '}', '[' and ']', determine if the
input string is valid.

An input string is valid if:
Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Every close bracket has a corresponding open bracket of the same type.

Example 1:

Input: s = "()"
Output: true

Example 2:

Input: s = "()[]{}"
Output: true

Example 3:

Input: s = "(]"
Output: false

Example 4:
Input: s = "([])"
Output: true
"""


class ValidParentheses:
    """
    Push opening brackets onto a stack; on a closing bracket the stack top
    must be its matching opener. Valid iff the stack ends empty.

    Time complexity:  O(n) -- each character is pushed/popped at most once.
    Space complexity: O(n) -- worst case all openers (e.g. "(((((").
    """

    def valid_parantheses(self, s: str) -> bool:

        if not s or len(s) % 2 != 0:
            return False
        # create a parenthese map for each closing bracket with corresponding
        # opening bracket
        parantheses_map = {"}": "{", "]": "[", ")": "("}
        stack_list: List[str] = []

        for char in s:
            # if character is present in parantheses_map(closing bracket)
            if char in parantheses_map:
                if not stack_list or stack_list.pop() != parantheses_map[char]:
                    return False
            else:
                # append opening bracket
                stack_list.append(char)
        return len(stack_list) == 0


if __name__ == '__main__':
    solution = ValidParentheses()
    print(solution.valid_parantheses("([])"))
