"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from typing import Optional
from collections import deque


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    """
    BFS over the original graph, building clones and wiring up edges as we go;
    a dict maps each value to its already-created clone to avoid revisiting.

    Time complexity:  O(V + E) -- every node and every edge is processed once.
    Space complexity: O(V) -- the clones map plus the BFS queue.
    """

    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:

        if not node:
            return None
        
        queue, clones = deque([node]), {node.val: Node(node.val)}
        while queue:
            current_node = queue.popleft()
            curr_clone = clones[current_node.val]

            for neighbor in current_node.neighbors:
                if neighbor.val not in clones:
                    clones[neighbor.val] = Node(neighbor.val)
                    queue.append(neighbor)
                curr_clone.neighbors.append(clones[neighbor.val])
        return clones[node.val]


if __name__ == '__main__':
    # Build an undirected graph: 1-2, 1-4, 2-3, 3-4 (a 4-cycle)
    n1, n2, n3, n4 = Node(1), Node(2), Node(3), Node(4)
    n1.neighbors = [n2, n4]
    n2.neighbors = [n1, n3]
    n3.neighbors = [n2, n4]
    n4.neighbors = [n1, n3]

    clone = Solution().cloneGraph(n1)
    print(clone.val, [nb.val for nb in clone.neighbors])  # 1 [2, 4]
    print("deep copy?", clone is not n1)                  # True
        