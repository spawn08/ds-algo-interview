# Graphs — Prerequisites & How to Actually Solve Graph Problems

> Graph problems feel scary because the input doesn't *look* like a graph. It looks
> like a grid, a list of pairs, a matrix, or a list of course dependencies. **Step 1
> of every graph problem is recognising "this is a graph" and turning it into one.**
> Once you have a graph + you know BFS/DFS, you are 80% done.
>
> A tree is just a graph with no cycles and one path between any two nodes. So
> everything you learned in `../trees/PREREQUISITES.md` still applies — graphs just
> add two complications: **cycles** (so you must track *visited*) and **multiple
> ways to represent the graph**. Read the tree guide first if you haven't.

---

## Part 0 — The mental model

Almost every graph problem is one of these:

1. **Reachability / connectivity** — "can I get from A to B?", "how many separate
   groups?", "how many islands?" → **DFS or BFS flood fill.**
2. **Shortest path** — "fewest steps", "minimum cost", "nearest" →
   **BFS** (unweighted) or **Dijkstra** (weighted).
3. **Ordering with dependencies** — "course schedule", "build order", "is there a
   cycle?" → **Topological sort (Kahn's algorithm) / cycle detection.**
4. **Minimum spanning tree** — "connect everything as cheaply as possible" →
   **Prim's / Kruskal's.**

When you read a problem, your **first job** is to map it to one of these four. The
rest of this guide teaches you how.

---

## Part 1 — The 2 things that make graphs different from trees

### Difference 1: You MUST track visited nodes

A tree can't loop back on itself. A graph can. If you DFS a graph without remembering
where you've been, you loop forever. **The single most common graph bug is forgetting
the `visited` set.**

```python
visited = set()
def dfs(node):
    if node in visited:      # <-- without this line, infinite loop
        return
    visited.add(node)
    for neighbour in graph[node]:
        dfs(neighbour)
```

> **Rule:** Every graph traversal needs a `visited` set (or a `visited` grid for 2D
> problems). No exceptions.

### Difference 2: A graph can come in many disguises — you convert it first

This is the skill that's actually missing when you "can't start." The graph is rarely
handed to you as `{node: [neighbours]}`. You have to **build that** from the input.
Learn to recognise these four input formats:

#### (a) Adjacency list — the canonical form (what you convert *to*)
```python
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0],
    3: [1],
}
```
This is the format `graph_traversal.py` uses. When the graph is given another way,
your first step is usually to build this dict (often a `defaultdict(list)`).

#### (b) Edge list → build adjacency list
Input: `edges = [[0,1], [0,2], [1,3]]` and `n` nodes.
```python
from collections import defaultdict
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)        # add BOTH directions if UNDIRECTED; one if DIRECTED
```
**The directed-vs-undirected decision lives in this loop.** Get it wrong and
everything downstream breaks. Ask: "if A connects to B, does B connect to A?" Yes →
undirected → add both.

#### (c) Adjacency matrix → neighbours are columns that equal 1
Input: `isConnected[i][j] == 1` means i–j are connected (see `number_of_provinces.py`).
You often don't even build a list — you just loop columns:
```python
for neighbour in range(n):
    if isConnected[node][neighbour] == 1 and neighbour not in visited:
        ...
```

#### (d) A 2D grid IS a graph (this trips everyone up)
In grid problems (`number_of_island.py`), **each cell is a node**, and its
**neighbours are the (up, down, left, right) cells**. There is no `graph` dict — the
grid *is* the adjacency structure. The neighbour pattern:
```python
rows, cols = len(grid), len(grid[0])
for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:   # up, down, left, right
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
        ...   # (nr, nc) is a valid neighbour
```
Memorise the four `(dr, dc)` deltas and the bounds check. You'll write them a hundred
times. (Add the 4 diagonals if the problem says "8-directionally connected".)

---

## Part 2 — The 2 core traversals (memorise both exactly)

These are the hammer for almost everything. Working code: `graph_traversal.py`.

### BFS — queue, explores level by level (use for SHORTEST PATH in unweighted graphs)
```python
from collections import deque

def bfs(graph, start):
    visited = {start}                    # mark when you ENQUEUE, not when you dequeue
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
```
> **Critical subtlety:** mark a node visited the moment you **add it to the queue**,
> not when you pop it. Otherwise the same node gets enqueued multiple times before
> it's processed.

### DFS — stack or recursion, dives deep (use for connectivity / "explore everything")
```python
# Recursive
def dfs(graph, node, visited):
    visited.add(node)
    for neighbour in graph[node]:
        if neighbour not in visited:
            dfs(graph, neighbour, visited)

# Iterative (when recursion depth might blow the stack)
def dfs_iter(graph, start):
    visited = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                stack.append(neighbour)
```

### BFS vs DFS — which do I pick?

| If the problem asks…                          | Use            |
|-----------------------------------------------|----------------|
| Shortest path / fewest moves (unweighted)     | **BFS**        |
| "Is everything connected?" / count components | Either (DFS is shorter) |
| Explore/flood-fill a region                   | Either         |
| Shortest path with **weights/costs**          | **Dijkstra** (Part 4) |
| Dependency order / cycle in directed graph    | **Topological sort** (Part 4) |

**Default to BFS when the word "shortest" or "minimum steps" appears.** BFS finds the
shortest path in an unweighted graph *for free*, because it reaches nodes in
increasing order of distance. DFS does not.

---

## Part 3 — Pattern: "Number of connected components / islands" (flood fill)

This is the most common graph pattern and the one to master first. The structure:

> Loop over every node. If it's unvisited, that's a **new** component — increment a
> counter and flood-fill (DFS/BFS) to mark the *entire* component visited so you
> don't count it again.

```python
def count_components(graph, n):
    visited = set()
    count = 0
    for node in range(n):
        if node not in visited:
            count += 1                    # found a new component
            dfs(graph, node, visited)     # drown the whole thing
    return count
```

This exact shape solves:
- **Number of Provinces** (`number_of_provinces.py`) — components in an adjacency matrix.
- **Number of Islands** (`number_of_island.py`) — components in a grid; "node" is a
  cell, you flood-fill connected `'1'`s. The outer loop is a double `for r / for c`.

> **Mantra for component problems:** *"outer loop finds a new seed, inner traversal
> drowns its whole island."*

---

## Part 4 — The "named algorithm" patterns (know when, not just how)

These have specific triggers. When you spot the trigger, reach for the algorithm.

### Topological Sort / Cycle Detection in a DIRECTED graph — **Kahn's Algorithm (BFS)**

**Triggers:** "course schedule", "prerequisites", "build/compile order", "task
dependencies", "is there a cycle in a directed graph". See
`cycle_detect_directed_graph.py`.

Idea: repeatedly remove nodes that have **no remaining prerequisites** (indegree 0).
If you can remove all of them, there's a valid order and no cycle. If some are stuck,
there's a cycle.

```python
from collections import defaultdict, deque

def topo_sort(n, edges):                  # edges: [prereq, course]
    graph = defaultdict(list)
    indegree = [0] * n
    for u, v in edges:                    # u must come before v
        graph[u].append(v)
        indegree[v] += 1

    queue = deque(i for i in range(n) if indegree[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph[node]:
            indegree[neighbour] -= 1      # "remove" the edge
            if indegree[neighbour] == 0:  # neighbour now has no prereqs
                queue.append(neighbour)

    return order if len(order) == n else []   # empty => cycle exists
```
- **Course Schedule I** = "is `len(order) == n`?" (cycle check).
- **Course Schedule II** = "return `order`."
They are the *same code*. That's the payoff of recognising the pattern.

> **Undirected cycle detection** is different — there you DFS and check if you reach
> an already-visited node that *isn't* the parent you came from. See
> `cycle_detect_undirected_graph.py`.

### Shortest path with WEIGHTS — **Dijkstra's Algorithm**

**Triggers:** "minimum cost", "shortest time", "cheapest", and edges have **weights**.
(If edges are unweighted, plain BFS is enough — don't over-engineer.)

Idea: BFS, but use a **min-heap** (priority queue) instead of a plain queue so you
always expand the closest-so-far node next.

```python
import heapq

def dijkstra(graph, start, n):            # graph[u] = [(v, weight), ...]
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]                    # (distance_so_far, node)
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:                 # stale entry, skip
            continue
        for neighbour, weight in graph[node]:
            nd = d + weight
            if nd < dist[neighbour]:
                dist[neighbour] = nd
                heapq.heappush(heap, (nd, neighbour))
    return dist
```
This is the template for **Network Delay Time (LC 743)** and most weighted
shortest-path problems on the to-do list in `README.md`.

### Minimum Spanning Tree — **Prim's / Kruskal's**

**Trigger:** "connect all points/nodes at minimum total cost" (e.g. *Minimum Cost to
Connect All Points*). Prim's is basically Dijkstra but you track the cheapest edge to
*reach* a node rather than the total distance. Learn this *after* you're solid on
Dijkstra.

### Clone / copy a graph — DFS/BFS + a `old → new` hash map

**Trigger:** "deep copy this graph" (`clone_graph.py`). The trick is a dictionary
mapping each original node to its clone, so you (a) don't clone twice and (b) the map
doubles as your `visited` set.

---

## Part 5 — A repeatable procedure for any graph problem

When you're stuck, run this in order:

1. **Identify the graph.** What are the nodes? What are the edges (when is A connected
   to B)? Write it in one sentence: *"Nodes are cells; edges connect adjacent land
   cells."*
2. **Note the input format** (edge list / matrix / grid / object) and decide whether
   you need to **build an adjacency list** or can traverse the input directly.
3. **Directed or undirected?** If you build the adj list, this decides whether you add
   one direction or both. Get this right early.
4. **Classify into one of the four buckets** (Part 0): connectivity, shortest path,
   dependency order, or MST.
5. **Pick the tool:**
   - connectivity / components → DFS or BFS flood fill (Part 3)
   - shortest path, unweighted → **BFS**
   - shortest path, weighted → **Dijkstra**
   - dependency order / directed cycle → **Kahn's topological sort**
   - connect-all-cheaply → **MST**
6. **Write the `visited` set first.** Then the traversal. Then the bookkeeping
   (counter / distance array / order list / clone map).
7. **Test on a tiny example by hand**, including a node with a back-edge (a cycle) to
   make sure `visited` saves you.

---

## Part 6 — Complexity (what to say in interviews)

Let **V** = number of vertices (nodes), **E** = number of edges.

- **BFS / DFS:** **O(V + E)** time, **O(V)** space. You touch every node and every
  edge once. This is the answer for the vast majority of graph problems.
- **Grid (R×C):** O(R·C) — each cell is a node with up to 4 edges.
- **Topological sort (Kahn's):** O(V + E).
- **Dijkstra (binary heap):** O(E log V).

> **Common confusion:** for a grid, people say "O(n²)." Prefer **O(rows × cols)** —
> it's precise and shows you understand the cell-as-node model.

---

## Part 7 — Practice order in this folder

1. `graph_traversal.py` — BFS & DFS templates. Memorise these. (Part 2)
2. `number_of_provinces.py` — your first component-count (adjacency matrix). (Part 3)
3. `number_of_island.py` — component count on a **grid** (cells as nodes). (Part 3)
4. `cycle_detect_undirected_graph.py` — DFS cycle detection (parent trick).
5. `cycle_detect_directed_graph.py` — Kahn's algorithm / topological sort. (Part 4)
6. `clone_graph.py` — traversal + `old→new` map. (Part 4)

Then tackle the rest of the `README.md` checklist: Rotting Oranges (multi-source BFS),
Dijkstra, Network Delay Time, Max Area of Island, Min Cost to Connect All Points.

For each: run the Part 5 procedure yourself *before* reading the solution.

---

## The one paragraph to remember

> Step 1 is always **"turn the input into a graph"**: identify the nodes, identify
> when two are connected, and decide directed vs undirected. Then **classify**:
> connectivity → DFS/BFS flood fill; shortest unweighted → BFS; shortest weighted →
> Dijkstra; dependency order or directed cycle → Kahn's topological sort; cheapest
> connection → MST. **Always keep a `visited` set** — that's the one thing trees let
> you skip and graphs never do. Write `visited` first, traversal second, bookkeeping
> third. Draw a tiny example with a cycle to prove it works.
