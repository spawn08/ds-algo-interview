"""Tests for the graph solutions."""

import importlib

import pytest


def test_bfs_and_dfs_orders():
    mod = importlib.import_module("graph_traversal")
    g = mod.GraphBFS()
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }
    # BFS visits every reachable node exactly once, starting at the source.
    bfs_order = g.bfs(graph, "A")
    assert bfs_order[0] == "A"
    assert sorted(bfs_order) == ["A", "B", "C", "D", "E", "F"]

    dfs_order = g.dfs_iterative(graph, "A")
    assert dfs_order[0] == "A"
    assert sorted(dfs_order) == ["A", "B", "C", "D", "E", "F"]


def test_number_of_islands():
    mod = importlib.import_module("number_of_island")
    solver = mod.Solution()
    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    assert solver.numIslands(grid1) == 1

    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert solver.numIslands(grid2) == 3
    assert solver.numIslands([]) == 0


def test_number_of_provinces():
    mod = importlib.import_module("number_of_provinces")
    solver = mod.Solution()
    assert solver.findCircleNum([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
    assert solver.findCircleNum([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3


def test_cycle_detection_directed():
    mod = importlib.import_module("cycle_detect_directed_graph")
    solver = mod.Solution()
    # 0 -> 1 -> 2 -> 0  (cycle)
    assert solver.detect_cycle_directed_graph(3, [[1], [2], [0]]) is True
    # 0 -> 1 -> 2  (DAG, no cycle)
    assert solver.detect_cycle_directed_graph(3, [[1, 2], [2], []]) is False


def test_cycle_detection_undirected():
    mod = importlib.import_module("cycle_detect_undirected_graph")
    solver = mod.Solution()
    assert solver.detect_cycle(3, [[1, 2], [0, 2], [0, 1]]) is True   # triangle
    assert solver.detect_cycle(3, [[1], [0, 2], [1]]) is False        # path 0-1-2


def test_clone_graph():
    mod = importlib.import_module("clone_graph")

    class Node:
        def __init__(self, val=0, neighbors=None):
            self.val = val
            self.neighbors = neighbors if neighbors is not None else []

    # The solution references a module-level ``Node`` (supplied by LeetCode);
    # inject our definition so the BFS clone can construct new nodes.
    mod.Node = Node

    # Build graph: 1-2, 1-4, 2-3, 3-4 (a 4-cycle).
    n1, n2, n3, n4 = Node(1), Node(2), Node(3), Node(4)
    n1.neighbors = [n2, n4]
    n2.neighbors = [n1, n3]
    n3.neighbors = [n2, n4]
    n4.neighbors = [n1, n3]

    clone = mod.Solution().cloneGraph(n1)

    # Same value, but a brand-new object (deep copy).
    assert clone is not n1
    assert clone.val == 1
    assert sorted(nb.val for nb in clone.neighbors) == [2, 4]
    # Every cloned neighbor must itself be a clone, not an original.
    assert all(nb is not orig for nb, orig in zip(clone.neighbors, n1.neighbors))
    assert mod.Solution().cloneGraph(None) is None


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
