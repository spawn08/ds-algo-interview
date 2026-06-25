# Trees — Prerequisites & How to Actually Solve Tree Problems

> If you freeze when you see a tree problem, it is almost never because the problem
> is hard. It is because you haven't yet internalised the **3 building blocks** and
> the **5 recurring patterns**. Once those click, ~90% of tree problems become
> "which pattern is this?" instead of "where do I even start?".
>
> Read this top to bottom once. Then keep it open while you solve the problems in
> this folder.

---

## Part 0 — The mental model that fixes everything

A tree problem is **always** one of these two questions in disguise:

1. **"Visit every node and collect/compute something."** → This is a *traversal*.
2. **"At each node, combine answers from my children to produce my own answer."**
   → This is *recursion on the tree* (also called "DFS that returns a value").

That's it. Every tree problem in this repo is a flavour of one of those two.

The reason tree problems *feel* hard is that the recursion hides the work. So we are
going to make the recursion **explicit and mechanical**.

---

## Part 1 — The 3 building blocks

### Block 1: What a tree node actually is

A binary tree is just a chain of objects pointing at up to two other objects.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left      # another TreeNode, or None
        self.right = right    # another TreeNode, or None
```

See `tree.py` for the real definition used across this folder.

Key facts you must hold in your head:
- A node with `left = None` and `right = None` is a **leaf**.
- `None` is a real, legal value — it means "no child here". **Half of all tree bugs
  are forgetting that a child can be `None`.**
- The whole tree is referenced by one variable, `root`. If `root is None`, the tree
  is empty — this is your most common base case.

### Block 2: Recursion = trust + base case

The single biggest unlock for trees is this sentence:

> **Assume the recursive call already works on a smaller subtree. Now just combine.**

This is "the recursive leap of faith." You do **not** trace the recursion in your
head 10 levels deep. You write the function as if it already works on the children,
and trust it.

Every recursive tree function has exactly two parts:

```python
def solve(node):
    # 1. BASE CASE — the smallest possible input. Almost always "empty tree".
    if node is None:
        return <the answer for an empty tree>

    # 2. RECURSIVE CASE — trust the calls on the children, then combine.
    left_answer  = solve(node.left)    # trust it
    right_answer = solve(node.right)   # trust it
    return <combine left_answer, right_answer, and node.val>
```

If you can fill in the two `<...>` blanks, you have solved the problem. **That is the
entire game.** When you're stuck, you are stuck on exactly one of:
- "What is the answer for an empty tree?" (base case)
- "How do I combine my children's answers with my own value?" (the combine step)

Ask yourself those two questions *explicitly, out loud*, every single time.

### Block 3: Depth-first vs Breadth-first

There are two orders in which you can visit nodes. You must know both cold.

**DFS (Depth-First Search)** — go as deep as possible before backtracking. Implemented
with **recursion** (the call stack *is* your stack) or an explicit **stack**.

**BFS (Breadth-First Search)** — visit level by level, top to bottom. Implemented with
a **queue** (`collections.deque`).

```
        1
       / \
      2   3
     / \
    4   5

DFS order (pre-order):  1 2 4 5 3   (dive deep first)
BFS order (level order): 1 2 3 4 5   (one level at a time)
```

Rule of thumb: **"levels", "distance from root", "shortest", "nearest"** → BFS.
Everything else → DFS.

---

## Part 2 — Traversals (the absolute foundation)

Memorise these four. Working code is in `tree_traversal_dfs.py` and
`bt_level_order_traversal.py`. The only thing that changes between the three DFS
traversals is **where you "process" the node** relative to the recursive calls.

```python
def pre_order(node):     # process BEFORE children:  Root, Left, Right
    if not node: return
    process(node)            # <-- here
    pre_order(node.left)
    pre_order(node.right)

def in_order(node):      # process BETWEEN children: Left, Root, Right
    if not node: return
    in_order(node.left)
    process(node)            # <-- here
    in_order(node.right)

def post_order(node):    # process AFTER children:   Left, Right, Root
    if not node: return
    post_order(node.left)
    post_order(node.right)
    process(node)            # <-- here
```

When do you use which?

| Traversal  | Use when…                                                                 |
|------------|---------------------------------------------------------------------------|
| **Pre-order**  | You need to process a node *before* its subtree (e.g. copy/clone, serialize). |
| **In-order**   | **Binary Search Trees** — in-order gives values in *sorted order*. Huge. |
| **Post-order** | You need children's results *before* the parent (e.g. height, deletion, "did my subtree satisfy X?"). **This is the most common pattern in interviews.** |
| **Level-order (BFS)** | Anything to do with levels, depth, or shortest distance. |

> **Memory hook:** "Pre/In/Post" = where **Root** sits. Pre = Root first,
> In = Root in the middle, Post = Root last.

### Level-order (BFS) template — memorise this exact shape

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)       # <-- KEY: freeze the count for THIS level
        current_level = []
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(current_level)
    return result
```

The `level_size = len(queue)` line is the trick that lets you process exactly one
level per outer loop. If a problem says "per level" / "level by level" / "right side
view" / "zigzag", you start from this template. See `bt_level_order_traversal.py`.

### Iterative DFS (when recursion is banned or stack depth is a worry)

Swap the queue for a stack. See `tree_iterative_traversal.py`. You rarely need this,
but interviewers sometimes ask "now do it without recursion."

---

## Part 3 — The 5 patterns that cover almost every tree problem

This is the part that fixes "I don't know where to start." For each problem, figure
out **which of these five it is.** Then copy the template and fill in the blanks.

### Pattern 1 — "Compute a value by combining children" (post-order / DFS-with-return)

The workhorse. You return information *up* the tree from children to parent.

**Tell-tale signs:** "maximum depth", "is it balanced", "diameter", "sum of...",
"height", "count nodes".

**Template:**
```python
def dfs(node):
    if not node:
        return <base value>          # e.g. 0 for height, True for "balanced"
    left  = dfs(node.left)
    right = dfs(node.right)
    return <combine left, right, node.val>
```

**Example — Max Depth (`bt_max_depth.py`):**
```python
def max_depth(node):
    if not node:
        return 0                          # empty tree has depth 0
    return 1 + max(max_depth(node.left), max_depth(node.right))
```
Read it as: "my depth = 1 (for myself) + the deeper of my two children." That's the
combine step. The base case is "empty = 0." Done.

**The "global variable" twist:** Sometimes the value you *return* to your parent is
different from the value you're *tracking overall*. Classic examples: diameter, and
**Binary Tree Maximum Path Sum** (`binary_tree_max_path_sum.py`). The trick:

```python
def max_path_sum(root):
    best = float('-inf')                  # the global answer

    def dfs(node):                        # returns: best path going DOWN from node
        nonlocal best
        if not node:
            return 0
        left  = max(dfs(node.left), 0)    # ignore negative contributions
        right = max(dfs(node.right), 0)
        best = max(best, node.val + left + right)   # path that BENDS at node
        return node.val + max(left, right)          # path you can EXTEND upward
    dfs(root)
    return best
```
The lesson: **what you return ≠ what you record.** A node returns a straight path it
can hand to its parent, but it *records* the bent path that peaks at itself. When a
problem feels impossible, ask: "are these two quantities actually different?"

### Pattern 2 — "Check a property of every node" (validation)

**Signs:** "is this a valid BST", "is it symmetric", "are two trees identical",
"is it balanced".

You recurse and return a boolean (or a value you check). See
`check_balanced_binary_tree.py`. For **valid BST**, the key insight is you must pass
down the allowed `(min, max)` range:

```python
def is_valid_bst(node, low=float('-inf'), high=float('inf')):
    if not node:
        return True
    if not (low < node.val < high):
        return False
    return (is_valid_bst(node.left,  low, node.val) and
            is_valid_bst(node.right, node.val, high))
```
Why a range and not just "left < node < right"? Because a node deep on the left must
be smaller than **every** ancestor it descended from the right of — not just its
parent. Passing `(low, high)` down captures all those constraints at once. This
"pass constraints down through arguments" idea is its own mini-pattern.

### Pattern 3 — "Path / root-to-node problems" (DFS carrying state down)

**Signs:** "root-to-leaf path", "path sum equals target", "all paths".

Here you carry accumulated state *down* as a parameter (the opposite direction from
Pattern 1, which carries answers *up*).

```python
def has_path_sum(node, target):
    if not node:
        return False
    if not node.left and not node.right:      # leaf
        return node.val == target
    remaining = target - node.val
    return has_path_sum(node.left, remaining) or has_path_sum(node.right, remaining)
```
Note the distinct **leaf** base case — "no children" is different from "node is None".
Many path problems hinge on detecting the leaf correctly.

### Pattern 4 — "Lowest Common Ancestor" (the bottom-up search)

`lowest_common_ancestor.py`. Worth knowing as its own pattern because the trick is
slick and reused:

```python
def lca(node, p, q):
    if not node or node is p or node is q:
        return node
    left  = lca(node.left,  p, q)
    right = lca(node.right, p, q)
    if left and right:        # p and q found in different subtrees -> THIS is the LCA
        return node
    return left or right      # both on one side (or neither) -> bubble it up
```
The "if left and right → I'm the meeting point" logic shows up in many tree problems.

### Pattern 5 — "Level-by-level" (BFS)

**Signs:** "level order", "zigzag", "right side view", "average per level",
"minimum depth", "connect nodes at same level". Use the BFS template from Part 2.
Right side view = take the *last* node of each level. Average = mean of each level.
They're all the same template with one line changed.

---

## Part 4 — A repeatable procedure for any tree problem

When you open a tree problem and your mind goes blank, run this checklist:

1. **Draw a small tree** (3–5 nodes). Always. Do not skip this. You cannot solve what
   you cannot see.
2. **Pick DFS or BFS:** does the problem mention *levels / depth / shortest*? → BFS.
   Otherwise → DFS.
3. **If DFS, decide the direction of information flow:**
   - Answers flow **up** (children → parent)? → Pattern 1/2, post-order, return values.
   - State flows **down** (root → node)? → Pattern 3, pass parameters.
4. **Write the base case first.** Ask literally: *"What's the answer for an empty
   tree (`node is None`)?"* Write that line before anything else.
5. **Write the combine step** assuming the recursive calls already work (the leap of
   faith). Ask: *"Given `left_answer` and `right_answer`, how do I make my answer?"*
6. **Ask: is what I return the same as what I track?** If not, use a `nonlocal`
   global (Pattern 1 twist).
7. **Trace your small tree by hand** to confirm. Pay special attention to leaves and
   `None` children.

If you do steps 4 and 5 *explicitly, in writing*, every time, you will stop freezing.

---

## Part 5 — Complexity (what to say in interviews)

- **Time:** almost always **O(n)** — you visit each node a constant number of times.
- **Space:** **O(h)** for DFS where `h` is the tree height (the recursion/call stack).
  - Balanced tree: `h ≈ log n` → O(log n).
  - Worst case (a "linked list" tree): `h = n` → O(n).
- **BFS space:** O(w) where `w` is the max width — up to O(n) for the bottom level.

---

## Part 6 — Practice order in this folder

Do them in this sequence. Earlier ones build the muscles for later ones.

1. `tree_traversal_dfs.py` — pre/in/post order. The foundation. (Part 2)
2. `bt_level_order_traversal.py` — BFS template. (Pattern 5)
3. `bt_max_depth.py` — your first "combine children" problem. (Pattern 1)
4. `bt_inorder_traversal.py` — in-order, the BST connection.
5. `check_balanced_binary_tree.py` — validation + height in one pass. (Pattern 2)
6. `tree_iterative_traversal.py` — DFS without recursion.
7. `lowest_common_ancestor.py` — the bubble-up trick. (Pattern 4)
8. `binary_tree_max_path_sum.py` — the "return ≠ record" twist. (Pattern 1, hard)

For each: cover the solution, run the procedure in Part 4 yourself, *then* compare.

---

## The one paragraph to remember

> Every tree problem is "traverse" or "combine children's answers." Pick DFS (default)
> or BFS (levels/shortest). For DFS, decide whether info flows **up** (return values,
> post-order) or **down** (parameters). Always write the **base case** (`if node is
> None`) first, then write the **combine step** *trusting that the recursive calls
> already work*. Draw a small tree. That's the whole skill.
