
from tree import TreeNode
from collections import deque
from typing import List


class TreeTraversal:


    def in_order_traversal(self, node: TreeNode):
        if not node:
            return
        
        self.in_order_traversal(node.left)
        print(node.val)
        self.in_order_traversal(node.right)

    def pre_order_traversal(self, node: TreeNode):
        if not node:
            return
        
        print(node.val)
        self.pre_order_traversal(node.left)
        self.pre_order_traversal(node.right)
    
    def post_order_traversal(self, node: TreeNode):

        if not node:
            return
        
        self.post_order_traversal(node.left)
        self.post_order_traversal(node.right)
        print(node.val)

    def level_order_traversal(self, node: TreeNode) -> List[int]:

        if not node:
            return []

        queue = deque([node])
        traversal = []

        while queue:
            current_node = queue.popleft()
            traversal.append(current_node.val)

            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

        return traversal


if __name__ == '__main__':
    #        1
    #       / \
    #      2   3
    #     / \
    #    4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    traversal = TreeTraversal()
    print("In-order (prints):")
    traversal.in_order_traversal(root)        # 4 2 5 1 3
    print("Pre-order (prints):")
    traversal.pre_order_traversal(root)       # 1 2 4 5 3
    print("Level-order:", traversal.level_order_traversal(root))  # [1, 2, 3, 4, 5]