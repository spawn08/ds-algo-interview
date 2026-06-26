"""
Given the root of a binary search tree, and an integer k, 
return the kth smallest value (1-indexed) of all the values of the nodes in the tree.

Example 1:

Input: root = [3,1,4,null,2], k = 1
Output: 1

Example 2:

Input: root = [5,3,6,2,4,null,null,1], k = 3
Output: 3
"""

from typing import Optional
from tree import TreeNode


class Solution:
	"""
	Kth smallest in a BST via an inorder traversal.

	An inorder traversal of a BST (left -> node -> right) visits values in
	ascending order, so the kth node visited is the kth smallest. We carry a
	countdown in count[0]; when it reaches 1 the current node is the answer, and
	we stop descending right once the count is exhausted (early exit).

	Time complexity:  O(h + k) -- we descend to the smallest value (O(h)) then
	                  visit k nodes; O(n) worst case (skewed tree, large k).
	Space complexity: O(h) -- recursion stack, h = height of the tree.
	"""

	def kth_smallest_element(self, root: Optional[TreeNode], k: int) -> int:
		'''
		This method calculates the kth smallest element present in binary search tree

		param:
			root: TreeNode datastructure
			k: int value for finding smallest element at k
		Time Complexity: O(n)
		Space Complexity: O(h) where h is height of tree
		'''
		
		count = [k]
		ans = [0]

		def dfs(node: Optional[TreeNode]):
			if not node:
				return
			dfs(node.left)

			if count[0] == 1:
				ans[0] = node.val

			count[0] = count[0] - 1	

			if count[0] > 0:
				dfs(node.right)
		dfs(root)
		return ans[0]


if __name__ == '__main__':
	input_list = [5, 3, 6, 2, 4, None, None, 1]
	root = TreeNode(5)
	root.left = TreeNode(3)
	root.right = TreeNode(6)
	root.left.left = TreeNode(2)
	root.left.right = TreeNode(4)
	root.left.left.left = TreeNode(1)
	solution = Solution()
	print(solution.kth_smallest_element(root, 3))
