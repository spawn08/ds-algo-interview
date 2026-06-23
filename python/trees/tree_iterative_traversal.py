from tree import TreeNode


class IterativeTraversals:


	def in_order_traversal(self, node: TreeNode) -> list[int]:
		if not node:
			return

		stack = []
		traversal = []
		current_node = node

		while current_node is not None or len(stack) > 0:
			while current_node is not None:
				stack.append(current_node)
				current_node = current_node.left

			current_node = stack.pop()
			traversal.append(current_node.val)

			current_node = current_node.right

		return traversal

if __name__ == '__main__':
	
	root = TreeNode(1)
	root.left = TreeNode(2)
	root.right = TreeNode(3)
	root.right.left = TreeNode(4)
	root.right.left = TreeNode(5)

	traversal = IterativeTraversals()
	result = traversal.in_order_traversal(root)
	print(" ".join(map(str, result)))

