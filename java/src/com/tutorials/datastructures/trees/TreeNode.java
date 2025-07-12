
package com.tutorials.datastructures.trees;

public class TreeNode {
	
	public int data;
	public TreeNode right;
	public TreeNode left;

	public TreeNode(int data) {
		this.data = data;
		left = right = null;
	}

	public static TreeNode getBinarytree() {
		TreeNode treeNode = new TreeNode(4);
		treeNode.left = new TreeNode(3);
		treeNode.right = new TreeNode(5);
		treeNode.left.left = new TreeNode(2);
		treeNode.left.right = new TreeNode(6);
		treeNode.right.right = new TreeNode(8);
		treeNode.right.left = new TreeNode(7);

		return treeNode;
	}
}