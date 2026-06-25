"""
Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).
<link>https://leetcode.com/problems/binary-tree-level-order-traversal/description/</link>

Example 1: 
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]

Example 2:

Input: root = [1]
Output: [[1]]

Example 3:

Input: root = []
Output: []
"""

from tree import TreeNode
from typing import List, Optional
from collections import deque


class Solution:
	"""
	BFS level by level: capture the queue size at the start of each level so
	exactly that many nodes are grouped together.

	Time complexity:  O(n) -- every node is enqueued and dequeued once.
	Space complexity: O(n) -- the queue holds up to a full level (O(n/2) at
	                  the widest), plus the output.
	"""

	def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

		if not root:
			return []
		queue = deque([root])
		result = []

		while queue:
			current_level = []
			queue_size = len(queue)

			for _ in range(queue_size):
				current_node = queue.popleft()

				current_level.append(current_node.val)

				if current_node.left:
					queue.append(current_node.left)
				if current_node.right:
					queue.append(current_node.right)
			result.append(current_level)
		return result

if __name__ == '__main__':
	#input_tree = [3, 9, 20, None, None, 15, 7]
	root = TreeNode(3)
	root.left = TreeNode(9)
	root.right = TreeNode(20)
	root.right.left = TreeNode(15)
	root.right.right = TreeNode(7)
	solution = Solution()
	print(solution.levelOrder(root))
