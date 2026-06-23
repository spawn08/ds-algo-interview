
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
            return

        queue = deque([node.val])
        traversal = []


        while queue:
            current_node = queue.popleft()
            traversal.append(current_node)

            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

        return traversal