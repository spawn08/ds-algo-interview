package com.tutorials.datastructures;

// Definition for a binary tree node
class TreeNode {
    int data;
    TreeNode left, right;

    public TreeNode(int item) {
        data = item;
        left = right = null;
    }
}

public class BinaryTree {
    TreeNode root;

    // Constructor
    public BinaryTree() {
        root = null;
    }

    // In-order traversal
    public void inOrderTraversal(TreeNode node) {
        if (node != null) {
            // Traverse the left subtree
            inOrderTraversal(node.left);

            // Visit the current node
            System.out.print(node.data + " ");

            // Traverse the right subtree
            inOrderTraversal(node.right);
        }
    }

    public void preOrderTraversal(TreeNode root) {
        if (root != null) {
            System.out.print(root.data + " ");
            preOrderTraversal(root.left);
            preOrderTraversal(root.right);
        }
    }

    private void postOrderTraversal(TreeNode root) {
        if (root != null) {
            postOrderTraversal(root.left);
            postOrderTraversal(root.right);
            System.out.print(root.data + " ");
        }
    }

    public static void main(String[] args) {
        BinaryTree tree = new BinaryTree();
        // Sample tree construction
        tree.root = new TreeNode(1);
        tree.root.left = new TreeNode(2);
        tree.root.right = new TreeNode(3);
        tree.root.left.left = new TreeNode(4);
        tree.root.left.right = new TreeNode(5);

        System.out.println("In-order traversal of Binary Tree:");
        tree.inOrderTraversal(tree.root);
        System.out.println();
        System.out.println("Pre-Order traversal of Binary Tree:");
        tree.preOrderTraversal(tree.root);
        System.out.println();
        System.out.println("Post-Order traversal of Binary Tree:");
        tree.postOrderTraversal(tree.root);
    }
}

