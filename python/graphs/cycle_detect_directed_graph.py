
from typing import List
from collections import defaultdict, deque

class Solution:

	def detect_cycle_directed_graph(self, vertices: int, adj: List[List[int]]):
		indegree = [0] * vertices
		graph = defaultdict(list)

		for u in range(vertices):
			for v in adj[u]:
				graph[u].append(v)
				indegree[v] += 1

		# queue for maintaining vertices which doesn't have dependencies and can be processed early
		queue: deque = deque(i for i in range(vertices) if indegree[i] == 0)
		processed: int = 0

		while queue:
			node = queue.popleft()
			processed += 1

			for neighbour in graph[node]:
				indegree[neighbour] -= 1
				if indegree[neighbour] == 0:
					queue.append(neighbour)

		return processed != vertices


if __name__ == '__main__':
	solution = Solution()
	# 0 -> 1 -> 2 -> 0  (cycle)
	print(solution.detect_cycle_directed_graph(3, [[1], [2], [0]]))   # True
	# 0 -> 1 -> 2  (DAG, no cycle)
	print(solution.detect_cycle_directed_graph(3, [[1, 2], [2], []]))  # False



