package com.tutorials.datastructures.trees;


public class SearchBST {

    public TreeNode searchBST(TreeNode root, int val) {

    	if (root == null || root.data == val) {
    		return root;
    	}

    	if (root.data > val) {
    		return searchBST(root.left, val);
    	} else {
    		return searchBST(root.right, val);
    	}

    }

	public static void main(String[] args) {
        TreeNode treeNode = new TreeNode(4);
		treeNode.left = new TreeNode(2);
		treeNode.right = new TreeNode(6);
		treeNode.left.left = new TreeNode(1);
		treeNode.left.right = new TreeNode(3);
		treeNode.right.left = new TreeNode(5);
		treeNode.right.right = new TreeNode(7);

//		treeNode = new TreeNode(10);
//		treeNode.left = new TreeNode(5);
//		treeNode.right = new TreeNode(20);
//		treeNode.left.left = new TreeNode(1);
//		treeNode.left.right = new TreeNode(7);
//		treeNode.right.left = new TreeNode(15);
//		treeNode.right.right = new TreeNode(25);

		SearchBST searchBST = new SearchBST();
		System.out.println(searchBST.searchBST(treeNode, 3) != null);
	}
}