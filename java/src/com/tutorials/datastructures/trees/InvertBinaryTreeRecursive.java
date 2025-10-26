package com.tutorials.datastructures.trees;

class InvertBinaryTreeRecursive {

	public static void invertBinaryTree(TreeNode root) {
		if (root == null) return;

		swapBinaryTree(root);
		invertBinaryTree(root.left);
		invertBinaryTree(root.right);
	}

	public static void swapBinaryTree(TreeNode root) {
		TreeNode left = root.left;
		root.left = root.right;
		root.right = left;
	}

	public static void main(String[] args) {
		TreeNode treeNode = TreeNode.getBinarytree();
		InvertBinaryTreeRecursive.invertBinaryTree(treeNode);
	}
}