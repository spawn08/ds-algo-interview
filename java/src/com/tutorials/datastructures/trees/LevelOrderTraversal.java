package com.tutorials.datastructures.trees;

import java.util.List;
import java.util.LinkedList;
import java.util.Queue;
import java.util.ArrayList;

class LevelOrderTraversal {

	public static List<List<Integer>> levelOrderTraversal(TreeNode root) {

		List<List<Integer>> levelOrderList = new ArrayList<>();

		if (root == null) {
			return levelOrderList;
		}

		Queue<TreeNode> traversalQueue = new LinkedList<>();
		traversalQueue.offer(root);

		while(!traversalQueue.isEmpty()) {
			int queueSize = traversalQueue.size();
			List<Integer> currentLevel = new ArrayList<>();
			for(int index = 0; index < queueSize; index++) {
				TreeNode temp = traversalQueue.poll();
				currentLevel.add(temp.data);
				if(temp.right != null)
					traversalQueue.add(temp.right);
				if (temp.left != null) {
					traversalQueue.add(temp.left);
				}
			}
			levelOrderList.add(currentLevel);
		}

		return levelOrderList;
	}

	public static List<List<Integer>> levelOrderTraversal2(TreeNode root) {
		List<List<Integer>> levelOrderList = new ArrayList<>();
		if(root == null)
			return levelOrderList;

		Queue<TreeNode> traversalQueue = new LinkedList<>();
		traversalQueue.offer(root);

		while(!traversalQueue.isEmpty()) {
			List<Integer> currentLevel = new ArrayList<>();
			int queueSize = traversalQueue.size();
			for(int index = 0; index < queueSize; index++) {
				if(traversalQueue.peek().left != null) traversalQueue.offer(traversalQueue.peek().left);
				if(traversalQueue.peek().right != null) traversalQueue.offer(traversalQueue.peek().right);
				currentLevel.add(traversalQueue.poll().data);
			}
			levelOrderList.add(currentLevel);
		}

		return levelOrderList;
	}

	public static void main(String[] args) {
		TreeNode treeNode = TreeNode.getBinarytree();
		System.out.println(LevelOrderTraversal.levelOrderTraversal(treeNode));
		System.out.println(LevelOrderTraversal.levelOrderTraversal2(treeNode));
	}
}