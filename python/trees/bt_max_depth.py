"""
Given the root of a binary tree, return its maximum depth.
A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: 3

Example 2:

Input: root = [1,null,2]
Output: 2
"""

from tree import TreeNode
from typing import Optional


class Solution:

	def max_depth(self, root: Optional[TreeNode]) -> int:
		if not root:
			return 0

		left_depth = self.max_depth(root.left)
		right_depth = self.max_depth(root.right)
		return 1 + max(left_depth, right_depth)


if __name__ == '__main__':
	root = TreeNode(3)
	root.left = TreeNode(9)
	root.right = TreeNode(20)
	root.left.left = TreeNode(15)
	root.left.right = TreeNode(7)
	solution = Solution()
	print(solution.max_depth(root))
