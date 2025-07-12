package com.tutorials.datastructures.trees;


class MaxPathSum {
	private int maxSum = Integer.MIN_VALUE;

	public int maxPathSum(TreeNode root) {
		dfs(root);
		return maxSum;
	}

	private int dfs(TreeNode root) {
		if (root == null) return 0;

		// discard negative values with `0`
		int leftGain = Math.max(0, dfs(root.left));
		int rightGain = Math.max(0, dfs(root.right));

		maxSum = Math.max(maxSum, leftGain + rightGain + root.data);
		return root.data + Math.max(leftGain, rightGain);
	}


	public static void main(String[] args) {
		TreeNode root = TreeNode.getBinarytree();
		MaxPathSum maxPathSum = new MaxPathSum();
		System.out.println(maxPathSum.maxPathSum(root));
	}
}