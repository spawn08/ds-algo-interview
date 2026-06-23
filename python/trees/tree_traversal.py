
from tree import TreeNode


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