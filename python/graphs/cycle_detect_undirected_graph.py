
"""
Given an undirected graph with V vertices and an adjacency list adj, determine whether the graph contains a cycle.

A cycle exists if there is a path that starts and ends at the same vertex, visiting at least one other vertex.
In undirected graphs, we must be careful not to consider the edge back to the parent as a cycle.

Cycle exists:Pythonadj = [[1,2], [0,2], [0,1]]   # Triangle: 0-1-2-0
Output: True
No cycle (Tree):Pythonadj = [[1], [0,2], [1]]        # 0-1-2
Output: False
"""

from typing import List

class Solution:

	def detect_cycle(self, num_nodes: int, graph: List[List[int]]):
		"""
		Detect a cycle in undirected graph using iterative DFS

		num_nodes: number of nodes
		graph: Adjacency list graph representation
		"""
		visited: List[bool] = [False] * num_nodes

		def dfs_iterative(start: int):
			stack = [(start, -1)]
			visited[start] = True

			while stack:
				current_node, parent = stack.pop()

				for neighbour in graph[current_node]:
					if not visited[neighbour]:
						visited[neighbour] = True
						stack.append((neighbour, current_node))
					elif parent != neighbour:
						return True
			return False

		for i in range(num_nodes):
			if not visited[i]:
				if dfs_iterative(i):
					return True
		return False

# Test the function
def test_cycle_detection():
	sol = Solution()
	# Example 1 - Has Cycle
	adj1 = [[1,2],[0,2],[0,1,3],[2,4],[3]]
	print("Example 1 (Has Cycle):", sol.detect_cycle(5, adj1))   # True
	# Example 2 - No Cycle
	adj2 = [[1],[0,2],[1,3],[2]]
	print("Example 2 (No Cycle):", sol.detect_cycle(4, adj2))    # False


if __name__ == '__main__':
	test_cycle_detection()
