"""Tests for the binary-tree solutions."""

import importlib
from collections import deque

import pytest

tree = importlib.import_module("tree")
TreeNode = tree.TreeNode


def build_tree(values):
    """Build a binary tree from a LeetCode-style level-order list (None = gap)."""
    if not values:
        return None
    it = iter(values)
    root = TreeNode(next(it))
    queue = deque([root])
    for value in it:
        parent = queue[0]
        # Attach left, then right; advance the parent once both are placed.
        if not hasattr(parent, "_left_done"):
            parent._left_done = True
            if value is not None:
                parent.left = TreeNode(value)
                queue.append(parent.left)
        else:
            if value is not None:
                parent.right = TreeNode(value)
                queue.append(parent.right)
            queue.popleft()
    return root


def test_inorder_recursive():
    mod = importlib.import_module("bt_inorder_traversal")
    solver = mod.Solution()
    root = build_tree([1, None, 2, 3])
    assert solver.inorderTraversal(root) == [1, 3, 2]
    assert solver.inorderTraversal(None) == []


def test_inorder_iterative():
    mod = importlib.import_module("tree_iterative_traversal")
    solver = mod.IterativeTraversals()
    root = build_tree([1, 2, 3, 4, 5])
    assert solver.in_order_traversal(root) == [4, 2, 5, 1, 3]


def test_level_order():
    mod = importlib.import_module("bt_level_order_traversal")
    solver = mod.Solution()
    root = build_tree([3, 9, 20, None, None, 15, 7])
    assert solver.levelOrder(root) == [[3], [9, 20], [15, 7]]
    assert solver.levelOrder(None) == []


def test_dfs_traversal_level_order_helper():
    mod = importlib.import_module("tree_traversal_dfs")
    solver = mod.TreeTraversal()
    root = build_tree([1, 2, 3, 4, 5])
    assert solver.level_order_traversal(root) == [1, 2, 3, 4, 5]
    assert solver.level_order_traversal(None) == []


def test_max_depth():
    mod = importlib.import_module("bt_max_depth")
    solver = mod.Solution()
    assert solver.max_depth(build_tree([3, 9, 20, None, None, 15, 7])) == 3
    assert solver.max_depth(build_tree([1, None, 2])) == 2
    assert solver.max_depth(None) == 0


def test_is_balanced():
    mod = importlib.import_module("check_balanced_binary_tree")
    solver = mod.Solution()
    assert solver.is_balanced_binary_tree(build_tree([3, 9, 20, None, None, 15, 7])) is True
    assert solver.is_balanced_binary_tree(build_tree([1, 2, 2, 3, 3, None, None, 4, 4])) is False


def test_max_path_sum():
    mod = importlib.import_module("binary_tree_max_path_sum")
    solver = mod.Solution()
    assert solver.maxPathSum(build_tree([1, 2, 3])) == 6
    assert solver.maxPathSum(build_tree([-10, 9, 20, None, None, 15, 7])) == 42
    assert solver.maxPathSum(build_tree([-3])) == -3


def test_lowest_common_ancestor():
    mod = importlib.import_module("lowest_common_ancestor")
    solver = mod.Solution()
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

    assert solver.lowestCommonAncestor(root, root.left, root.right) is root
    assert solver.lowestCommonAncestor(root, root.left, root.left.right.right) is root.left


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
