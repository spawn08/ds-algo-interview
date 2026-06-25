# Tree Data Structures — From Scratch to Google L5/L6 Interview Ready

All code follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html): snake_case functions/variables, CamelCase classes, type hints, docstrings, descriptive names.

---

## 1. What Is a Tree?

A tree is a connected graph with no cycles. That's the formal definition, and it's the most useful one. Everything you learned about graphs applies to trees, but trees have additional properties that enable algorithms graphs can't support.

Specifically: a tree on `N` nodes has exactly `N-1` edges. There's exactly one path between any two nodes (no cycles means no alternative routes). One node is designated the **root**, which induces a parent-child hierarchy on the rest. Every non-root node has exactly one parent. This hierarchy is what makes trees so useful — it gives us a natural notion of "above" and "below," which graphs lack.

**Why trees dominate Google interviews:** Trees model hierarchy, and almost all data has hierarchy. File systems are trees. DOM is a tree. Decision trees, parse trees, expression trees, B-trees in databases, tries for autocomplete, segment trees for range queries — every system Google operates uses trees somewhere. At L5/L6, you're expected to recognize when a problem has tree structure (even when not obvious) and choose the right traversal.

---

## 2. Tree Vocabulary

**Root:** The single node at the top of the hierarchy. Has no parent.

**Leaf:** A node with no children. In an N-node tree, leaves are the "boundary."

**Internal node:** Any non-leaf node.

**Parent / Child:** If A has a directed edge to B in the rooted hierarchy, A is B's parent and B is A's child. Each non-root has exactly one parent.

**Sibling:** Two nodes sharing the same parent.

**Ancestor / Descendant:** A is an ancestor of B if A appears on the path from root to B. B is then a descendant of A. Every node is its own ancestor and descendant.

**Depth of a node:** Number of edges from root to that node. Root has depth 0.

**Height of a node:** Number of edges on the longest downward path from that node to a leaf. Leaves have height 0. The height of the tree is the height of its root.

**Subtree rooted at node X:** X and all its descendants.

**Binary tree:** Every node has at most 2 children, called `left` and `right`.

**Balanced tree:** Heights of left and right subtrees differ by at most some constant (usually 1). Critical because operations on balanced trees are O(log N), while on degenerate trees they're O(N).

**Complete tree:** All levels filled except possibly the last, which is filled left to right.

**BST (Binary Search Tree):** A binary tree where for every node, all values in the left subtree are less than the node's value, and all values in the right subtree are greater. This invariant enables O(log N) search on balanced BSTs.

---

## 3. Tree Representations

### 3.1 Linked Node (The Standard Interview Representation)

```python
from typing import Optional


class TreeNode:
    """Standard binary tree node.

    This is the LeetCode-standard definition. Memorize the constructor
    signature — it appears in nearly every tree problem.

    Attributes:
        val: The value stored at this node.
        left: Reference to the left child, or None.
        right: Reference to the right child, or None.
    """

    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right
```

For N-ary trees (each node can have arbitrarily many children):

```python
class NaryTreeNode:
    """N-ary tree node where each node has a list of children.

    Used for problems like "Serialize and Deserialize N-ary Tree" or
    when modeling file systems, DOM trees, or organizational hierarchies.

    Attributes:
        val: The value stored at this node.
        children: List of child node references.
    """

    def __init__(
        self,
        val: int = 0,
        children: Optional[list["NaryTreeNode"]] = None,
    ) -> None:
        self.val = val
        self.children = children if children is not None else []
```

### 3.2 Array Representation (Heaps)

For complete binary trees, we can store them in an array without any pointers. Node at index `i` has:
- Left child at index `2*i + 1`
- Right child at index `2*i + 2`
- Parent at index `(i - 1) // 2`

This is how Python's `heapq` works. It's space-efficient and cache-friendly, but only works for complete trees.

### 3.3 Parent Pointers

Some problems require traversing upward. We can either store explicit parent pointers in nodes, or build a `child_to_parent` map during a preorder pass. The latter avoids modifying the node structure.

```python
def build_parent_map(
    root: Optional[TreeNode],
) -> dict[TreeNode, Optional[TreeNode]]:
    """Builds a child-to-parent mapping for a binary tree.

    Useful when a problem requires traversing upward from a node
    (e.g., "Find all nodes at distance K from target"). Building this
    map once during a preorder pass is cleaner than mutating TreeNode.

    Args:
        root: Root of the binary tree.

    Returns:
        Dictionary mapping each node to its parent. Root maps to None.
    """
    parent_of: dict[TreeNode, Optional[TreeNode]] = {root: None}

    def dfs_assign_parents(current_node: Optional[TreeNode]) -> None:
        if current_node is None:
            return
        if current_node.left:
            parent_of[current_node.left] = current_node
            dfs_assign_parents(current_node.left)
        if current_node.right:
            parent_of[current_node.right] = current_node
            dfs_assign_parents(current_node.right)

    dfs_assign_parents(root)
    return parent_of
```

---

## 4. The Four Traversals — The Foundation of Every Tree Problem

Every tree algorithm is built on one of four traversal orders. Internalize these. When you see a tree problem, your first question should be: which traversal does this need?

### 4.1 Preorder (Root → Left → Right)

Visit the current node BEFORE recursing into its children. Useful when you need to process a node before knowing anything about its subtrees — for example, when serializing a tree or copying it.

```python
def preorder_traversal(root: Optional[TreeNode]) -> list[int]:
    """Returns node values in preorder: root, then left subtree, then right.

    Use preorder when the parent must be processed before the children.
    Examples: tree serialization, deep-copying a tree, evaluating prefix
    expressions, printing a directory structure.

    Args:
        root: Root of the binary tree.

    Returns:
        List of values in preorder.
    """
    result = []

    def dfs(current_node: Optional[TreeNode]) -> None:
        if current_node is None:
            return
        result.append(current_node.val)  # Process BEFORE recursing
        dfs(current_node.left)
        dfs(current_node.right)

    dfs(root)
    return result
```

### 4.2 Inorder (Left → Root → Right)

Recurse into the left subtree first, then process the current node, then recurse into the right subtree. **For a BST, inorder traversal yields values in sorted order.** This single fact powers many BST algorithms.

```python
def inorder_traversal(root: Optional[TreeNode]) -> list[int]:
    """Returns node values in inorder: left subtree, root, right subtree.

    Critical property: on a BST, inorder traversal produces values in
    ascending sorted order. This is THE fundamental BST property
    interviewers test. If you see "BST + sorted" or "BST + k-th smallest",
    inorder is the answer.

    Args:
        root: Root of the binary tree.

    Returns:
        List of values in inorder.
    """
    result = []

    def dfs(current_node: Optional[TreeNode]) -> None:
        if current_node is None:
            return
        dfs(current_node.left)
        result.append(current_node.val)  # Process BETWEEN subtrees
        dfs(current_node.right)

    dfs(root)
    return result
```

### 4.3 Postorder (Left → Right → Root)

Process children BEFORE the current node. Use postorder when you need information from subtrees to make a decision about the current node. This is the workhorse traversal for tree DP problems — "compute X for each subtree, then combine."

```python
def postorder_traversal(root: Optional[TreeNode]) -> list[int]:
    """Returns node values in postorder: left subtree, right subtree, root.

    Postorder is the right choice when the answer for a node depends on
    answers from its children. Examples: deleting a tree (delete children
    before parent, else you lose references), computing subtree heights,
    computing subtree sums, most tree DP problems.

    Args:
        root: Root of the binary tree.

    Returns:
        List of values in postorder.
    """
    result = []

    def dfs(current_node: Optional[TreeNode]) -> None:
        if current_node is None:
            return
        dfs(current_node.left)
        dfs(current_node.right)
        result.append(current_node.val)  # Process AFTER both subtrees

    dfs(root)
    return result
```

### 4.4 Level Order (BFS)

Visit all nodes at depth 0, then all at depth 1, then depth 2, etc. Uses a queue. This is BFS applied to trees. Use it whenever you need "level by level" processing — problems involving depths, level averages, right-side views, zigzag traversals.

```python
from collections import deque


def level_order_traversal(root: Optional[TreeNode]) -> list[list[int]]:
    """Returns node values grouped by level (depth).

    The key technique: at the start of each iteration, capture the
    current queue size. That's exactly how many nodes are at the
    current level. Process exactly that many, then move on. Any
    nodes enqueued during this pass belong to the next level.

    Args:
        root: Root of the binary tree.

    Returns:
        List of lists, where result[i] contains all values at depth i.
    """
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)  # Snapshot: nodes at the current level
        current_level_values = []

        for _ in range(level_size):
            current_node = queue.popleft()
            current_level_values.append(current_node.val)
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

        result.append(current_level_values)

    return result
```

### Choosing the Right Traversal

Decision framework:

- **"Process node, then recurse":** Preorder. Examples — serialization, tree cloning.
- **"BST + sorted output / k-th element / validation":** Inorder.
- **"Need subtree info to decide about node":** Postorder. Examples — height, diameter, balanced check, most tree DP.
- **"Level-by-level / depth-aware":** Level order (BFS). Examples — right view, zigzag, minimum depth.

---

## 5. Iterative Traversals (When Recursion Isn't Allowed)

Sometimes interviewers ask for iterative solutions — either to test deeper understanding or because the tree might be too deep for Python's default 1000-recursion limit. Iterative traversals use an explicit stack to simulate the recursion.

### Iterative Inorder

```python
def inorder_iterative(root: Optional[TreeNode]) -> list[int]:
    """Iterative inorder traversal using an explicit stack.

    The pattern: dive left as far as possible, pushing nodes onto the
    stack as we go. When we can't go further left, pop the top of the
    stack (the leftmost unprocessed node), record it, then explore its
    right subtree using the same pattern.

    Why this works: inorder = left, root, right. The stack holds nodes
    whose left subtrees have been fully explored but who haven't been
    visited yet. Popping gives the next node in inorder.

    Args:
        root: Root of the binary tree.

    Returns:
        List of values in inorder.
    """
    result = []
    stack: list[TreeNode] = []
    current_node = root

    while current_node is not None or stack:
        # Phase 1: go as far left as possible
        while current_node is not None:
            stack.append(current_node)
            current_node = current_node.left

        # Phase 2: process the leftmost unvisited node
        current_node = stack.pop()
        result.append(current_node.val)

        # Phase 3: now explore its right subtree the same way
        current_node = current_node.right

    return result
```

### Iterative Preorder

```python
def preorder_iterative(root: Optional[TreeNode]) -> list[int]:
    """Iterative preorder traversal using an explicit stack.

    Simpler than iterative inorder because preorder processes the node
    immediately. We push the right child BEFORE the left child so that
    the left child is popped (and processed) first. This matches the
    "root, left, right" order.

    Args:
        root: Root of the binary tree.

    Returns:
        List of values in preorder.
    """
    if root is None:
        return []

    result = []
    stack = [root]

    while stack:
        current_node = stack.pop()
        result.append(current_node.val)

        # Push right first so left is processed next (stacks are LIFO)
        if current_node.right:
            stack.append(current_node.right)
        if current_node.left:
            stack.append(current_node.left)

    return result
```

### Iterative Postorder

Postorder is the trickiest iterative traversal. The cleanest approach: do a modified preorder that visits root → right → left, then reverse the result. Reversing gives left → right → root, which is postorder.

```python
def postorder_iterative(root: Optional[TreeNode]) -> list[int]:
    """Iterative postorder via reversed modified-preorder.

    Trick: postorder = (left, right, root). If we do (root, right, left)
    iteratively and REVERSE the result, we get (left, right, root). The
    forward traversal is just preorder with right-before-left ordering,
    which is easy with a stack.

    Args:
        root: Root of the binary tree.

    Returns:
        List of values in postorder.
    """
    if root is None:
        return []

    result = []
    stack = [root]

    while stack:
        current_node = stack.pop()
        result.append(current_node.val)

        # Push left first so right is processed first (we'll reverse at end)
        if current_node.left:
            stack.append(current_node.left)
        if current_node.right:
            stack.append(current_node.right)

    return result[::-1]
```

---

## 6. Tree Properties — Height, Depth, Diameter

These problems use postorder almost exclusively. The pattern: compute something for each subtree, combine to compute for the current node.

### Maximum Depth (Height)

```python
def maximum_depth(root: Optional[TreeNode]) -> int:
    """Computes the maximum depth (height + 1) of a binary tree.

    Depth of a tree = depth of the deeper subtree + 1 (for the root).
    A None subtree has depth 0. This is the canonical postorder pattern:
    we need both subtree depths BEFORE we can compute the current node's
    depth, so we recurse first and combine after.

    Args:
        root: Root of the binary tree.

    Returns:
        Maximum depth from root to any leaf. 0 for an empty tree.
    """
    if root is None:
        return 0

    left_depth = maximum_depth(root.left)
    right_depth = maximum_depth(root.right)
    return max(left_depth, right_depth) + 1
```

### Diameter (Longest Path Between Any Two Nodes)

The diameter of a tree is the longest path between any pair of nodes. This path may or may not pass through the root. Key insight: for any path, there's exactly one "highest" node on that path (closest to the root). That node is where the path's left half meets its right half.

So: for every node, compute `left_subtree_height + right_subtree_height`. The maximum of these values across all nodes is the diameter.

```python
def diameter_of_tree(root: Optional[TreeNode]) -> int:
    """Computes the diameter: longest path (in edges) between any two nodes.

    For every node, the longest path THROUGH that node equals
    left_height + right_height. The diameter is the max of this quantity
    across all nodes.

    We compute heights bottom-up (postorder). At each node, we both
    return the height (for our caller) and update the global maximum
    using the through-this-node candidate. This single-pass approach
    is O(N) instead of the O(N²) you'd get by computing heights
    separately at each node.

    Args:
        root: Root of the binary tree.

    Returns:
        Number of edges on the longest path between any two nodes.
    """
    max_diameter = 0

    def compute_height(current_node: Optional[TreeNode]) -> int:
        nonlocal max_diameter
        if current_node is None:
            return 0

        left_height = compute_height(current_node.left)
        right_height = compute_height(current_node.right)

        # Longest path passing through this node, in edges
        path_through_current = left_height + right_height
        max_diameter = max(max_diameter, path_through_current)

        # Height of this subtree (for the caller)
        return max(left_height, right_height) + 1

    compute_height(root)
    return max_diameter
```

### Balanced Binary Tree Check

A tree is balanced if, for every node, the heights of its left and right subtrees differ by at most 1. Naive approach: at every node, compute both subtree heights and compare. That's O(N²). Better: compute height and balanced-ness in a single postorder pass. Return -1 as a sentinel meaning "unbalanced."

```python
def is_balanced(root: Optional[TreeNode]) -> bool:
    """Determines whether a binary tree is height-balanced.

    Height-balanced means: for every node, |left_height - right_height| <= 1.

    The naive O(N²) approach computes height repeatedly at every node.
    Instead, we fuse the height computation with the balance check using
    -1 as a sentinel meaning "this subtree is unbalanced; stop computing
    heights." As soon as any subtree is unbalanced, the answer is False,
    and we propagate the -1 sentinel up to short-circuit.

    Args:
        root: Root of the binary tree.

    Returns:
        True if every node's subtrees differ in height by at most 1.
    """

    def check_height(current_node: Optional[TreeNode]) -> int:
        """Returns height if balanced, -1 if any subtree is unbalanced."""
        if current_node is None:
            return 0

        left_height = check_height(current_node.left)
        if left_height == -1:
            return -1  # Short-circuit: left subtree is unbalanced

        right_height = check_height(current_node.right)
        if right_height == -1:
            return -1  # Short-circuit: right subtree is unbalanced

        if abs(left_height - right_height) > 1:
            return -1  # This node violates balance

        return max(left_height, right_height) + 1

    return check_height(root) != -1
```

---

## 7. Binary Search Trees (BST)

A BST is a binary tree with a structural invariant: for every node, all values in the left subtree are less than the node's value, and all values in the right subtree are greater. This invariant gives BSTs their two superpowers:

1. **Inorder traversal yields sorted values.** This makes BSTs naturally suited for problems involving order statistics.
2. **Search/insert/delete in O(log N) on balanced BSTs.** Each comparison eliminates half the remaining tree.

The catch: on unbalanced BSTs, these operations degrade to O(N). Self-balancing variants (AVL, Red-Black, B-Trees) maintain balance automatically, but you almost never implement these in interviews — you just need to know they exist.

### BST Search

```python
def search_bst(
    root: Optional[TreeNode], target_value: int
) -> Optional[TreeNode]:
    """Searches for target_value in a BST.

    At each node, we use the BST invariant to eliminate half the tree:
    if target < node.val, the target (if it exists) must be in the
    left subtree; if target > node.val, it must be in the right.
    This gives O(log N) on balanced BSTs, O(N) worst case on degenerate
    (chain-like) ones.

    Args:
        root: Root of the BST.
        target_value: Value to search for.

    Returns:
        The node containing target_value, or None if not found.
    """
    current_node = root
    while current_node is not None:
        if target_value == current_node.val:
            return current_node
        if target_value < current_node.val:
            current_node = current_node.left
        else:
            current_node = current_node.right
    return None
```

### BST Insertion

```python
def insert_into_bst(
    root: Optional[TreeNode], new_value: int
) -> TreeNode:
    """Inserts a new value into a BST and returns the (possibly new) root.

    Walks down the tree using BST comparisons until reaching a None
    slot, then inserts. This preserves the BST invariant: the new
    node ends up in a position consistent with all ancestors' values.

    Note: in interviews, the recursive version is more common because
    it's shorter and makes the "return the new root" pattern explicit.

    Args:
        root: Root of the BST (may be None for empty tree).
        new_value: Value to insert.

    Returns:
        Root of the BST after insertion.
    """
    if root is None:
        return TreeNode(new_value)

    if new_value < root.val:
        root.left = insert_into_bst(root.left, new_value)
    else:
        root.right = insert_into_bst(root.right, new_value)

    return root
```

### Validating a BST — The Range Pattern

A common wrong approach: at every node, check that `node.left.val < node.val < node.right.val`. This is INSUFFICIENT. A node's value must be greater than EVERY value in its left subtree (not just the immediate left child) and less than EVERY value in its right subtree. The classic counterexample: a node has value 10, its left child has value 5, but 5's right child has value 15 — this violates the BST property at the root level even though every parent-child comparison passes.

The correct approach: at each node, track the valid value range `(min_allowed, max_allowed)`. The range tightens as we recurse: going left tightens the maximum (everything must be less than the current node); going right tightens the minimum.

```python
def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """Validates that a binary tree satisfies the BST invariant.

    The range pattern: each recursive call carries the valid range
    (min_allowed, max_allowed) for the current node. At the root,
    the range is (-inf, +inf). When we recurse left, max_allowed
    becomes the current node's value (everything left must be less).
    When we recurse right, min_allowed becomes the current node's value.

    This correctly handles the deep-descendant constraint that a naive
    "check immediate children" approach misses.

    Args:
        root: Root of the binary tree.

    Returns:
        True if the tree is a valid BST.
    """

    def validate(
        current_node: Optional[TreeNode],
        min_allowed: float,
        max_allowed: float,
    ) -> bool:
        if current_node is None:
            return True
        if (
            current_node.val <= min_allowed
            or current_node.val >= max_allowed
        ):
            return False
        return validate(
            current_node.left, min_allowed, current_node.val
        ) and validate(
            current_node.right, current_node.val, max_allowed
        )

    return validate(root, float("-inf"), float("inf"))
```

### K-th Smallest in BST

Since BST inorder is sorted, the k-th smallest element is the k-th element visited during inorder traversal. We can early-terminate as soon as we've visited k elements.

```python
def kth_smallest_in_bst(root: Optional[TreeNode], k: int) -> int:
    """Returns the k-th smallest value in a BST (1-indexed).

    Uses iterative inorder traversal, stopping after k visits. The
    iterative version is preferred here because it makes early
    termination clean — once we've found our answer, we just return,
    no need to unwind recursion or track flags.

    Args:
        root: Root of the BST.
        k: Rank to find (1 = smallest).

    Returns:
        The k-th smallest value.
    """
    stack: list[TreeNode] = []
    current_node = root
    remaining = k

    while current_node is not None or stack:
        # Dive left
        while current_node is not None:
            stack.append(current_node)
            current_node = current_node.left

        # Visit the leftmost unvisited
        current_node = stack.pop()
        remaining -= 1
        if remaining == 0:
            return current_node.val

        current_node = current_node.right

    raise ValueError("k exceeds tree size")
```

---

## 8. Lowest Common Ancestor (LCA)

The LCA of two nodes is the deepest node that has both of them as descendants (a node is its own descendant). This appears constantly in interviews.

### LCA in a General Binary Tree

```python
def lowest_common_ancestor(
    root: Optional[TreeNode],
    node_p: TreeNode,
    node_q: TreeNode,
) -> Optional[TreeNode]:
    """Finds the lowest common ancestor of two nodes in a binary tree.

    Three cases at each recursive call:
    1. Current node is None, p, or q: return it directly.
    2. Both p and q are found in different subtrees: current node is LCA.
    3. Both found in same subtree: return whichever subtree result is
       non-None (the LCA is somewhere in that subtree).

    The elegance of this solution: we don't need separate "found p" /
    "found q" flags. The recursive return values encode everything we
    need. If we return a non-None value from both subtrees, we've found
    p in one and q in the other — this node is their LCA.

    Args:
        root: Root of the binary tree.
        node_p: First target node.
        node_q: Second target node.

    Returns:
        The lowest common ancestor node.
    """
    if root is None or root is node_p or root is node_q:
        return root

    left_result = lowest_common_ancestor(root.left, node_p, node_q)
    right_result = lowest_common_ancestor(root.right, node_p, node_q)

    if left_result and right_result:
        return root  # p and q are split between subtrees → this is LCA

    # Otherwise return whichever side found something (or None)
    return left_result if left_result else right_result
```

### LCA in a BST

When the tree is a BST, we can exploit the ordering. The LCA is the first node we encounter where p and q split — i.e., where p is on one side and q is on the other (or where the current node IS p or q). Walking from root: if both p and q are smaller, go left. If both larger, go right. Otherwise we've found the split point.

```python
def lca_in_bst(
    root: TreeNode, node_p: TreeNode, node_q: TreeNode
) -> TreeNode:
    """Finds LCA in a BST using value comparisons.

    Faster than the general algorithm: O(height) instead of O(N) because
    we use the BST ordering to descend in one direction only.

    The split point: as long as both p.val and q.val are on the same
    side of the current node, we descend in that direction. The first
    node where they're on opposite sides (or where one equals the
    current node's value) is the LCA.

    Args:
        root: Root of the BST.
        node_p: First target node.
        node_q: Second target node.

    Returns:
        The LCA node.
    """
    current_node = root
    while current_node is not None:
        if node_p.val < current_node.val and node_q.val < current_node.val:
            current_node = current_node.left
        elif node_p.val > current_node.val and node_q.val > current_node.val:
            current_node = current_node.right
        else:
            return current_node  # Split point or current is p or q
    return root  # Unreachable for valid input
```

---

## 9. Path Problems

These problems ask about root-to-leaf paths, or paths between arbitrary nodes. Most use DFS with backtracking.

### Maximum Path Sum (Path Can Start and End Anywhere)

The path can start and end at any nodes, and must follow tree edges. This is similar to diameter, but with weighted values. Same insight: for each node, the best path THROUGH that node uses the best downward path from left and the best downward path from right.

Critical detail: when a subtree's best downward path sum is negative, we should exclude it (treat it as 0). Including a negative-sum subtree would only hurt.

```python
def maximum_path_sum(root: Optional[TreeNode]) -> int:
    """Computes the maximum path sum in a binary tree.

    A path can start and end at any nodes (not necessarily root-to-leaf)
    and must follow tree edges. Node values may be negative.

    For each node, two quantities matter:
    1. Best path sum FROM this node downward (single direction). This
       is what we return to the caller — they can extend our path upward.
    2. Best path sum THROUGH this node (combining left-down and right-down
       through this node). This is a candidate for the global answer but
       CAN'T be extended upward, since it already uses both children.

    We treat negative downward sums as 0 — excluding that subtree is
    always better than including it.

    Args:
        root: Root of the binary tree.

    Returns:
        Maximum sum achievable on any path in the tree.
    """
    max_sum_found = float("-inf")

    def best_downward_sum(current_node: Optional[TreeNode]) -> int:
        nonlocal max_sum_found
        if current_node is None:
            return 0

        # Get best downward sums from children, clamping negatives to 0
        left_gain = max(best_downward_sum(current_node.left), 0)
        right_gain = max(best_downward_sum(current_node.right), 0)

        # Candidate: full path through this node (can't extend upward)
        path_through_current = current_node.val + left_gain + right_gain
        max_sum_found = max(max_sum_found, path_through_current)

        # Return best path that CAN extend upward — only one child direction
        return current_node.val + max(left_gain, right_gain)

    best_downward_sum(root)
    return max_sum_found
```

### Root-to-Leaf Path Sum

Does any root-to-leaf path sum equal a target value? Classic DFS with running sum.

```python
def has_path_sum(
    root: Optional[TreeNode], target_sum: int
) -> bool:
    """Checks if any root-to-leaf path sums to target_sum.

    We subtract the current node's value from the remaining target as
    we descend. When we hit a leaf, we check if the remaining target
    equals the leaf's value. If yes, this path works.

    A "leaf" is a node with no left AND no right child. A node with
    one child is NOT a leaf — the path must continue down that child.

    Args:
        root: Root of the binary tree.
        target_sum: The target sum to find.

    Returns:
        True if such a path exists.
    """
    if root is None:
        return False

    # Leaf check: must have no children at all
    if root.left is None and root.right is None:
        return root.val == target_sum

    remaining = target_sum - root.val
    return has_path_sum(root.left, remaining) or has_path_sum(
        root.right, remaining
    )
```

### All Root-to-Leaf Paths Equal to Target

When asked to return all qualifying paths (not just check existence), use backtracking. Maintain a `current_path` list, append/pop as we descend/ascend.

```python
def find_all_root_to_leaf_paths_with_sum(
    root: Optional[TreeNode], target_sum: int
) -> list[list[int]]:
    """Returns all root-to-leaf paths whose values sum to target_sum.

    Backtracking pattern: maintain a current_path list. Append the
    current node's value before recursing, pop it after returning.
    This ensures current_path always reflects the path from root to
    the currently-being-explored node.

    Why we pop after returning (not before): if we didn't pop, sibling
    subtree explorations would see leftover values from previously
    explored paths.

    Args:
        root: Root of the binary tree.
        target_sum: The target path sum.

    Returns:
        List of paths (each path is a list of node values from root to leaf).
    """
    all_matching_paths: list[list[int]] = []
    current_path: list[int] = []

    def dfs(
        current_node: Optional[TreeNode], remaining: int
    ) -> None:
        if current_node is None:
            return

        current_path.append(current_node.val)
        new_remaining = remaining - current_node.val

        is_leaf = (
            current_node.left is None and current_node.right is None
        )
        if is_leaf and new_remaining == 0:
            # Append a COPY — current_path will be mutated during backtrack
            all_matching_paths.append(current_path[:])
        else:
            dfs(current_node.left, new_remaining)
            dfs(current_node.right, new_remaining)

        current_path.pop()  # Backtrack: undo the append

    dfs(root, target_sum)
    return all_matching_paths
```

---

## 10. Tree Construction Problems

These problems ask you to build a tree from some representation. The most famous: building a tree from preorder and inorder traversals.

### Build Tree from Preorder and Inorder

The first element of preorder is always the root of the current subtree. Once we know the root, we can find it in the inorder array — everything to its left in inorder is the left subtree, everything to its right is the right subtree. Recurse.

For O(N): build a hashmap from value to inorder index once at the start. This makes "find root in inorder" an O(1) lookup instead of O(N) scan, reducing total complexity from O(N²) to O(N).

```python
def build_tree_from_preorder_inorder(
    preorder: list[int], inorder: list[int]
) -> Optional[TreeNode]:
    """Constructs a binary tree from preorder and inorder traversals.

    Algorithm:
    1. First element of preorder is always the root of the current subtree.
    2. Find that root in inorder. Everything to its left in inorder is
       the left subtree (in inorder form). Everything to its right is
       the right subtree (in inorder form).
    3. The next len(left_subtree) elements of preorder form the left
       subtree's preorder. The rest form the right subtree's preorder.
    4. Recurse.

    We use a hashmap value→inorder_index to avoid O(N) scans, achieving
    O(N) total. We also pass index bounds instead of slicing arrays to
    avoid O(N) slice copies.

    Assumes all values are unique (otherwise the hashmap approach breaks
    and the tree isn't uniquely determined).

    Args:
        preorder: Preorder traversal of the target tree.
        inorder: Inorder traversal of the target tree.

    Returns:
        Root of the reconstructed tree.
    """
    inorder_index_of: dict[int, int] = {
        value: index for index, value in enumerate(inorder)
    }
    preorder_position = 0

    def build(
        inorder_left: int, inorder_right: int
    ) -> Optional[TreeNode]:
        nonlocal preorder_position
        if inorder_left > inorder_right:
            return None

        # Next root comes from preorder
        root_value = preorder[preorder_position]
        preorder_position += 1
        current_node = TreeNode(root_value)

        # Split inorder around the root
        root_inorder_index = inorder_index_of[root_value]

        # Build left subtree first (preorder visits left before right)
        current_node.left = build(inorder_left, root_inorder_index - 1)
        current_node.right = build(root_inorder_index + 1, inorder_right)

        return current_node

    return build(0, len(inorder) - 1)
```

---

## 11. Serialization

Serialize a tree to a string, then deserialize it back. The trick: handle None children explicitly so the structure is unambiguous.

```python
class TreeCodec:
    """Serializes and deserializes a binary tree using preorder traversal.

    Preorder with explicit None markers uniquely determines a binary
    tree (unlike inorder, which doesn't). The serialized format looks
    like "1,2,#,#,3,4,#,#,5,#,#" where # represents None.

    Why preorder works for this: the first element is always the root.
    Once we consume it, the remaining string is the left subtree's
    serialization followed by the right subtree's serialization. We
    recursively deserialize the left subtree (which consumes some
    prefix), then whatever's left is the right subtree.

    Without None markers, we couldn't tell where the left subtree ends
    and the right begins.
    """

    NULL_MARKER = "#"
    DELIMITER = ","

    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string."""
        output_parts: list[str] = []

        def encode(current_node: Optional[TreeNode]) -> None:
            if current_node is None:
                output_parts.append(self.NULL_MARKER)
                return
            output_parts.append(str(current_node.val))
            encode(current_node.left)
            encode(current_node.right)

        encode(root)
        return self.DELIMITER.join(output_parts)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decodes a string produced by serialize()."""
        token_iterator = iter(data.split(self.DELIMITER))

        def decode() -> Optional[TreeNode]:
            token = next(token_iterator)
            if token == self.NULL_MARKER:
                return None
            current_node = TreeNode(int(token))
            current_node.left = decode()
            current_node.right = decode()
            return current_node

        return decode()
```

---

## 12. Trie (Prefix Tree)

A trie is a tree specialized for storing strings. Each node represents a character. Paths from root to nodes represent prefixes. This makes prefix queries (autocomplete, "starts with") O(prefix_length) regardless of how many strings are stored.

**Where it shows up:** Autocomplete, spell-checkers, IP routing tables, longest common prefix, problems involving "given a list of words, find all words that..."

```python
class TrieNode:
    """Node in a trie.

    Attributes:
        children: Maps each character to the corresponding child TrieNode.
            Using a dict is more memory-efficient than a fixed-size array
            when the alphabet is large or usage is sparse.
        is_end_of_word: True if some inserted word ends exactly at this node.
            Necessary to distinguish "app" from "apple" — both go through
            the same path until the 'p' at depth 3.
    """

    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_end_of_word: bool = False


class Trie:
    """Prefix tree supporting insert, search, and prefix queries.

    All operations are O(L) where L is the length of the input word
    or prefix. This is independent of the number of words stored —
    a crucial property for autocomplete and dictionary problems.

    The space cost is O(total_characters_across_all_words) in the
    worst case (no shared prefixes), but typically much better since
    shared prefixes are stored only once.
    """

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Inserts a word into the trie."""
        current_node = self.root
        for character in word:
            if character not in current_node.children:
                current_node.children[character] = TrieNode()
            current_node = current_node.children[character]
        current_node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Returns True if the exact word was previously inserted."""
        final_node = self._walk_to_node(word)
        return final_node is not None and final_node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Returns True if any inserted word starts with prefix."""
        return self._walk_to_node(prefix) is not None

    def _walk_to_node(self, sequence: str) -> Optional[TreeNode]:
        """Helper: walks the trie following sequence's characters.

        Returns the final TrieNode reached, or None if any character
        is missing along the path. Search and starts_with differ only
        in whether they also require is_end_of_word at the final node.
        """
        current_node = self.root
        for character in sequence:
            if character not in current_node.children:
                return None
            current_node = current_node.children[character]
        return current_node
```

---

## 13. Segment Tree — Range Queries with Updates

A segment tree supports two operations on an array: update a single element, and query a range (sum, min, max, etc.) — both in O(log N). Useful when the array is mutable and you need many range queries.

This is the most advanced data structure on this list. It appears in L6+ Google interviews and competitive programming. Below is a sum segment tree; the same skeleton works for min/max with different combine functions.

```python
class SegmentTree:
    """Segment tree supporting point updates and range sum queries.

    Stores the array in a complete binary tree where each internal
    node represents the sum of its range. The leaves correspond to
    individual array elements.

    Both operations are O(log N) because update touches one root-to-leaf
    path, and range queries split into at most O(log N) precomputed
    range segments.

    For an array of size N, we allocate 4*N space — this is the
    standard safe upper bound that works regardless of whether N is
    a power of 2.
    """

    def __init__(self, source_array: list[int]) -> None:
        self.array_size = len(source_array)
        self.tree: list[int] = [0] * (4 * self.array_size)
        if self.array_size > 0:
            self._build(source_array, tree_index=1, left=0, right=self.array_size - 1)

    def _build(
        self,
        source_array: list[int],
        tree_index: int,
        left: int,
        right: int,
    ) -> None:
        """Recursively builds the segment tree from source_array.

        tree_index uses 1-based indexing so left child = 2*i,
        right child = 2*i+1 (standard segment tree convention).
        left and right are the array index bounds (inclusive) that
        this tree node represents.
        """
        if left == right:
            self.tree[tree_index] = source_array[left]
            return

        mid = (left + right) // 2
        self._build(source_array, 2 * tree_index, left, mid)
        self._build(source_array, 2 * tree_index + 1, mid + 1, right)
        self.tree[tree_index] = (
            self.tree[2 * tree_index] + self.tree[2 * tree_index + 1]
        )

    def update(self, array_index: int, new_value: int) -> None:
        """Sets array[array_index] = new_value in O(log N)."""
        self._update_helper(
            tree_index=1,
            segment_left=0,
            segment_right=self.array_size - 1,
            target_index=array_index,
            new_value=new_value,
        )

    def _update_helper(
        self,
        tree_index: int,
        segment_left: int,
        segment_right: int,
        target_index: int,
        new_value: int,
    ) -> None:
        if segment_left == segment_right:
            self.tree[tree_index] = new_value
            return

        mid = (segment_left + segment_right) // 2
        if target_index <= mid:
            self._update_helper(
                2 * tree_index, segment_left, mid, target_index, new_value
            )
        else:
            self._update_helper(
                2 * tree_index + 1,
                mid + 1,
                segment_right,
                target_index,
                new_value,
            )
        # Recompute this node's sum after the child changed
        self.tree[tree_index] = (
            self.tree[2 * tree_index] + self.tree[2 * tree_index + 1]
        )

    def range_sum(self, query_left: int, query_right: int) -> int:
        """Returns sum of array[query_left..query_right] in O(log N)."""
        return self._query_helper(
            tree_index=1,
            segment_left=0,
            segment_right=self.array_size - 1,
            query_left=query_left,
            query_right=query_right,
        )

    def _query_helper(
        self,
        tree_index: int,
        segment_left: int,
        segment_right: int,
        query_left: int,
        query_right: int,
    ) -> int:
        # Three cases for the relationship between [segment] and [query]:
        # 1. No overlap: this segment contributes nothing.
        if query_right < segment_left or query_left > segment_right:
            return 0

        # 2. Total overlap: this segment is fully inside the query range.
        if query_left <= segment_left and segment_right <= query_right:
            return self.tree[tree_index]

        # 3. Partial overlap: recurse into both children.
        mid = (segment_left + segment_right) // 2
        left_sum = self._query_helper(
            2 * tree_index, segment_left, mid, query_left, query_right
        )
        right_sum = self._query_helper(
            2 * tree_index + 1,
            mid + 1,
            segment_right,
            query_left,
            query_right,
        )
        return left_sum + right_sum
```

---

## 14. Problem Recognition Cheat Sheet

**"Find depth / height / max depth":** Postorder DFS.

**"K-th smallest in BST" / "Validate BST" / "BST as sorted":** Inorder traversal.

**"Path between two nodes" / "LCA":** Recursive LCA pattern.

**"Path sum" / "Root to leaf":** DFS with running sum (and backtracking if collecting all paths).

**"Maximum path through tree" / "Diameter":** Postorder returning subtree info, updating global max.

**"Level by level" / "Right side view" / "Zigzag":** BFS with level snapshots.

**"Serialize tree" / "Clone tree":** Preorder traversal with None markers.

**"Reconstruct tree from traversals":** Preorder gives the root, inorder splits subtrees.

**"Autocomplete" / "Prefix matching" / "Word dictionary":** Trie.

**"Range sum/min/max with updates":** Segment tree (or Fenwick tree for sums).

**"Check if node X is ancestor of Y":** DFS with entry/exit times, or path tracking.

**"All nodes at distance K":** Build parent map, then BFS treating the tree as an undirected graph.

---

## 15. Practice Problems — Priority Order

### Tier 1: Foundations (Do These First)

104 Maximum Depth of Binary Tree — Postorder.
226 Invert Binary Tree — Any traversal, swap children.
100 Same Tree — Recursive structural comparison.
101 Symmetric Tree — Mirror traversal.
102 Binary Tree Level Order Traversal — BFS with level snapshots.
98 Validate Binary Search Tree — Range pattern.
700 Search in a BST — BST search.
108 Convert Sorted Array to BST — Recursive median selection.

### Tier 2: Core Patterns

543 Diameter of Binary Tree — Postorder with global max.
110 Balanced Binary Tree — Postorder with -1 sentinel.
236 LCA of a Binary Tree — Recursive LCA.
235 LCA of a BST — Use BST ordering.
112 Path Sum — DFS with running sum.
113 Path Sum II — DFS with backtracking.
124 Maximum Path Sum — Postorder with global max.
105 Build Tree from Preorder and Inorder — Recursive split.
297 Serialize and Deserialize Binary Tree — Preorder with markers.
230 K-th Smallest Element in BST — Iterative inorder.

### Tier 3: Google L5/L6 Level

863 All Nodes Distance K in Binary Tree — Parent map + BFS.
1110 Delete Nodes And Return Forest — Postorder with parent tracking.
208 Implement Trie (Prefix Tree) — Trie basics.
212 Word Search II — Trie + DFS on grid.
295 Find Median from Data Stream — Two heaps (related to BST ideas).
99 Recover Binary Search Tree — Inorder + identify swap.
337 House Robber III — Tree DP returning two states.
968 Binary Tree Cameras — Postorder tree DP with state machine.
1305 All Elements in Two BSTs — Merge two inorder iterators.
315 Count of Smaller Numbers After Self — Segment tree or merge sort.

---

## 16. Common Mistakes That Cost Offers

**Validating a BST with only immediate-child comparisons.** Each node must satisfy constraints from ALL ancestors, not just its parent. Use the range pattern (`min_allowed`, `max_allowed`).

**Confusing depth and height.** Depth is measured from the root downward (root has depth 0). Height is measured from a node down to the deepest leaf (leaves have height 0). Many problems are sensitive to this — read the problem carefully and clarify with the interviewer if ambiguous.

**Forgetting that a "leaf" requires BOTH children to be None.** A node with one child and one None child is NOT a leaf. This bug shows up in path sum problems where you incorrectly terminate the recursion.

**Appending the path list instead of a copy.** `result.append(current_path)` stores a reference. When `current_path` is mutated by subsequent backtracking, the result is corrupted. Always `result.append(current_path[:])` or `result.append(list(current_path))`.

**Doing repeated work in tree DP.** If you compute `height(node)` at every node by recursive calls, that's O(N²). Instead, fuse the computation: a single postorder pass returns the height while also updating any global state you need (like diameter or max path sum).

**Mutating shared state across recursive branches.** When backtracking, every append must be paired with a pop after the recursive call returns. Otherwise sibling subtrees inherit corrupted state.

**Recursive solutions hitting Python's default 1000-recursion limit.** For very deep or skewed trees, recursive DFS may stack overflow. Either use iterative versions or call `sys.setrecursionlimit(10**6)` at the start. Mention this trade-off in interviews — it shows awareness of Python's limitations.

**Treating BST operations as O(log N) without checking balance.** They're O(log N) on BALANCED BSTs. On a degenerate BST (e.g., values inserted in sorted order), they're O(N). If the interviewer asks about worst case, mention this explicitly.

**Forgetting the `is_end_of_word` flag in tries.** Without it, you can't distinguish "app" from "apple." This is the most common trie bug.

**Building a segment tree of size `2*N` instead of `4*N`.** `2*N` only works when N is a power of 2. `4*N` is the safe universal bound. Saving the memory isn't worth the off-by-one bugs.

---

## 17. Learning Resources to Refer

Resources are ordered roughly from foundational to advanced. Pick by where you are, not by trying to consume all of them.

### Complexity reference
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/) — quick lookup table for the time/space costs annotated throughout this repo's `.py` solutions.
- [VisuAlgo — BST / Trees](https://visualgo.net/en/bst) — animate insert/search/delete and traversals step by step.

### Foundations (traversals, recursion, BST)
- [CSES Tree Algorithms](https://cses.fi/book/book.pdf) (Competitive Programmer's Handbook, ch. on trees) — clean, language-agnostic treatment of tree DP and traversals.
- [GeeksforGeeks — Binary Tree](https://www.geeksforgeeks.org/binary-tree-data-structure/) and [Binary Search Tree](https://www.geeksforgeeks.org/binary-search-tree-data-structure/) — broad problem catalog with worked examples.
- [Abdul Bari — Trees playlist (YouTube)](https://www.youtube.com/playlist?list=PLDN4rrl48XKpZkf03iYFl-O29szjTrs_O) — careful whiteboard explanations of BST operations and balancing.

### Interview patterns
- [NeetCode — Trees roadmap](https://neetcode.io/roadmap) — curated problem order with video walkthroughs; mirrors the Tier 1/2/3 progression in §15.
- [LeetCode Explore — Binary Tree](https://leetcode.com/explore/learn/card/data-structure-tree/) — guided card that drills traversal and recursion patterns.
- *Cracking the Coding Interview* (Gayle Laakmann McDowell), "Trees and Graphs" chapter — the canonical interview framing.

### Advanced (Trie, Segment Tree, balanced trees)
- [CP-Algorithms — Segment Tree](https://cp-algorithms.com/data_structures/segment_tree.html) and [Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html) — the definitive reference for range-query structures (§13).
- [USACO Guide — Trees & Tries](https://usaco.guide/) — progressively harder problems with editorial-quality solutions.
- [Open Data Structures](https://opendatastructures.org/) — free textbook covering AVL, Red-Black, and B-Trees (the self-balancing variants referenced in §7).
