
from collections import deque

class GraphBFS:

    def bfs(self, graph: dict(int, list[int]), start_node: int) -> None:

        visited_node = {start_node}
        queue = deque([start_node]) 
        visit_order = []
        while queue:
            current_node = queue.popleft()
            visit_order.append(current_node)
            for neighbour in graph.get(current_node, []):
                if neighbour not in visited_node:
                    visited_node.add(neighbour)
                    queue.append(neighbour)
        return visit_order

    def dfs_recursive(self, graph: dict[int, list[int]], current_node: int, visited_node: set[int]) -> None:
        visited_node.add(current_node)
        print(current_node)
        for neighbour in graph[current_node]:
            if neighbour not in visited_node:
                self.dfs_recursive(graph, neighbour, visited_node)

    def dfs_iterative(self, graph: dict[int, list[int]], start_node: int) -> None:
        visited_node = {start_node}
        stack = [start_node]
        visit_order = []

        while stack:
            current_node = stack.pop()
            visit_order.append(current_node)

            for neighbour in graph[current_node]:
                if neighbour not in visited_node:
                    visited_node.add(neighbour)
                    stack.append(neighbour)
        return visit_order

if __name__ == '__main__':
    example_graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    graph_bfs = GraphBFS()
    print(graph_bfs.bfs(example_graph, 'B'))
    graph_bfs.dfs_recursive(example_graph, 'B', set())
    print(graph_bfs.dfs_iterative(example_graph, 'B'))
