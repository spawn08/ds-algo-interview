package com.tutorials.datastructures.trees;


import java.util.ArrayList;
import java.util.List;

/**
 * Write a function that takes in a Binary Tree and returns a list of its branch sums
 * ordered from leftmost branch sum to rightmost branch sum.
 * A branch sum is a sum of all values in a branch in Binary Tree. A binary tree branch is a path of nodes
 * in a tree that starts at a root node and ends at any leaf node.
 */
class BranchSum {

    public static void main(String[] args) {
        List<Integer> sums = new ArrayList<>();
        TreeNode root = TreeNode.getBinarytree();
        BranchSum branchSum = new BranchSum();
        branchSum.calculateBranchSums(root, 0, sums);
        System.out.println(sums);

    }

    /**
     * This method calculates the sum of all the branches in the binary tree.
     * Time complexity: O(n) where n is number of nodes in a tree
     * Space Complexity: O(n) due to recursion call stack
     * 
     */
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