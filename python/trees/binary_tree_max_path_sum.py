"""
A path in a binary tree is a sequence of nodes where each
pair of adjacent nodes in the sequence has an edge
connecting them.
A node can only appear in the sequence at most once.
Note that the path does not need to pass through the root.
The path sum of a path is the sum of the node's values
in the path.
Given the root of a binary tree, return the maximum path
sum of any non-empty path.

Example 1:

Input: root = [1,2,3]
Output: 6
Explanation: The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.

Example 2:

Input: root = [-10,9,20,null,null,15,7]
Output: 42
Explanation: The optimal path is 15 -> 20 -> 7
with a path sum of 15 + 20 + 7 = 42.
"""

from tree import TreeNode
from typing import Optional


class Solution:
    """
    Post-order DFS. Each call returns the best downward gain through a node;
    a global max tracks the best path that bends through a node using both
    children. Negative branches are clamped to 0.

    Time complexity:  O(n) -- every node is visited once.
    Space complexity: O(h) -- recursion stack, h = height of the tree.
    """

    def maxPathSum(self, root: Optional[TreeNode]) -> int:

        max_sum = float('-inf')

        def get_max_gain(node: Optional[TreeNode]) -> int:
            nonlocal max_sum
            if not node:
                return 0

            # Clamp negative gains to 0: a branch only helps if it adds value.
            left_gain = max(get_max_gain(node.left), 0)
            right_gain = max(get_max_gain(node.right), 0)

            # Best path that "passes through" this node (can use both children).
            current_path_sum = node.val + left_gain + right_gain
            max_sum = max(max_sum, current_path_sum)

            # A parent can only extend one side, so return the better branch.
            return node.val + max(left_gain, right_gain)

        get_max_gain(root)
        return max_sum


if __name__ == '__main__':
    # root = [-10, 9, 20, null, null, 15, 7]  ->  42
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    solution = Solution()
    print(solution.maxPathSum(root))
