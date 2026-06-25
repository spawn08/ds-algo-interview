"""
Given a binary tree, determine if it is height-balanced.

Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: true

Example 2:

Input: root = [1,2,2,3,3,null,null,4,4]
Output: false
"""

from typing import Optional
from tree import TreeNode


class Solution:
	"""
	Single post-order pass: each call returns the subtree height, or -1 as a
	sentinel once any subtree is found unbalanced, short-circuiting the rest.

	Time complexity:  O(n) -- height and balance computed together in one pass
	                  (the naive recompute-height approach would be O(n^2)).
	Space complexity: O(h) -- recursion stack, h = height of the tree.
	"""

	def is_balanced_binary_tree(self, root: Optional[TreeNode]) -> bool:

		def dfs(node: Optional[TreeNode]):
			if not node:
				return 0

			left_height = dfs(node.left)
			if left_height == -1: return -1
			right_height = dfs(node.right)
			if right_height == -1: return -1

			if abs(left_height - right_height) > 1:
				return -1

			return 1 + max(left_height, right_height)
		return dfs(root) != -1

if __name__ == '__main__':
	root = TreeNode(3)
	root.left = TreeNode(9)
	root.right = TreeNode(20)
	root.right.left = TreeNode(15)
	root.right.right = TreeNode(7)
	solution = Solution()
	print(solution.is_balanced_binary_tree(root))
