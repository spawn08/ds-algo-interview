"""
Given the root of a binary tree, return the inorder traversal of its nodes' values.
<link>https://leetcode.com/problems/binary-tree-inorder-traversal/description</link>

Example 1:

Input: root = [1,null,2,3]
Output: [1,3,2]

Example 2:

Input: root = [1,2,3,4,5,null,8,null,null,6,7,9]
Output: [4,2,6,5,7,1,3,9,8]

Example 3:

Input: root = []
Output: []

Example 4:

Input: root = [1]
Output: [1]
"""

from tree import TreeNode
from typing import List, Optional


class Solution:
	"""
	Recursive inorder traversal (left -> node -> right).

	Time complexity:  O(n) -- every node is visited once.
	Space complexity: O(h) -- recursion stack, h = height (plus O(n) for the
	                  output list).
	"""

	def helper(self, root: Optional[TreeNode], traversal: list[int]):
		if root is not None:
			self.helper(root.left, traversal)
			traversal.append(root.val)
			self.helper(root.right, traversal)


	def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
		traversal = []
		self.helper(root, traversal)
		return traversal

if __name__ == '__main__':
	# root = [1, null, 2, 3]  ->  [1, 3, 2]
	root = TreeNode(1)
	root.right = TreeNode(2)
	root.right.left = TreeNode(3)

	solution = Solution()
	print(solution.inorderTraversal(root))
