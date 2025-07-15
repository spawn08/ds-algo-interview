package com.tutorials.datastructures.trees;


import java.util.List;
import java.util.ArrayList;

class BranchSum {

	public static void main(String[] args) {
		List<Integer> sums = new ArrayList<>();
		TreeNode root = TreeNode.getBinarytree();
		BranchSum branchSum = new BranchSum();
		branchSum.calculateBranchSums(root, 0, sums);
		System.out.println(sums);

	}

	// this method calculates the sum of all the branches in the binary tree
	public void calculateBranchSums(TreeNode root, int currentSum, List<Integer> sums) {
		if (root == null) return;
		
		int newRunningSum = currentSum + root.data;
		if (root.right == null && root.left == null) {
			sums.add(newRunningSum);
			return;
		}
		calculateBranchSums(root.left, newRunningSum, sums);
		calculateBranchSums(root.right, newRunningSum, sums);

	}
}