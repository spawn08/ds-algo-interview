# Graph Data Structures — From Scratch to Google L5/L6 Interview Ready

All code follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html): snake_case functions/variables, CamelCase classes, type hints, docstrings, descriptive names, no single-character variables unless mathematically standard with citation.

---

## 1. What Is a Graph?

A graph is a collection of **nodes** (also called vertices) connected by **edges**. Formally, `G = (V, E)` where `V` is the set of nodes and `E` is the set of edges between them.

Every other data structure you know is a restricted graph. A linked list is a graph where each node has at most one outgoing edge. A tree is a connected graph with no cycles. A matrix/grid is a graph where each cell connects to its 4 (or 8) neighbors. Once you internalize this, you stop seeing "graph problems" as a separate category and start seeing graphs everywhere — which is exactly what Google expects at L5/L6.

**Why this matters for Google interviews specifically:** Google's core products are graph problems at scale. PageRank is a graph algorithm. Google Maps is shortest-path on a weighted graph. YouTube recommendations are graph traversal. Social connections in Google Chat are graph connectivity. At senior levels, you won't be told "this is a graph problem." You'll be given an ambiguous scenario and expected to *recognize* the graph, *define* what nodes and edges represent, and *choose* the right algorithm — all within the first 2 minutes of your whiteboard discussion.

---

## 2. Graph Vocabulary

You need these terms cold. Interviewers use them without explanation.

**Directed vs Undirected:** In a directed graph, edge A→B does not imply B→A. Think Twitter follows — you can follow someone without them following you back. In an undirected graph, every edge is bidirectional. Think Facebook friendships — if A is friends with B, then B is friends with A.

**Weighted vs Unweighted:** A weighted graph assigns a cost to each edge (distance, time, price). An unweighted graph treats all edges as equal cost (equivalently, cost = 1).

**Cycle:** A path that starts and ends at the same node. A→B→C→A is a cycle. A Directed Acyclic Graph (DAG) is a directed graph guaranteed to have no cycles — these show up constantly in dependency/scheduling problems.

**Connected (undirected):** Every node can reach every other node. **Strongly Connected (directed):** Every node can reach every other node following edge directions.

**Degree:** How many edges touch a node. In directed graphs, this splits into **in-degree** (incoming edges) and **out-degree** (outgoing edges). In-degree is central to topological sort — a node with in-degree 0 has no dependencies.

**Sparse vs Dense:** A graph with `V` nodes can have at most `V²` edges (directed) or `V*(V-1)/2` edges (undirected). Sparse means edge count is closer to `V`. Dense means it's closer to `V²`. This distinction drives your choice of representation.

---

## 3. Graph Representations

The way you store a graph in memory determines the time complexity of every operation you perform on it. This choice is the first decision in any graph problem.

### 3.1 Adjacency List — Use This 90% of the Time

Each node maps to a list of its neighbors. For weighted graphs, each neighbor is stored as a `(neighbor, weight)` tuple.

**Why it works:** Most interview graphs are sparse. An adjacency list uses O(V + E) space, and iterating over a node's neighbors takes O(degree) time — which is exactly what BFS and DFS need.

**When it's the wrong choice:** If the problem repeatedly asks "does an edge exist between node X and node Y?", adjacency list gives O(degree) lookup per query. An adjacency matrix gives O(1). But this pattern is rare in interviews.

```python
from collections import defaultdict


def build_directed_graph(
    edges: list[tuple[int, int]],
) -> dict[int, list[int]]:
    """Builds a directed unweighted graph from an edge list.

    Args:
        edges: List of (source, destination) pairs.

    Returns:
        Adjacency list mapping each node to its neighbors.
    """
    adjacency = defaultdict(list)
    for source, destination in edges:
        adjacency[source].append(destination)
    return adjacency


def build_undirected_graph(
    edges: list[tuple[int, int]],
) -> dict[int, list[int]]:
    """Builds an undirected unweighted graph from an edge list.

    For undirected graphs, every edge must be recorded in both directions.
    Forgetting the reverse edge is one of the most common interview bugs.

    Args:
        edges: List of (node_a, node_b) pairs.

    Returns:
        Adjacency list mapping each node to its neighbors.
    """
    adjacency = defaultdict(list)
    for node_a, node_b in edges:
        adjacency[node_a].append(node_b)
        adjacency[node_b].append(node_a)
    return adjacency


def build_weighted_graph(
    edges: list[tuple[int, int, int]],
) -> dict[int, list[tuple[int, int]]]:
    """Builds a directed weighted graph from an edge list.

    Args:
        edges: List of (source, destination, weight) triples.

    Returns:
        Adjacency list mapping each node to (neighbor, weight) pairs.
    """
    adjacency = defaultdict(list)
    for source, destination, weight in edges:
        adjacency[source].append((destination, weight))
    return adjacency
```

### 3.2 Adjacency Matrix

A `V × V` 2D array where `matrix[i][j]` stores the edge weight (or 1/0 for unweighted) between nodes `i` and `j`.

**Why it exists:** O(1) edge lookup. Also required by Floyd-Warshall (all-pairs shortest path), which iterates over all `(i, j)` pairs.

**The cost:** O(V²) space regardless of how many edges exist. For a sparse graph with 10,000 nodes and 20,000 edges, an adjacency list uses ~30K entries while a matrix uses 100 million.

```python
def build_adjacency_matrix(
    num_nodes: int,
    edges: list[tuple[int, int, int]],
) -> list[list[int]]:
    """Builds a weighted adjacency matrix.

    Uses infinity for non-edges and 0 for self-loops. This convention
    is standard for shortest-path algorithms like Floyd-Warshall.

    Args:
        num_nodes: Total number of nodes (0-indexed).
        edges: List of (source, destination, weight) triples.

    Returns:
        V×V matrix where matrix[i][j] = weight of edge i→j.
    """
    INF = float("inf")
    matrix = [[INF] * num_nodes for _ in range(num_nodes)]
    for node_index in range(num_nodes):
        matrix[node_index][node_index] = 0
    for source, destination, weight in edges:
        matrix[source][destination] = weight
    return matrix
```

### 3.3 Implicit Graphs — The Pattern That Separates L5 from L4

Many Google interview problems never give you an explicit graph. The graph is *implicit* — you construct it from the problem's structure. Recognizing this is the single most important graph skill at senior levels.

**Grid as graph:** Each cell `(row, col)` is a node. Each cell connects to its 4 (or 8) adjacent cells. The grid itself IS the adjacency list — you don't need to build a separate data structure. Problems: Number of Islands, Shortest Path in Binary Matrix, Rotting Oranges.

**String transformation as graph:** Each string state is a node. Each valid single-character mutation is an edge. Problems: Word Ladder, Open the Lock.

**State space as graph:** This is the most powerful and most commonly tested pattern. The node isn't just a position — it's a *compound state* like `(row, col, keys_collected)` or `(row, col, walls_broken)`. Each valid transition is an edge. Problems: Shortest Path with Obstacles Elimination, Shortest Path to Get All Keys.

```python
# Grid neighbor generation — the building block for all grid-graph problems.
# This replaces building an explicit adjacency list for grid problems.

FOUR_DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def get_grid_neighbors(
    row: int,
    col: int,
    num_rows: int,
    num_cols: int,
) -> list[tuple[int, int]]:
    """Returns valid 4-directional neighbors for a grid cell.

    This is the equivalent of "adjacency[node]" for grid-based graphs.
    Bounds checking here replaces the "if neighbor in graph" check
    you'd use with an explicit adjacency list.

    Args:
        row: Current row index.
        col: Current column index.
        num_rows: Total rows in the grid.
        num_cols: Total columns in the grid.

    Returns:
        List of (row, col) tuples for valid neighboring cells.
    """
    neighbors = []
    for delta_row, delta_col in FOUR_DIRECTIONS:
        next_row = row + delta_row
        next_col = col + delta_col
        if 0 <= next_row < num_rows and 0 <= next_col < num_cols:
            neighbors.append((next_row, next_col))
    return neighbors
```

---

## 4. BFS — Breadth-First Search

### The Core Idea

BFS explores a graph in concentric rings outward from the start node. First it visits all nodes at distance 1, then all nodes at distance 2, then distance 3, and so on. This "layer by layer" expansion is what gives BFS its key property: **the first time BFS reaches a node, it has found the shortest path to that node** (in an unweighted graph).

This works because of the queue (FIFO). Nodes discovered earlier are processed earlier. Since closer nodes are always discovered before farther nodes, the queue naturally maintains distance ordering.

**When to use BFS:** Any time you need the shortest path or minimum number of steps in an unweighted graph. If you see "minimum moves", "fewest operations", "shortest transformation sequence" — think BFS immediately.

### Basic BFS Traversal

```python
from collections import deque


def bfs_traversal(
    graph: dict[int, list[int]],
    start_node: int,
) -> list[int]:
    """Visits all nodes reachable from start_node in BFS order.

    Key implementation detail: we add nodes to `visited` AT THE TIME
    WE ENQUEUE THEM, not when we dequeue them. This prevents the same
    node from being enqueued multiple times by different parents.
    Getting this wrong is the #1 BFS bug in interviews — it doesn't
    change correctness but causes O(V²) time instead of O(V + E).

    Args:
        graph: Adjacency list.
        start_node: Node to begin traversal from.

    Returns:
        List of nodes in the order they were visited.
    """
    visited = {start_node}
    queue = deque([start_node])
    visit_order = []

    while queue:
        current_node = queue.popleft()
        visit_order.append(current_node)

        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)  # Mark visited HERE, not after popleft
                queue.append(neighbor)

    return visit_order
```

### BFS Shortest Path (Unweighted)

```python
def bfs_shortest_distance(
    graph: dict[int, list[int]],
    start_node: int,
    target_node: int,
) -> int:
    """Finds the shortest distance between two nodes in an unweighted graph.

    BFS guarantees that the first time we reach target_node, we've found
    the shortest path. This is because every node at distance d is fully
    processed before any node at distance d+1. No other path to
    target_node can be shorter — they'd have been discovered in an
    earlier BFS layer.

    Args:
        graph: Adjacency list (unweighted).
        start_node: Starting node.
        target_node: Node we're trying to reach.

    Returns:
        Shortest distance (number of edges), or -1 if unreachable.
    """
    if start_node == target_node:
        return 0

    visited = {start_node}
    queue = deque([(start_node, 0)])  # (node, distance_from_start)

    while queue:
        current_node, current_distance = queue.popleft()

        for neighbor in graph[current_node]:
            if neighbor == target_node:
                return current_distance + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, current_distance + 1))

    return -1  # Target is unreachable from start
```

### BFS on a Grid — The Most Tested Pattern

```python
def bfs_grid_shortest_path(
    grid: list[list[int]],
    start_row: int,
    start_col: int,
    target_row: int,
    target_col: int,
) -> int:
    """Finds shortest path in a grid where 0 = open, 1 = blocked.

    The grid IS the implicit graph. Each cell is a node. Each pair of
    adjacent open cells is connected by an edge. We don't build a
    separate adjacency list — we generate neighbors on the fly using
    the 4-direction pattern.

    Args:
        grid: 2D grid where 0 is passable and 1 is blocked.
        start_row: Starting row.
        start_col: Starting column.
        target_row: Target row.
        target_col: Target column.

    Returns:
        Minimum steps from start to target, or -1 if unreachable.
    """
    num_rows = len(grid)
    num_cols = len(grid[0])

    if grid[start_row][start_col] == 1 or grid[target_row][target_col] == 1:
        return -1

    visited = set()
    visited.add((start_row, start_col))
    queue = deque([(start_row, start_col, 0)])  # (row, col, distance)

    while queue:
        current_row, current_col, distance = queue.popleft()

        if current_row == target_row and current_col == target_col:
            return distance

        for neighbor_row, neighbor_col in get_grid_neighbors(
            current_row, current_col, num_rows, num_cols
        ):
            if (
                (neighbor_row, neighbor_col) not in visited
                and grid[neighbor_row][neighbor_col] == 0
            ):
                visited.add((neighbor_row, neighbor_col))
                queue.append((neighbor_row, neighbor_col, distance + 1))

    return -1
```

### Multi-Source BFS

Sometimes the shortest distance isn't from one source but from *any* of several sources simultaneously. The trick: initialize the BFS queue with ALL source nodes at distance 0. The BFS then expands outward from all sources in parallel, automatically computing the minimum distance from the nearest source for every cell.

Classic problems: Rotting Oranges (all rotten oranges spread simultaneously), 01 Matrix (distance from nearest 0).

```python
def multi_source_bfs_grid(
    grid: list[list[int]],
    source_value: int,
) -> list[list[int]]:
    """Computes minimum distance from each cell to the nearest source cell.

    Instead of running BFS from each source separately (which would be
    O(sources × V)), we enqueue ALL sources at distance 0 and run a
    single BFS. This works because BFS processes nodes in distance order,
    so the first time we reach any cell, it's via the nearest source.

    Args:
        grid: 2D grid of values.
        source_value: Value identifying source cells.

    Returns:
        2D grid where each cell contains its distance to nearest source.
    """
    num_rows = len(grid)
    num_cols = len(grid[0])
    INF = float("inf")
    distances = [[INF] * num_cols for _ in range(num_rows)]

    queue = deque()
    for row in range(num_rows):
        for col in range(num_cols):
            if grid[row][col] == source_value:
                distances[row][col] = 0
                queue.append((row, col))

    while queue:
        current_row, current_col = queue.popleft()

        for neighbor_row, neighbor_col in get_grid_neighbors(
            current_row, current_col, num_rows, num_cols
        ):
            # Only process if we found a shorter path
            new_distance = distances[current_row][current_col] + 1
            if new_distance < distances[neighbor_row][neighbor_col]:
                distances[neighbor_row][neighbor_col] = new_distance
                queue.append((neighbor_row, neighbor_col))

    return distances
```

**Complexity for all BFS variants:** O(V + E). For a grid of R rows and C columns: O(R × C), since each cell is a node and each cell has at most 4 edges.

---

## 5. DFS — Depth-First Search

### The Core Idea

DFS explores as deep as possible along one path before backtracking. Where BFS spreads wide, DFS goes deep. It uses a stack (implicit via recursion, or explicit) instead of a queue.

**The key difference from BFS:** DFS does NOT guarantee shortest paths. The first time DFS reaches a node, it may have taken a longer route. This makes DFS wrong for "minimum steps" problems but right for problems where you need to explore all paths, detect cycles, compute orderings, or find any path (not necessarily shortest).

**When to use DFS:** Cycle detection, topological sort, connected components, path existence, flood fill, backtracking/exhaustive search, anything involving "visit all" or "count components."

### Recursive DFS

```python
def dfs_recursive(
    graph: dict[int, list[int]],
    current_node: int,
    visited: set[int],
) -> None:
    """Explores all nodes reachable from current_node using DFS.

    Recursion naturally provides the stack. Each recursive call goes
    one level deeper; returning from a call backtracks one level.

    Warning: Python's default recursion limit is 1000. For graphs with
    more than ~900 nodes, use iterative DFS or increase the limit with
    sys.setrecursionlimit(). In interviews, mention this limitation
    when choosing recursive DFS.

    Args:
        graph: Adjacency list.
        current_node: Node currently being explored.
        visited: Set of already-visited nodes (mutated in place).
    """
    visited.add(current_node)
    for neighbor in graph[current_node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)
```

### Iterative DFS

```python
def dfs_iterative(
    graph: dict[int, list[int]],
    start_node: int,
) -> list[int]:
    """Explores all nodes reachable from start_node using an explicit stack.

    Unlike BFS, we check `visited` AFTER popping, not before pushing.
    Why? Because the same node may be pushed multiple times by different
    parents. We let all copies exist in the stack and skip duplicates
    when we pop. (For BFS, we check before enqueueing because BFS needs
    exactly one copy per node for its distance guarantee to hold.)

    Args:
        graph: Adjacency list.
        start_node: Node to begin traversal from.

    Returns:
        List of nodes in the order they were visited.
    """
    visited = set()
    stack = [start_node]
    visit_order = []

    while stack:
        current_node = stack.pop()
        if current_node in visited:
            continue
        visited.add(current_node)
        visit_order.append(current_node)

        for neighbor in graph[current_node]:
            if neighbor not in visited:
                stack.append(neighbor)

    return visit_order
```

### DFS Flood Fill on Grid (Number of Islands Pattern)

```python
def count_connected_components_grid(
    grid: list[list[str]],
    target_value: str = "1",
) -> int:
    """Counts connected regions of target_value cells in a grid.

    This is the "Number of Islands" pattern. The idea: scan every cell.
    When you find an unvisited target cell, that's a new component.
    Run DFS/BFS from it to mark ALL cells in that component as visited.
    The number of times you trigger a new DFS = number of components.

    Args:
        grid: 2D grid of string values.
        target_value: Value identifying cells that form components.

    Returns:
        Number of connected components of target_value cells.
    """
    if not grid:
        return 0

    num_rows = len(grid)
    num_cols = len(grid[0])
    visited = set()
    component_count = 0

    def flood_fill(start_row: int, start_col: int) -> None:
        """Marks all cells connected to (start_row, start_col) as visited."""
        stack = [(start_row, start_col)]
        visited.add((start_row, start_col))

        while stack:
            current_row, current_col = stack.pop()
            for neighbor_row, neighbor_col in get_grid_neighbors(
                current_row, current_col, num_rows, num_cols
            ):
                if (
                    (neighbor_row, neighbor_col) not in visited
                    and grid[neighbor_row][neighbor_col] == target_value
                ):
                    visited.add((neighbor_row, neighbor_col))
                    stack.append((neighbor_row, neighbor_col))

    for row in range(num_rows):
        for col in range(num_cols):
            if (row, col) not in visited and grid[row][col] == target_value:
                component_count += 1
                flood_fill(row, col)

    return component_count
```

### When BFS vs DFS? Decision Framework

Use **BFS** when the problem asks for shortest/minimum in an unweighted graph: "minimum moves," "fewest steps," "shortest transformation." BFS finds this naturally because of its layer-by-layer expansion.

Use **DFS** when the problem asks about structure: "detect cycle," "topological order," "count components," "find any path," "explore all possibilities." DFS is also the natural choice for backtracking problems where you need to try one path completely before trying another.

Both work equally well for: connected components (counting or labeling), reachability ("can node A reach node B?"), and graph traversal where order doesn't matter.

---

## 6. Topological Sort — Ordering Dependencies

### The Core Idea

Topological sort produces a linear ordering of nodes in a DAG (Directed Acyclic Graph) such that for every directed edge A→B, node A appears before node B in the ordering. Think of it as: if A must happen before B, A comes first in the output.

**Why this only works on DAGs:** If there's a cycle A→B→C→A, then A must come before B, B before C, and C before A — a contradiction. No valid ordering exists. This is also why topological sort doubles as a cycle detector: if you can't produce a complete ordering, the graph has a cycle.

**Where it shows up:** Course prerequisites ("take CS101 before CS201"), build systems (compile dependencies before dependents), task scheduling, alien dictionary (deriving character ordering from sorted words).

### Kahn's Algorithm (BFS-Based) — Prefer This in Interviews

Kahn's works by repeatedly removing nodes with zero incoming edges. The intuition: a node with in-degree 0 has no unmet dependencies, so it can go next. After "removing" it (adding to result and decrementing neighbors' in-degrees), new nodes may become dependency-free. This continues until all nodes are processed (success) or we get stuck (cycle detected).

```python
from collections import deque, defaultdict


def topological_sort_kahn(
    num_nodes: int,
    edges: list[tuple[int, int]],
) -> list[int]:
    """Returns a valid topological ordering using Kahn's BFS-based algorithm.

    The algorithm works by maintaining an in-degree count for every node.
    Nodes with in-degree 0 have no unmet prerequisites, so they can be
    processed next. When we "process" a node, we reduce the in-degree
    of all its neighbors (simulating removal of that node's outgoing
    edges). Any neighbor whose in-degree drops to 0 becomes eligible.

    If we process all nodes, we have a valid ordering. If we get stuck
    with remaining nodes all having in-degree > 0, a cycle exists.

    Why Kahn's over DFS-based: Kahn's naturally provides cycle detection
    (check output length), is iterative (no recursion limit issues),
    and the "remove zero-dependency nodes" logic maps directly to how
    interviewers think about scheduling problems.

    Args:
        num_nodes: Total number of nodes (0-indexed).
        edges: List of (prerequisite, dependent) directed edges.

    Returns:
        List of nodes in topological order.
        Empty list if a cycle exists (no valid ordering possible).
    """
    adjacency = defaultdict(list)
    in_degree = [0] * num_nodes

    for prerequisite, dependent in edges:
        adjacency[prerequisite].append(dependent)
        in_degree[dependent] += 1

    # Start with all nodes that have no prerequisites
    ready_queue = deque(
        node for node in range(num_nodes) if in_degree[node] == 0
    )
    topological_order = []

    while ready_queue:
        current_node = ready_queue.popleft()
        topological_order.append(current_node)

        for neighbor in adjacency[current_node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                ready_queue.append(neighbor)

    # If we couldn't process all nodes, a cycle blocks the remaining ones
    if len(topological_order) != num_nodes:
        return []  # Cycle detected
    return topological_order
```

### DFS-Based Topological Sort

DFS-based topological sort uses post-order: add a node to the result AFTER all its descendants are fully explored. Then reverse the result. The intuition: if A→B exists, DFS finishes B before A (since B is deeper), so B appears earlier in post-order. Reversing gives A before B.

```python
def topological_sort_dfs(
    num_nodes: int,
    edges: list[tuple[int, int]],
) -> list[int]:
    """Returns a valid topological ordering using DFS post-order reversal.

    For each unvisited node, we DFS to its deepest descendants first.
    A node is added to the result only after ALL of its descendants
    have been added (post-order). This guarantees that every node
    appears after all its dependents. Reversing gives a valid
    topological order.

    Args:
        num_nodes: Total number of nodes (0-indexed).
        edges: List of (source, destination) directed edges.

    Returns:
        List of nodes in topological order.
    """
    adjacency = defaultdict(list)
    for source, destination in edges:
        adjacency[source].append(destination)

    visited = set()
    reverse_order = []  # Nodes in reverse topological order

    def dfs_post_order(node: int) -> None:
        visited.add(node)
        for neighbor in adjacency[node]:
            if neighbor not in visited:
                dfs_post_order(neighbor)
        reverse_order.append(node)  # Add AFTER all descendants are done

    for node in range(num_nodes):
        if node not in visited:
            dfs_post_order(node)

    return reverse_order[::-1]
```

**Complexity:** O(V + E) for both variants.

---

## 7. Cycle Detection

### Undirected Graph — Parent Tracking

In an undirected graph, every edge creates a trivial "cycle" of length 2 (A↔B). We exclude this by tracking each node's parent (the node that discovered it). A real cycle exists when DFS finds an edge to an already-visited node that ISN'T the parent.

```python
def has_cycle_undirected(
    adjacency: dict[int, list[int]],
    num_nodes: int,
) -> bool:
    """Detects whether an undirected graph contains a cycle.

    Uses DFS with parent tracking. During traversal, if we encounter
    an already-visited neighbor that is NOT the node we came from
    (the parent), we've found a back edge — proof of a cycle.

    We loop over all nodes as starting points to handle disconnected
    graphs. A graph might have multiple components, some acyclic and
    some containing cycles.

    Args:
        adjacency: Undirected graph as adjacency list.
        num_nodes: Total number of nodes.

    Returns:
        True if any cycle exists, False otherwise.
    """
    visited = set()

    def dfs_detect_cycle(current_node: int, parent_node: int) -> bool:
        visited.add(current_node)
        for neighbor in adjacency[current_node]:
            if neighbor not in visited:
                if dfs_detect_cycle(neighbor, current_node):
                    return True
            elif neighbor != parent_node:
                # Visited neighbor that isn't our parent → back edge → cycle
                return True
        return False

    for node in range(num_nodes):
        if node not in visited:
            if dfs_detect_cycle(node, parent_node=-1):
                return True
    return False
```

### Directed Graph — Three-Color (White/Gray/Black)

Undirected parent tracking doesn't work for directed graphs because edge direction matters. Instead, we use three states per node:

- **White (0):** Not yet visited.
- **Gray (1):** Currently being explored (on the current DFS path).
- **Black (2):** Fully explored (all descendants finished).

A cycle exists if and only if DFS encounters a Gray node — meaning we've found a path back to a node that's still on our current exploration path.

```python
def has_cycle_directed(
    adjacency: dict[int, list[int]],
    num_nodes: int,
) -> bool:
    """Detects whether a directed graph contains a cycle using 3-color DFS.

    WHITE (0): Unvisited.
    GRAY (1): In the current DFS path (between entry and exit).
    BLACK (2): Fully explored, including all descendants.

    A back edge to a GRAY node proves a cycle: it means we've found
    a path from a node back to one of its own ancestors in the current
    DFS tree.

    A cross edge to a BLACK node is harmless — it reaches a fully
    explored subtree, not our current path.

    Args:
        adjacency: Directed graph as adjacency list.
        num_nodes: Total number of nodes.

    Returns:
        True if any cycle exists, False otherwise.
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    node_color = [WHITE] * num_nodes

    def dfs_detect_cycle(node: int) -> bool:
        node_color[node] = GRAY  # Entering this node's DFS subtree
        for neighbor in adjacency[node]:
            if node_color[neighbor] == GRAY:
                return True  # Back edge to ancestor → cycle
            if node_color[neighbor] == WHITE:
                if dfs_detect_cycle(neighbor):
                    return True
        node_color[node] = BLACK  # All descendants fully explored
        return False

    for node in range(num_nodes):
        if node_color[node] == WHITE:
            if dfs_detect_cycle(node):
                return True
    return False
```

---

## 8. Union-Find (Disjoint Set Union)

### The Core Idea

Union-Find maintains a collection of disjoint sets and supports two operations: **find** (which set does this element belong to?) and **union** (merge two sets). It answers the question "are these two elements connected?" in nearly O(1) time.

**Why it matters:** Union-Find solves connectivity problems where elements are dynamically connected. Problems like "is adding this edge redundant?" or "at what point does the graph become connected?" are natural fits.

**Two optimizations that make it fast:**

1. **Path compression:** When finding the root of a set, make every node on the path point directly to the root. This flattens the tree so future finds are O(1).

2. **Union by rank:** When merging two sets, attach the shorter tree under the taller tree. This keeps the tree balanced, preventing degenerate chains.

With both optimizations, each operation runs in O(α(n)) amortized time, where α is the inverse Ackermann function — effectively constant for all practical input sizes.

```python
class UnionFind:
    """Disjoint Set Union with path compression and union by rank.

    Tracks connected components. Each element starts in its own set.
    Union merges two sets. Find returns the representative (root)
    of an element's set. Two elements are in the same set if and
    only if they have the same root.

    Attributes:
        parent: Maps each element to its parent. Root elements are
            their own parent.
        rank: Upper bound on the height of each element's subtree.
            Used to keep the tree balanced during unions.
        num_components: Current number of disjoint sets.
    """

    def __init__(self, size: int) -> None:
        self.parent = list(range(size))  # Each node is its own root
        self.rank = [0] * size
        self.num_components = size

    def find(self, element: int) -> int:
        """Returns the root representative of the set containing element.

        Uses path compression: after finding the root, every node on
        the path from element to root is updated to point directly
        to the root. This means future find() calls for any of those
        nodes are O(1).
        """
        if self.parent[element] != element:
            self.parent[element] = self.find(self.parent[element])
        return self.parent[element]

    def union(self, element_a: int, element_b: int) -> bool:
        """Merges the sets containing element_a and element_b.

        Uses union by rank: the shorter tree is attached under the
        taller tree's root. This prevents the tree from degenerating
        into a linked list (which would make find() O(n)).

        Returns:
            True if a merge happened (elements were in different sets).
            False if they were already in the same set (meaning this
            edge is redundant — useful for cycle detection).
        """
        root_a = self.find(element_a)
        root_b = self.find(element_b)

        if root_a == root_b:
            return False  # Already connected — edge is redundant

        # Attach shorter tree under taller tree
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a

        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1

        self.num_components -= 1
        return True

    def are_connected(self, element_a: int, element_b: int) -> bool:
        """Checks whether two elements belong to the same set."""
        return self.find(element_a) == self.find(element_b)
```

**Interview signal:** If the problem says "connect nodes" and "are they connected?" without needing path information, Union-Find is almost always the right choice over BFS/DFS. It's also the backbone of Kruskal's MST algorithm.

---

## 9. Shortest Path Algorithms

### 9.1 Dijkstra's Algorithm — Non-Negative Weights

Dijkstra's is BFS generalized to weighted graphs. Instead of a plain queue (which processes nodes in discovery order), it uses a min-heap (priority queue) that always processes the node with the smallest known distance.

**Why it works:** At each step, the node with the smallest tentative distance is guaranteed to have its final shortest distance. No future path through other nodes could be shorter, because all edge weights are non-negative. This "greedy" property is what makes Dijkstra's correct — and exactly why it fails with negative weights.

**Why not just use BFS?** BFS treats all edges as cost 1. With varying weights, a path through more edges might cost less than a path through fewer edges. BFS can't detect this because it doesn't consider edge weights.

```python
import heapq


def dijkstra_shortest_distances(
    adjacency: dict[int, list[tuple[int, int]]],
    start_node: int,
    num_nodes: int,
) -> list[float]:
    """Computes shortest distances from start_node to all other nodes.

    Uses a min-heap to always expand the node with the smallest known
    distance. When we pop a node, its distance is final (proof: any
    alternative path would go through nodes with >= current distance,
    and all edges add non-negative weight, so the alternative total
    cost >= current cost).

    The "stale entry" check (current_distance > shortest_distance[node])
    is critical. We can't efficiently delete outdated heap entries when
    we find a shorter path, so we push the new shorter entry and skip
    outdated ones when we pop them. This is called "lazy deletion."

    Args:
        adjacency: Weighted directed graph as adjacency list.
            adjacency[node] = [(neighbor, edge_weight), ...]
        start_node: Source node.
        num_nodes: Total number of nodes.

    Returns:
        List where shortest_distance[i] = shortest distance from
        start_node to node i. float('inf') if unreachable.
    """
    shortest_distance = [float("inf")] * num_nodes
    shortest_distance[start_node] = 0
    min_heap = [(0, start_node)]  # (distance, node)

    while min_heap:
        current_distance, current_node = heapq.heappop(min_heap)

        # Skip stale entries — we already found a shorter path
        if current_distance > shortest_distance[current_node]:
            continue

        for neighbor, edge_weight in adjacency[current_node]:
            new_distance = current_distance + edge_weight
            if new_distance < shortest_distance[neighbor]:
                shortest_distance[neighbor] = new_distance
                heapq.heappush(min_heap, (new_distance, neighbor))

    return shortest_distance
```

**Complexity:** O((V + E) × log V) with a binary heap. The log V comes from heap push/pop operations. For dense graphs where E ≈ V², this becomes O(V² log V). An adjacency matrix + linear scan (no heap) gives O(V²), which is better for dense graphs — but in interviews, the heap version is almost always expected.

### 9.2 Bellman-Ford — Handles Negative Weights

Bellman-Ford is simpler and slower than Dijkstra's, but it handles negative edge weights. It works by "relaxing" every edge V-1 times. The logic: the shortest path between any two nodes has at most V-1 edges (otherwise it contains a cycle). After k relaxation rounds, all shortest paths using at most k edges are correct. So after V-1 rounds, all shortest paths are correct.

**Negative cycle detection:** After V-1 rounds, one more round of relaxation should change nothing. If any distance decreases in round V, a negative cycle exists (a cycle whose total weight is negative, allowing infinite cost reduction).

```python
def bellman_ford_shortest_distances(
    edges: list[tuple[int, int, int]],
    num_nodes: int,
    start_node: int,
) -> list[float] | None:
    """Computes shortest distances from start_node, handling negative weights.

    Runs V-1 relaxation passes over all edges. Each pass guarantees
    that shortest paths using one more edge are discovered. Since the
    longest acyclic path has V-1 edges, V-1 passes suffice.

    A Vth pass detects negative cycles: if any distance still decreases,
    a negative cycle is reachable from start_node.

    Args:
        edges: List of (source, destination, weight) triples.
        num_nodes: Total number of nodes.
        start_node: Source node.

    Returns:
        List of shortest distances, or None if a negative cycle exists.
    """
    shortest_distance = [float("inf")] * num_nodes
    shortest_distance[start_node] = 0

    # Relax all edges V-1 times
    for pass_number in range(num_nodes - 1):
        updated = False
        for source, destination, weight in edges:
            if (
                shortest_distance[source] != float("inf")
                and shortest_distance[source] + weight
                < shortest_distance[destination]
            ):
                shortest_distance[destination] = (
                    shortest_distance[source] + weight
                )
                updated = True
        # Optimization: if no update in this pass, we're done early
        if not updated:
            break

    # Vth pass — check for negative cycles
    for source, destination, weight in edges:
        if (
            shortest_distance[source] != float("inf")
            and shortest_distance[source] + weight
            < shortest_distance[destination]
        ):
            return None  # Negative cycle detected

    return shortest_distance
```

**Complexity:** O(V × E). Much slower than Dijkstra's, but necessary when negative weights exist.

### 9.3 Floyd-Warshall — All-Pairs Shortest Path

Floyd-Warshall computes shortest distances between EVERY pair of nodes. It uses dynamic programming with the recurrence: "the shortest path from i to j either goes through intermediate node k or it doesn't."

**When to use:** When the problem asks for shortest path between ALL pairs, and V is small (≤ 400). For single-source shortest path, Dijkstra's or Bellman-Ford is faster.

```python
def floyd_warshall_all_pairs(
    num_nodes: int,
    edges: list[tuple[int, int, int]],
) -> list[list[float]]:
    """Computes shortest distance between every pair of nodes.

    DP recurrence: dist[i][j] through nodes {0..k} =
        min(dist[i][j] through {0..k-1},
            dist[i][k] through {0..k-1} + dist[k][j] through {0..k-1})

    In plain English: for each potential intermediate node k, check
    if routing through k gives a shorter path than the best known
    path that doesn't use k.

    The triple loop order MUST be k (outermost), then i, then j.
    This is because the DP state depends on having fully processed
    all pairs for intermediate nodes {0..k-1} before considering k.

    Args:
        num_nodes: Total number of nodes.
        edges: List of (source, destination, weight) triples.

    Returns:
        V×V matrix where result[i][j] = shortest distance from i to j.
    """
    INF = float("inf")
    distance = [[INF] * num_nodes for _ in range(num_nodes)]

    for node in range(num_nodes):
        distance[node][node] = 0
    for source, destination, weight in edges:
        distance[source][destination] = weight

    # k MUST be the outermost loop
    for intermediate in range(num_nodes):
        for origin in range(num_nodes):
            for destination in range(num_nodes):
                through_intermediate = (
                    distance[origin][intermediate]
                    + distance[intermediate][destination]
                )
                if through_intermediate < distance[origin][destination]:
                    distance[origin][destination] = through_intermediate

    return distance
```

**Complexity:** O(V³). Only viable when V ≤ ~400.

### 9.4 0-1 BFS — When Edge Weights Are Only 0 or 1

A special case that's faster than Dijkstra's. Uses a deque instead of a heap: 0-weight edges push to the front (maintaining current distance layer), 1-weight edges push to the back (next distance layer). This preserves BFS's distance ordering property without the O(log V) heap overhead.

```python
from collections import deque


def zero_one_bfs_shortest_distances(
    adjacency: dict[int, list[tuple[int, int]]],
    start_node: int,
    num_nodes: int,
) -> list[float]:
    """Shortest distances when all edge weights are 0 or 1.

    Uses a deque (double-ended queue) instead of a heap.
    0-weight edges: neighbor goes to FRONT of deque (same distance layer).
    1-weight edges: neighbor goes to BACK of deque (next distance layer).

    This maintains the invariant that the deque is sorted by distance,
    which is exactly what Dijkstra's heap provides — but in O(1) per
    operation instead of O(log V).

    Args:
        adjacency: Graph with edge weights restricted to 0 or 1.
            adjacency[node] = [(neighbor, weight), ...] where weight ∈ {0, 1}.
        start_node: Source node.
        num_nodes: Total number of nodes.

    Returns:
        List of shortest distances from start_node.
    """
    shortest_distance = [float("inf")] * num_nodes
    shortest_distance[start_node] = 0
    double_ended_queue = deque([start_node])

    while double_ended_queue:
        current_node = double_ended_queue.popleft()

        for neighbor, edge_weight in adjacency[current_node]:
            new_distance = shortest_distance[current_node] + edge_weight
            if new_distance < shortest_distance[neighbor]:
                shortest_distance[neighbor] = new_distance
                if edge_weight == 0:
                    double_ended_queue.appendleft(neighbor)  # Same layer
                else:
                    double_ended_queue.append(neighbor)  # Next layer

    return shortest_distance
```

**Complexity:** O(V + E). Strictly faster than Dijkstra's O((V+E) log V).

### Algorithm Selection

- **Unweighted graph:** BFS. Always. It's O(V + E) and guarantees shortest path.
- **Weighted, no negative edges:** Dijkstra's. O((V + E) log V).
- **Weighted, has negative edges:** Bellman-Ford. O(V × E).
- **Need all-pairs distances, V ≤ 400:** Floyd-Warshall. O(V³).
- **Weights are only 0 and 1:** 0-1 BFS. O(V + E).

---

## 10. Minimum Spanning Tree

An MST connects all nodes in an undirected weighted graph with the minimum total edge weight. It uses exactly V-1 edges (a tree on V nodes) and has no cycles.

### Kruskal's Algorithm — Sort Edges + Union-Find

Kruskal's is greedy: sort all edges by weight, then add them one by one, skipping any edge that would create a cycle. Union-Find handles the cycle check — if both endpoints are already in the same component, the edge is redundant.

```python
def kruskal_mst_cost(
    num_nodes: int,
    edges: list[tuple[int, int, int]],
) -> int | None:
    """Computes the total weight of the Minimum Spanning Tree.

    Greedy approach: process edges in ascending weight order. Add an
    edge if it connects two previously-disconnected components (checked
    via Union-Find). Skip it if both endpoints are already connected
    (adding it would create a cycle).

    This works because of the Cut Property: for any cut of the graph,
    the lightest edge crossing the cut is always in some MST. By
    processing edges lightest-first, we're always picking the lightest
    edge that crosses some cut.

    Args:
        num_nodes: Total number of nodes.
        edges: List of (node_a, node_b, weight) triples.

    Returns:
        Total MST weight, or None if graph is disconnected.
    """
    sorted_edges = sorted(edges, key=lambda edge: edge[2])
    union_find = UnionFind(num_nodes)
    total_mst_weight = 0
    edges_added = 0

    for node_a, node_b, weight in sorted_edges:
        if union_find.union(node_a, node_b):
            total_mst_weight += weight
            edges_added += 1
            if edges_added == num_nodes - 1:
                break  # MST is complete

    if edges_added != num_nodes - 1:
        return None  # Graph is disconnected — no spanning tree exists
    return total_mst_weight
```

**Complexity:** O(E log E) for the sort, nearly O(E) for Union-Find operations. Total: O(E log E).

### Prim's Algorithm — Grow MST from One Node

Prim's starts from an arbitrary node and greedily adds the cheapest edge that connects the current MST to a non-MST node. Uses a min-heap to efficiently find the cheapest edge.

```python
def prim_mst_cost(
    adjacency: dict[int, list[tuple[int, int]]],
    num_nodes: int,
) -> int:
    """Computes MST weight using Prim's algorithm.

    Starts from node 0 and grows the MST one edge at a time.
    At each step, picks the cheapest edge from any MST node to
    any non-MST node. The min-heap stores candidate edges as
    (weight, destination) and lazy-deletes stale entries.

    Args:
        adjacency: Undirected weighted graph.
            adjacency[node] = [(neighbor, weight), ...]
        num_nodes: Total number of nodes.

    Returns:
        Total MST weight.
    """
    in_mst = [False] * num_nodes
    min_heap = [(0, 0)]  # (edge_weight, node) — start from node 0 at cost 0
    total_mst_weight = 0

    while min_heap:
        edge_weight, current_node = heapq.heappop(min_heap)
        if in_mst[current_node]:
            continue  # Already in MST — stale heap entry
        in_mst[current_node] = True
        total_mst_weight += edge_weight

        for neighbor, weight in adjacency[current_node]:
            if not in_mst[neighbor]:
                heapq.heappush(min_heap, (weight, neighbor))

    return total_mst_weight
```

**Complexity:** O(E log V).

**Kruskal's vs Prim's:** Kruskal's is edge-centric (sort edges, use Union-Find). Better for sparse graphs or when you already have an edge list. Prim's is node-centric (grow from a starting node). Better for dense graphs or when you have an adjacency list. In interviews, either is fine — pick the one you can write faster.

---

## 11. Advanced Patterns — Google L5/L6 Favorites

### 11.1 Bipartite Check (2-Coloring)

A graph is bipartite if you can color every node with one of two colors such that no two adjacent nodes share the same color. Equivalent to: "can the nodes be split into two groups where edges only go between groups, never within a group?"

Uses BFS with alternating colors. If we ever need to color a neighbor the same color as the current node, the graph isn't bipartite.

```python
def is_bipartite(
    adjacency: dict[int, list[int]],
    num_nodes: int,
) -> bool:
    """Determines whether an undirected graph is bipartite.

    Uses BFS coloring. Assign the start node color 0. All its
    neighbors get color 1. All their uncolored neighbors get color 0.
    And so on. If we ever try to color a neighbor that already has
    the SAME color as the current node, the graph contains an
    odd-length cycle and is NOT bipartite.

    Args:
        adjacency: Undirected graph as adjacency list.
        num_nodes: Total number of nodes.

    Returns:
        True if the graph is bipartite, False otherwise.
    """
    NO_COLOR = -1
    node_color = [NO_COLOR] * num_nodes

    for start_node in range(num_nodes):
        if node_color[start_node] != NO_COLOR:
            continue  # Already colored in a previous component

        node_color[start_node] = 0
        queue = deque([start_node])

        while queue:
            current_node = queue.popleft()
            for neighbor in adjacency[current_node]:
                if node_color[neighbor] == NO_COLOR:
                    node_color[neighbor] = 1 - node_color[current_node]
                    queue.append(neighbor)
                elif node_color[neighbor] == node_color[current_node]:
                    return False  # Same color on both sides of edge

    return True
```

### 11.2 BFS with Compound State — The #1 Google Pattern

This is the pattern that separates strong candidates from average ones. The graph's nodes aren't simple positions — they're tuples encoding all relevant state. Each valid transition is an edge.

**Example:** Shortest path in a grid where you can destroy at most `max_obstacles` walls. The state isn't just `(row, col)` — it's `(row, col, obstacles_remaining)`. Two entries at the same cell but with different obstacles_remaining are DIFFERENT nodes. A path that used 2 destructions is fundamentally different from one that used 0, even if both are at the same cell.

```python
def shortest_path_with_obstacle_limit(
    grid: list[list[int]],
    max_obstacles: int,
) -> int:
    """Shortest path in grid from top-left to bottom-right, breaking at most
    max_obstacles walls.

    Grid values: 0 = open cell, 1 = wall/obstacle.

    The state for BFS is (row, col, obstacles_remaining). This is NOT
    the same as running BFS on (row, col) — because arriving at the
    same cell with different remaining obstacle budget opens different
    future possibilities. We need the full state in our visited set.

    Why BFS works here: every move costs exactly 1 step (unweighted),
    so BFS still guarantees shortest path. The graph is just larger:
    instead of R×C nodes, we have R×C×(max_obstacles+1) nodes.

    Args:
        grid: 2D grid where 0 = open, 1 = obstacle.
        max_obstacles: Maximum number of obstacles we can destroy.

    Returns:
        Minimum steps from (0,0) to (rows-1, cols-1), or -1 if impossible.
    """
    num_rows = len(grid)
    num_cols = len(grid[0])

    # State: (row, col, obstacles_remaining)
    start_state = (0, 0, max_obstacles)
    visited = {start_state}
    queue = deque([(0, 0, max_obstacles, 0)])  # row, col, obstacles_left, steps

    while queue:
        current_row, current_col, obstacles_left, steps = queue.popleft()

        if current_row == num_rows - 1 and current_col == num_cols - 1:
            return steps

        for neighbor_row, neighbor_col in get_grid_neighbors(
            current_row, current_col, num_rows, num_cols
        ):
            cell_is_obstacle = grid[neighbor_row][neighbor_col] == 1
            new_obstacles_left = obstacles_left - cell_is_obstacle

            if new_obstacles_left >= 0:
                next_state = (neighbor_row, neighbor_col, new_obstacles_left)
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((
                        neighbor_row,
                        neighbor_col,
                        new_obstacles_left,
                        steps + 1,
                    ))

    return -1
```

### 11.3 Alien Dictionary — Topological Sort on Characters

Given a sorted list of words in an alien language, derive the character ordering. Each adjacent word pair gives one edge: the first differing character in word[i] must come before the first differing character in word[i+1].

```python
def derive_alien_character_order(
    sorted_words: list[str],
) -> str:
    """Derives character ordering from a list of words sorted in alien order.

    For each consecutive pair of words, find the first position where
    characters differ. This gives us one ordering constraint:
    char_in_word1 comes before char_in_word2 in the alien alphabet.

    Edge case: if word1 is a prefix of word2 but longer (e.g., "abc"
    before "ab"), the input is invalid — a prefix must come first.

    After extracting all constraints, run topological sort. If a valid
    ordering exists, it's the alien alphabet. If not, the input is
    contradictory (contains a cycle in character dependencies).

    Args:
        sorted_words: Words sorted according to the alien alphabet.

    Returns:
        String of characters in alien alphabetical order.
        Empty string if no valid ordering exists.
    """
    # Collect all unique characters
    adjacency: dict[str, set[str]] = defaultdict(set)
    in_degree: dict[str, int] = {
        char: 0 for word in sorted_words for char in word
    }

    # Extract ordering constraints from consecutive word pairs
    for word_index in range(len(sorted_words) - 1):
        current_word = sorted_words[word_index]
        next_word = sorted_words[word_index + 1]
        shorter_length = min(len(current_word), len(next_word))

        # Invalid: longer word is prefix of shorter word but appears first
        if (
            current_word[:shorter_length] == next_word[:shorter_length]
            and len(current_word) > len(next_word)
        ):
            return ""

        for char_index in range(shorter_length):
            char_before = current_word[char_index]
            char_after = next_word[char_index]
            if char_before != char_after:
                if char_after not in adjacency[char_before]:
                    adjacency[char_before].add(char_after)
                    in_degree[char_after] += 1
                break  # Only the first difference gives information

    # Topological sort via Kahn's algorithm
    ready_queue = deque(
        char for char, degree in in_degree.items() if degree == 0
    )
    character_order = []

    while ready_queue:
        current_char = ready_queue.popleft()
        character_order.append(current_char)
        for neighbor_char in adjacency[current_char]:
            in_degree[neighbor_char] -= 1
            if in_degree[neighbor_char] == 0:
                ready_queue.append(neighbor_char)

    if len(character_order) != len(in_degree):
        return ""  # Cycle in dependencies — contradictory input
    return "".join(character_order)
```

### 11.4 Word Ladder — BFS on Implicit String Graph

Each word is a node. Two words are connected if they differ by exactly one character. BFS finds the shortest transformation sequence.

```python
def word_ladder_length(
    begin_word: str,
    end_word: str,
    word_list: list[str],
) -> int:
    """Finds shortest transformation sequence from begin_word to end_word.

    Each step changes exactly one character, and the resulting word must
    be in word_list. This is BFS on an implicit graph where:
    - Nodes = words
    - Edges = single-character differences

    Instead of precomputing all edges (O(n² × word_length)), we generate
    neighbors on the fly: for each position, try all 26 characters and
    check if the result is in our word set. This is O(26 × word_length)
    per node, which is faster when the word list is large.

    Args:
        begin_word: Starting word.
        end_word: Target word.
        word_list: Dictionary of valid words.

    Returns:
        Length of shortest transformation sequence (including start and
        end words), or 0 if no valid sequence exists.
    """
    valid_words = set(word_list)
    if end_word not in valid_words:
        return 0

    visited = {begin_word}
    queue = deque([(begin_word, 1)])  # (current_word, sequence_length)

    while queue:
        current_word, sequence_length = queue.popleft()

        for char_index in range(len(current_word)):
            for replacement in "abcdefghijklmnopqrstuvwxyz":
                candidate_word = (
                    current_word[:char_index]
                    + replacement
                    + current_word[char_index + 1 :]
                )
                if candidate_word == end_word:
                    return sequence_length + 1
                if (
                    candidate_word in valid_words
                    and candidate_word not in visited
                ):
                    visited.add(candidate_word)
                    queue.append((candidate_word, sequence_length + 1))

    return 0
```

---

## 12. Problem Recognition Cheat Sheet

**"Shortest path" / "minimum moves" (unweighted):** BFS.

**"Shortest path" (weighted, positive):** Dijkstra's.

**"Shortest path" (negative weights):** Bellman-Ford.

**Grid with obstacles, find path:** BFS on grid.

**"Number of islands" / "connected regions":** DFS or BFS flood fill, or Union-Find.

**"Course schedule" / "prerequisite order":** Topological Sort.

**"Detect cycle":** DFS — 3-color for directed, parent-tracking for undirected.

**"Minimum cost to connect all nodes":** MST via Kruskal's or Prim's.

**"Can we split into two groups?":** Bipartite check via BFS coloring.

**"Transform X to Y with minimum steps":** BFS on implicit graph.

**"Connect/disconnect dynamically":** Union-Find.

**"Shortest path with constraints" (keys, walls, fuel):** BFS on compound state `(position, constraint)`.

**"All pairs shortest path" with small V:** Floyd-Warshall.

**"Network delay" / "cheapest flights":** Dijkstra or Bellman-Ford depending on weight signs.

---

## 13. Practice Problems — Priority Order

### Tier 1: Foundations (Do These First)

200 Number of Islands — DFS/BFS flood fill.
133 Clone Graph — DFS + hashmap for visited tracking.
207 Course Schedule — Topological sort / cycle detection.
210 Course Schedule II — Topological sort (output the order).
994 Rotting Oranges — Multi-source BFS.
547 Number of Provinces — DFS or Union-Find.

### Tier 2: Core Patterns

127 Word Ladder — BFS on implicit string graph.
743 Network Delay Time — Dijkstra's.
785 Is Graph Bipartite? — BFS 2-coloring.
323 Number of Connected Components — Union-Find.
261 Graph Valid Tree — Union-Find (check: V-1 edges + no cycle).
684 Redundant Connection — Union-Find (find the edge that creates a cycle).

### Tier 3: Google L5/L6 Level

269 Alien Dictionary — Topological sort on character constraints.
787 Cheapest Flights Within K Stops — Bellman-Ford or BFS with state.
1293 Shortest Path in Grid with Obstacles — BFS with compound state.
1091 Shortest Path in Binary Matrix — BFS on 8-directional grid.
815 Bus Routes — BFS where routes are nodes.
1368 Min Cost to Make Valid Path — 0-1 BFS.
332 Reconstruct Itinerary — Eulerian path via Hierholzer's algorithm.
1192 Critical Connections — Tarjan's bridge-finding algorithm.
399 Evaluate Division — Weighted graph DFS/BFS.
882 Reachable Nodes in Subdivided Graph — Modified Dijkstra's.

---

## 14. Common Mistakes That Cost Offers

**Marking visited after dequeue instead of at enqueue time.** In BFS, a node should be marked visited the moment it enters the queue, not when it's removed. If you mark at dequeue time, multiple parents can enqueue the same node before any of them processes it. Correctness is preserved but time/space blows up. Interviewers notice.

**Using DFS for shortest path.** DFS does not guarantee shortest path in unweighted graphs. It explores depth-first, so it might find a longer path first. If the problem says "minimum" or "shortest," use BFS.

**Not handling disconnected components.** If the graph might not be connected, you must loop over all nodes as potential DFS/BFS starting points. A single `bfs(0)` misses all components not connected to node 0.

**Confusing undirected and directed cycle detection.** Parent-tracking only works for undirected graphs. For directed graphs, you need the 3-color (white/gray/black) approach because edge direction changes what constitutes a "back edge."

**Using a visited set instead of the stale-entry check with Dijkstra.** The pattern `if current_distance > shortest_distance[node]: continue` is correct. A simpler visited-set approach works but is less standard and can miss updates in certain edge cases with how Python's heapq handles equal distances.

**Forgetting that Dijkstra fails with negative weights.** Dijkstra's greedy assumption ("the smallest tentative distance is final") breaks when negative weights can reduce a path cost after it was finalized. If you see negative costs, switch to Bellman-Ford.

**Wrong state in the visited set.** If BFS has compound state `(position, constraint)`, your visited set must track the full state. Tracking only `position` collapses states that are fundamentally different and leads to wrong answers. This is the most common bug in state-space BFS problems.
