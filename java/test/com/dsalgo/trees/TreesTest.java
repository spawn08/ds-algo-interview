package com.dsalgo.trees;

import java.util.ArrayList;
import java.util.List;

import com.dsalgo.TestHarness;

/**
 * Lives in {@code com.dsalgo.trees} so it can reach the package-private
 * solution classes (BranchSum, MaxPathSum, LevelOrderTraversal, ...).
 */
public final class TreesTest {

    public static void run(TestHarness h) {
        System.out.println("[trees]");

        // Shared sample tree:
        //        4
        //      /   \
        //     3     5
        //    / \   / \
        //   2   6 7   8
        BranchSum branchSum = new BranchSum();
        List<Integer> sums = new ArrayList<>();
        branchSum.calculateBranchSums(TreeNode.getBinarytree(), 0, sums);
        h.assertListEquals("Branch sums", List.of(9, 13, 16, 17), sums);

        MaxPathSum maxPathSum = new MaxPathSum();
        h.assertEquals("Max path sum", 26, maxPathSum.maxPathSum(TreeNode.getBinarytree()));

        h.assertEquals("Level order (left-to-right)",
                "[[4], [3, 5], [2, 6, 7, 8]]",
                String.valueOf(LevelOrderTraversal.levelOrderTraversal2(TreeNode.getBinarytree())));

        // Binary search tree for searchBST: 4 / 2,6 / 1,3,5,7
        TreeNode bst = new TreeNode(4);
        bst.left = new TreeNode(2);
        bst.right = new TreeNode(6);
        bst.left.left = new TreeNode(1);
        bst.left.right = new TreeNode(3);
        bst.right.left = new TreeNode(5);
        bst.right.right = new TreeNode(7);
        SearchBST searchBST = new SearchBST();
        h.check("BST search finds 3", searchBST.searchBST(bst, 3) != null);
        h.check("BST search misses 8", searchBST.searchBST(bst, 8) == null);

        // Invert swaps every left/right child.
        TreeNode toInvert = TreeNode.getBinarytree();
        InvertBinaryTreeRecursive.invertBinaryTree(toInvert);
        h.assertEquals("Invert: root.left becomes old right", 5, toInvert.left.data);
        h.assertEquals("Invert: root.right becomes old left", 3, toInvert.right.data);
    }
}
