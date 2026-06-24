"""
Given a binary tree, find the lowest common ancestor (LCA) of two given
nodes in the tree.
<link>https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/</link>

The lowest common ancestor is defined between two nodes p and q as the
lowest node in T that has both p and q as descendants (where we allow a
node to be a descendant of itself).

Example 1:

Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
Output: 3
Explanation: The LCA of nodes 5 and 1 is 3.

Example 2:

Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
Output: 5
Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a
descendant of itself.
"""

from typing import Optional
from tree import TreeNode


class Solution:
    """
    Single post-order DFS.

    Why post-order (children before parent)?  A node can only be the LCA once
    we know what each of its subtrees contains. We recurse down, and let each
    call report back whether it found p or q. The first node that sees one
    target on its left and the other on its right (or is itself a target with
    the other below it) is the lowest common ancestor.

    Time complexity:  O(n) -- every node is visited once.
    Space complexity: O(h) -- recursion stack, h = height of the tree.
    """

    def lowestCommonAncestor(self, root: Optional[TreeNode],
                             p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
        if root is None or root is p or root is q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        # p and q were found in different subtrees -> this node is the LCA.
        if left and right:
            return root

        # Otherwise bubble up whichever side actually found something.
        return left if left else right


if __name__ == '__main__':
    #        3
    #      /   \
    #     5     1
    #    / \   / \
    #   6   2 0   8
    #      / \
    #     7   4
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    root.left.right.left = TreeNode(7)
    root.left.right.right = TreeNode(4)

    solution = Solution()
    p, q = root.left, root.right          # nodes 5 and 1
    print(solution.lowestCommonAncestor(root, p, q).val)  # 3
    p, q = root.left, root.left.right.right  # nodes 5 and 4
    print(solution.lowestCommonAncestor(root, p, q).val)  # 5
