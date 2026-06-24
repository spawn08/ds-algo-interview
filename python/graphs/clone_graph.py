"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from typing import Optional
from collections import deque

class Solution:
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
        