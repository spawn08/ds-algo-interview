#!/usr/bin/env python3
"""
Generate the data file that powers the interactive learning site.

This script is the *single source of truth* glue: it reads the real solution
files from ``java/`` and ``python/`` (so the code shown on the site is always
exactly what's in the repo) and merges them with a curated catalog of
explanations, complexity analysis, and visualization bindings defined below.

Output: ``docs/data/problems.js`` -> ``window.SITE_DATA = {...}``

Usage:
    python3 scripts/generate_site.py
"""

import json
import os
import re
import textwrap

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(REPO_ROOT, "docs", "data", "problems.js")


def code(path):
    """Read a source file relative to the repo root."""
    full = os.path.join(REPO_ROOT, path)
    with open(full, "r", encoding="utf-8") as fh:
        return fh.read()


def _clean_statement(text):
    """Strip javadoc/markup noise from an extracted problem statement."""
    lines = []
    for ln in text.split("\n"):
        s = ln.strip()
        if s.startswith("@"):            # @link, @param, @return …
            continue
        s = s.replace("<p>", "").replace("</p>", "")
        s = re.sub(r"<link>.*?</link>", "", s)   # python docstring link tags
        s = re.sub(r"</?a[^>]*>", "", s)         # html anchors
        s = re.sub(r"\{@link[^}]*\}", "", s)     # javadoc {@link ...}
        if s.strip() in ("...", "*"):
            continue
        lines.append(s)
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def extract_statement(files):
    """Pull the problem statement from a source file's leading docstring/javadoc."""
    for f in files:
        path, src = f["path"], code(f["path"])
        if path.endswith(".py"):
            m = re.search(r'"""(.*?)"""', src, re.S)
            if m:
                text = m.group(1).strip()
                if "Definition for" in text or len(text) < 40:
                    continue  # skip Node stubs / too-short docstrings
                return _clean_statement(text)
        elif path.endswith(".java"):
            m = re.search(r"/\*\*(.*?)\*/", src, re.S)
            if m:
                body = "\n".join(re.sub(r"^\s*\*?", "", ln) for ln in m.group(1).split("\n"))
                cleaned = _clean_statement(body)
                if len(cleaned) >= 40:
                    return cleaned
    return None


def D(text):
    """Dedent + strip a triple-quoted block for clean storage."""
    return textwrap.dedent(text).strip("\n")


# ---------------------------------------------------------------------------
# Category metadata (controls ordering + landing-page blurbs)
# ---------------------------------------------------------------------------
CATEGORIES = [
    {"id": "arrays", "name": "Arrays & Hashing",
     "blurb": "The bread and butter of interviews. Master scanning, hashing for O(1) lookups, and prefix tricks."},
    {"id": "two-pointers", "name": "Two Pointers",
     "blurb": "Converging or chasing pointers turn many O(n^2) scans into O(n) on sorted or symmetric data."},
    {"id": "sliding-window", "name": "Sliding Window",
     "blurb": "Maintain a moving sub-range to answer 'best window' questions in a single pass."},
    {"id": "binary-search", "name": "Binary Search",
     "blurb": "Halve the search space each step. Works on sorted arrays and on monotonic answer spaces."},
    {"id": "stack", "name": "Stacks",
     "blurb": "LIFO ordering shines for matching, nesting, and 'most recent' problems."},
    {"id": "strings", "name": "Strings",
     "blurb": "Frequency counts, scanning, and DP applied to character sequences."},
    {"id": "dynamic-programming", "name": "Dynamic Programming",
     "blurb": "Break a problem into overlapping subproblems and reuse answers instead of recomputing."},
    {"id": "trees", "name": "Trees",
     "blurb": "Recursion is your friend: most tree problems reduce to 'solve children, combine at the parent'."},
    {"id": "graphs", "name": "Graphs",
     "blurb": "BFS, DFS, topological sort, and connectivity over nodes and edges (and grids in disguise)."},
    {"id": "misc", "name": "Greedy & Misc",
     "blurb": "Greedy choices, bit tricks, and search problems that don't fit a single bucket."},
]


# ---------------------------------------------------------------------------
# Problem catalog
# ---------------------------------------------------------------------------
PROBLEMS = [
    # ===================== ARRAYS & HASHING =====================
    {
        "id": "two-sum",
        "title": "Two Sum",
        "category": "arrays",
        "difficulty": "Easy",
        "tags": ["array", "hash map"],
        "link": "https://leetcode.com/problems/two-sum/",
        "summary": "Return the indices of the two numbers that add up to a target.",
        "idea": D("""
            For each number `x`, the only partner that completes the pair is `target - x`.
            So instead of searching the rest of the array for that partner (O(n) each time),
            we remember every number we've already seen in a **hash map** of `value -> index`.
            Lookups are O(1), so one pass solves it.
        """),
        "why": D("""
            **Why a hash map?** The brute-force solution uses two nested loops — O(n²) — because
            for every element it re-scans the array looking for the complement. A hash map trades
            a little memory for time: it answers "have I already seen the number I need?" in O(1).
            This is the canonical example of the *space-for-time* tradeoff that shows up everywhere
            in interviews. We store the index (not just the value) because the problem asks for
            positions, and we add each number *after* checking, which neatly avoids reusing the same
            element twice.
        """),
        "complexity": {"time": "O(n)", "space": "O(n)",
                       "note": "One pass; the map holds up to n entries."},
        "files": [
            {"lang": "python", "label": "Python — hash map", "path": "python/arrays/two_sum.py"},
            {"lang": "java", "label": "Java — hash map", "path": "java/src/com/dsalgo/arrays/twosum/TwoSumHashTable.java"},
            {"lang": "java", "label": "Java — brute force (O(n²))", "path": "java/src/com/dsalgo/arrays/twosum/TwoSumBruteForce.java"},
        ],
        "viz": {"type": "twoSumHash", "nums": [2, 7, 11, 15], "target": 9},
    },
    {
        "id": "two-sum-ii",
        "title": "Two Sum II — Sorted Input",
        "category": "two-pointers",
        "difficulty": "Medium",
        "tags": ["two pointers", "sorted array"],
        "link": "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/",
        "summary": "Find two numbers that sum to target in a sorted array, using O(1) extra space.",
        "idea": D("""
            Because the array is **sorted**, put one pointer at the smallest value and one at the
            largest. If their sum is too small, the only way to grow it is to move the left pointer
            right; if it's too big, move the right pointer left. Each step eliminates one element.
        """),
        "why": D("""
            **Why two pointers instead of a hash map?** Two Sum II adds a constraint — *constant
            extra space*. Sorting gives the array a monotonic structure we can exploit: the sum of
            the two ends behaves predictably as we move inward. That lets us replace the hash map's
            O(n) memory with two integer indices (O(1)). The same converging-pointer pattern powers
            3Sum, container-with-most-water, and many palindrome problems.
        """),
        "complexity": {"time": "O(n)", "space": "O(1)",
                       "note": "If you must sort first, sorting dominates at O(n log n)."},
        "files": [
            {"lang": "python", "label": "Python — two pointers", "path": "python/arrays/two_sum_II.py"},
            {"lang": "java", "label": "Java — two pointers", "path": "java/src/com/dsalgo/arrays/twosum/TwoSumUsingPointers.java"},
        ],
        "viz": {"type": "twoPointers", "nums": [2, 7, 11, 15], "target": 9},
    },
    {
        "id": "max-subarray",
        "title": "Maximum Subarray (Kadane's)",
        "category": "arrays",
        "difficulty": "Medium",
        "tags": ["dynamic programming", "greedy"],
        "link": "https://leetcode.com/problems/maximum-subarray/",
        "summary": "Find the contiguous subarray with the largest sum.",
        "idea": D("""
            Walk left to right keeping a `current` running sum. At each element decide: is it better
            to **extend** the previous subarray or **start fresh** at this element? That's
            `current = max(x, current + x)`. Track the best `current` ever seen.
        """),
        "why": D("""
            **Why this works (the DP insight):** the key realization is that the best subarray
            *ending at index i* either builds on the best subarray ending at `i-1` or restarts at
            `i`. Once a running sum goes negative it can only hurt whatever comes next, so we drop it.
            This turns an O(n²) "try every subarray" search into a single O(1)-memory pass. It's the
            gateway problem for understanding dynamic programming as "reuse the answer to the smaller
            prefix."
        """),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "files": [
            {"lang": "python", "label": "Python — Kadane", "path": "python/arrays/max_path_sum.py"},
            {"lang": "java", "label": "Java — Kadane (two forms)", "path": "java/src/com/dsalgo/arrays/subarray/MaximumSubArray.java"},
        ],
        "viz": {"type": "kadane", "nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]},
    },
    {
        "id": "max-sum-subarray-k",
        "title": "Maximum Sum Subarray of Size K",
        "category": "sliding-window",
        "difficulty": "Easy",
        "tags": ["sliding window"],
        "link": "https://www.geeksforgeeks.org/find-maximum-minimum-sum-subarray-size-k/",
        "summary": "Largest sum among all fixed-length windows of size k.",
        "idea": D("""
            Sum the first `k` elements, then **slide** the window one step at a time: add the new
            right element and subtract the one that fell off the left. The window sum updates in O(1)
            per step instead of being recomputed from scratch.
        """),
        "why": D("""
            **Why a fixed sliding window?** Recomputing each window's sum is O(n·k). The window only
            changes by two elements between consecutive positions, so we maintain the sum
            incrementally. Recognizing "fixed-size window + running aggregate" is the simplest member
            of the sliding-window family and a frequent warm-up question.
        """),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "files": [
            {"lang": "java", "label": "Java — sliding window", "path": "java/src/com/dsalgo/arrays/subarray/MaximumSumSubArrayWithK.java"},
        ],
        "viz": {"type": "fixedWindow", "nums": [100, 200, 300, 400], "k": 2},
    },
    {
        "id": "max-subarray-distinct-k",
        "title": "Max Sum Subarray of Size K (Distinct)",
        "category": "sliding-window",
        "difficulty": "Medium",
        "tags": ["sliding window", "hash map"],
        "link": "https://leetcode.com/problems/maximum-sum-of-distinct-subarrays-with-length-k/",
        "summary": "Largest sum among size-k windows whose elements are all distinct.",
        "idea": D("""
            Slide a window of size `k` while keeping a **frequency map** of the elements inside it.
            A window is valid only when it has exactly `k` *distinct* values (map size == k). Track
            the max sum over all valid windows.
        """),
        "why": D("""
            **Why add a hash map to the window?** The distinctness constraint can't be checked by the
            sum alone. A counter lets us test "are all k elements unique?" in O(1) by comparing the
            number of keys to `k`, and lets us cleanly add/remove elements as the window moves. This
            is the variable-validity flavor of sliding window where a secondary structure tracks the
            window's invariant.
        """),
        "complexity": {"time": "O(n)", "space": "O(k)"},
        "files": [
            {"lang": "python", "label": "Python — window + counter", "path": "python/arrays/max_subarray_size_k.py"},
        ],
        "viz": {"type": "fixedWindow", "nums": [1, 5, 4, 2, 9, 9, 9], "k": 3, "distinct": True},
    },
    {
        "id": "longest-consecutive-sequence",
        "title": "Longest Consecutive Sequence",
        "category": "arrays",
        "difficulty": "Medium",
        "tags": ["hash set"],
        "link": "https://leetcode.com/problems/longest-consecutive-sequence/",
        "summary": "Length of the longest run of consecutive integers, in O(n).",
        "idea": D("""
            Drop everything into a **hash set**. A number `x` can only be the *start* of a run if
            `x-1` is absent. From each such start, walk `x+1, x+2, ...` counting the streak.
        """),
        "why": D("""
            **Why a set, and why the 'start' check?** Sorting would solve it in O(n log n), but the
            problem demands O(n). A set gives O(1) membership tests. The subtle trick is only
            extending from sequence *starts* — without it you'd re-walk the same run from every
            member and degrade to O(n²). Because each number is visited at most twice total
            (once as a candidate, once while extending a run), the whole thing is linear.
        """),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "files": [
            {"lang": "python", "label": "Python — hash set", "path": "python/arrays/longest_consecutive_sequence.py"},
        ],
    },
    {
        "id": "rotate-image",
        "title": "Rotate Image",
        "category": "arrays",
        "difficulty": "Medium",
        "tags": ["matrix", "in-place"],
        "link": "https://leetcode.com/problems/rotate-image/",
        "summary": "Rotate an n×n matrix 90° clockwise, in place.",
        "idea": D("""
            A 90° clockwise rotation equals two reflections: **transpose** the matrix (swap across
            the main diagonal), then **reverse each row**. Both steps only swap elements, so no second
            matrix is needed.
        """),
        "why": D("""
            **Why transpose + reverse instead of a copy?** The obvious approach allocates a new matrix
            and maps `new[j][n-1-i] = old[i][j]` — simple but O(n²) extra space. Decomposing the
            rotation into two in-place reflections keeps memory at O(1). It's a great example of
            re-expressing a geometric transform as composable, cache-friendly element swaps.
        """),
        "complexity": {"time": "O(n²)", "space": "O(1)"},
        "files": [
            {"lang": "python", "label": "Python — transpose + reverse", "path": "python/arrays/rotate_image.py"},
        ],
        "viz": {"type": "matrixRotate", "matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
    },
    {
        "id": "contains-duplicate",
        "title": "Contains Duplicate",
        "category": "arrays",
        "difficulty": "Easy",
        "tags": ["hash set"],
        "link": "https://leetcode.com/problems/contains-duplicate/",
        "summary": "Return true if any value appears at least twice.",
        "idea": D("""
            Add values to a **hash set** as you scan. If you ever try to add one that's already there,
            you've found a duplicate.
        """),
        "why": D("""
            **Why a set?** Sorting then scanning neighbors is O(n log n); a nested-loop comparison is
            O(n²). A hash set answers "seen before?" in O(1), giving an O(n) single pass for O(n)
            memory — the simplest illustration of hashing for membership.
        """),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "files": [
            {"lang": "java", "label": "Java — hash set", "path": "java/src/com/dsalgo/arrays/ContainsDuplicate.java"},
        ],
    },
    {
        "id": "smallest-subarray-or",
        "title": "Smallest Subarray with OR ≥ K",
        "category": "sliding-window",
        "difficulty": "Medium",
        "tags": ["sliding window", "bit manipulation"],
        "link": "https://www.geeksforgeeks.org/smallest-subarray-such-that-its-bitwise-or-is-at-least-k/",
        "summary": "Shortest subarray whose bitwise OR is at least K.",
        "idea": D("""
            Bitwise OR only ever *adds* bits as the window grows, but removing the left element may
            drop bits, so OR isn't simply reversible. Keep a **per-bit count** (32 counters) of how
            many window elements set each bit; rebuild the OR from bits whose count is positive. Grow
            right, then shrink left while the OR still satisfies K.
        """),
        "why": D("""
            **Why a bit-count array?** A plain sliding window works when the aggregate can be undone
            in O(1) (like a sum). OR can't be undone directly. Counting contributions per bit makes
            removal reversible: a bit stays set only while at least one window element provides it.
            This "make the window aggregate reversible" idea generalizes to ANDs, GCDs, and frequency
            constraints. A brute-force O(n²) version is included for contrast.
        """),
        "complexity": {"time": "O(n·32)", "space": "O(32)",
                       "note": "Constant 32-bit factor; effectively O(n)."},
        "files": [
            {"lang": "java", "label": "Java — window + bit counts", "path": "java/src/com/dsalgo/arrays/subarray/SubarrayOR.java"},
        ],
    },
    {
        "id": "alternate-sorting",
        "title": "Alternate Sorting (max, min, …)",
        "category": "arrays",
        "difficulty": "Easy",
        "tags": ["sorting", "two pointers"],
        "link": "https://www.geeksforgeeks.org/alternative-sorting/",
        "summary": "Arrange a sorted array as max, min, 2nd-max, 2nd-min, …",
        "idea": D("""
            Sort the array, then read it from both ends inward: take the largest, then the smallest,
            then the next-largest, and so on, writing into the output in alternating order.
        """),
        "why": D("""
            **Why sort first?** Once sorted, the i-th largest and i-th smallest are just the two ends,
            so a single two-pointer pass produces the alternating layout. Sorting dominates the cost;
            the rearrangement itself is O(n).
        """),
        "complexity": {"time": "O(n log n)", "space": "O(n)"},
        "files": [
            {"lang": "java", "label": "Java — sort + two pointers", "path": "java/src/com/dsalgo/arrays/AlternateSorting.java"},
        ],
    },

    # ===================== STRINGS =====================
    {
        "id": "valid-parentheses",
        "title": "Valid Parentheses",
        "category": "stack",
        "difficulty": "Easy",
        "tags": ["stack"],
        "link": "https://leetcode.com/problems/valid-parentheses/",
        "summary": "Decide whether brackets are correctly opened and closed in order.",
        "idea": D("""
            Push every opening bracket onto a **stack**. On a closing bracket, the most recently
            opened bracket must match — so pop and compare. Valid iff nothing mismatches and the
            stack ends empty.
        """),
        "why": D("""
            **Why a stack?** Nesting is inherently last-in-first-out: the bracket you must close next
            is always the most recent unclosed one. A stack models that exactly. The Java file shows
            two takes — a hand-rolled array "stack" and a `Deque` — to highlight that a stack is an
            *interface/behavior*, not a specific class.
        """),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "files": [
            {"lang": "python", "label": "Python — dict + stack", "path": "python/strings/valid_parentheses.py"},
            {"lang": "java", "label": "Java — Deque & array stack", "path": "java/src/com/dsalgo/stacks/ValidParentheses.java"},
        ],
        "viz": {"type": "stackParens", "s": "([]{})"},
    },
    {
        "id": "valid-anagram",
        "title": "Valid Anagram",
        "category": "strings",
        "difficulty": "Easy",
        "tags": ["hash map", "counting"],
        "link": "https://leetcode.com/problems/valid-anagram/",
        "summary": "Check whether two strings are anagrams of each other.",
        "idea": D("""
            Anagrams use the exact same letters with the same multiplicities. Compare **character
            frequency counts** — if every character appears the same number of times in both
            strings, they're anagrams.
        """),
        "why": D("""
            **Why counting beats sorting?** Sorting both strings and comparing is O(n log n). Counting
            characters is O(n) with O(1) space for a fixed alphabet (or O(k) for k distinct chars).
            `Counter` makes the intent crystal clear. Early-exit on length mismatch avoids wasted work.
        """),
        "complexity": {"time": "O(n)", "space": "O(1)",
                       "note": "Alphabet is bounded, so the counter is constant size."},
        "files": [
            {"lang": "python", "label": "Python — Counter", "path": "python/strings/valid_anagrams.py"},
        ],
    },
    {
        "id": "valid-palindrome",
        "title": "Valid Palindrome",
        "category": "two-pointers",
        "difficulty": "Easy",
        "tags": ["two pointers", "string"],
        "link": "https://leetcode.com/problems/valid-palindrome/",
        "summary": "Ignoring case and non-alphanumerics, is the string a palindrome?",
        "idea": D("""
            Normalize to lowercase alphanumerics, then put one pointer at each end and walk inward,
            comparing characters. Any mismatch means it's not a palindrome.
        """),
        "why": D("""
            **Why two pointers?** A palindrome is symmetric about its center, so comparing mirrored
            positions is the natural check and uses O(1) extra space beyond the cleaned string.
            Converging pointers on a symmetric structure is a pattern worth internalizing.
        """),
        "complexity": {"time": "O(n)", "space": "O(n)",
                       "note": "O(n) for the cleaned copy; the scan itself is O(1) space."},
        "files": [
            {"lang": "python", "label": "Python — two pointers", "path": "python/strings/valid_palindrome.py"},
        ],
        "viz": {"type": "stringTwoPointer", "s": "A man, a plan, a canal: Panama"},
    },
    {
        "id": "group-anagrams",
        "title": "Group Anagrams",
        "category": "strings",
        "difficulty": "Medium",
        "tags": ["hash map", "sorting"],
        "link": "https://leetcode.com/problems/group-anagrams/",
        "summary": "Cluster words that are anagrams of one another.",
        "idea": D("""
            All anagrams share the same sorted letters, so the **sorted word** is a canonical key.
            Bucket every word under its sorted form in a hash map; each bucket is one anagram group.
        """),
        "why": D("""
            **Why a hash map keyed by a canonical form?** We need a signature that's identical for
            anagrams and different otherwise. Sorting the letters is the simplest such signature; a
            character-count tuple is an O(n)-per-word alternative (also shown). The map groups in a
            single pass.
        """),
        "complexity": {"time": "O(n·k log k)", "space": "O(n·k)",
                       "note": "n words of length up to k; sorting each is k log k."},
        "files": [
            {"lang": "python", "label": "Python — sorted-key & tuple-key", "path": "python/strings/group_anagrams.py"},
        ],
    },
    {
        "id": "longest-substring-no-repeat",
        "title": "Longest Substring Without Repeating Characters",
        "category": "sliding-window",
        "difficulty": "Medium",
        "tags": ["sliding window", "hash map"],
        "link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
        "summary": "Length of the longest substring with all-unique characters.",
        "idea": D("""
            Grow a window to the right. Remember the **last index** each character was seen. When you
            hit a repeat that's inside the current window, jump the left edge to just past the
            previous occurrence. Track the widest window.
        """),
        "why": D("""
            **Why store last-seen indices?** A naive window slides the left pointer one step at a time
            on a conflict; storing the previous index lets us jump it directly, so each character is
            processed once — O(n). The Java file even shows three escalating versions (HashSet →
            HashMap → fixed 256-int array) to illustrate squeezing constants out of the same idea.
        """),
        "complexity": {"time": "O(n)", "space": "O(min(n, alphabet))"},
        "files": [
            {"lang": "python", "label": "Python — last-seen map", "path": "python/sliding_window/lcs_without_repeating_character.py"},
            {"lang": "java", "label": "Java — set / map / array", "path": "java/src/com/dsalgo/strings/LongestSubstringWithoutRepeatingCharacters.java"},
        ],
        "viz": {"type": "slidingWindow", "s": "abcabcbb"},
    },
    {
        "id": "reverse-string",
        "title": "Reverse String",
        "category": "two-pointers",
        "difficulty": "Easy",
        "tags": ["two pointers", "in-place"],
        "link": "https://practice.geeksforgeeks.org/problems/reverse-a-string/",
        "summary": "Reverse a string in place by swapping ends inward.",
        "idea": D("""
            Swap the first and last characters, then the second and second-to-last, and so on, until
            the two pointers meet in the middle.
        """),
        "why": D("""
            **Why two pointers?** Reversing is a symmetric swap problem — exactly what converging
            pointers do, touching each character once and using O(1) extra space (beyond the char
            array needed because Java strings are immutable).
        """),
        "complexity": {"time": "O(n)", "space": "O(n)",
                       "note": "O(n) only because the string is copied to a mutable char array."},
        "files": [
            {"lang": "java", "label": "Java — swap inward", "path": "java/src/com/dsalgo/strings/ReverseString.java"},
        ],
    },

    # ===================== DYNAMIC PROGRAMMING =====================
    {
        "id": "lcs",
        "title": "Longest Common Subsequence",
        "category": "dynamic-programming",
        "difficulty": "Medium",
        "tags": ["dynamic programming", "2D DP"],
        "link": "https://leetcode.com/problems/longest-common-subsequence/",
        "summary": "Length of the longest subsequence common to two strings.",
        "idea": D("""
            Build a table `dp[i][j]` = LCS length of the first `i` chars of one string and first `j`
            of the other. If the current characters match, `dp[i][j] = 1 + dp[i-1][j-1]`; otherwise
            it's the better of dropping one character from either string: `max(dp[i-1][j], dp[i][j-1])`.
        """),
        "why": D("""
            **Why 2D DP?** The choices ("does this pair of characters belong to the subsequence?")
            overlap massively across prefixes. A 2D table memoizes every (prefix, prefix) subproblem
            so each is solved once. This grid recurrence is the template for edit distance, longest
            common substring, and sequence-alignment problems.
        """),
        "complexity": {"time": "O(m·n)", "space": "O(m·n)",
                       "note": "Reducible to O(min(m,n)) with rolling rows."},
        "files": [
            {"lang": "python", "label": "Python — 2D table", "path": "python/dynamic_programming/longest_common_sequence.py"},
            {"lang": "java", "label": "Java — 2D table", "path": "java/src/com/dsalgo/strings/LongestCommonSubsequence.java"},
        ],
        "viz": {"type": "dpGrid", "a": "abcde", "b": "ace", "mode": "subsequence"},
    },
    {
        "id": "longest-common-substring",
        "title": "Longest Common Substring",
        "category": "dynamic-programming",
        "difficulty": "Medium",
        "tags": ["dynamic programming", "2D DP"],
        "link": "https://www.geeksforgeeks.org/longest-common-substring-dp-29/",
        "summary": "Length of the longest *contiguous* run common to two strings.",
        "idea": D("""
            Same grid as LCS, but with one twist: a substring must be contiguous, so a mismatch
            **resets** the run to 0. `dp[i][j] = 1 + dp[i-1][j-1]` on a match, else `0`. The answer is
            the maximum cell, not the corner.
        """),
        "why": D("""
            **Why reset on mismatch?** Subsequences may skip characters (so they carry forward
            `max(...)`); substrings cannot. Zeroing on mismatch encodes "the contiguous run ended
            here." Contrasting this with LCS makes the subsequence-vs-substring distinction concrete.
        """),
        "complexity": {"time": "O(m·n)", "space": "O(m·n)"},
        "files": [
            {"lang": "python", "label": "Python — 2D table", "path": "python/dynamic_programming/longest_common_substring.py"},
        ],
        "viz": {"type": "dpGrid", "a": "ABABC", "b": "BABCA", "mode": "substring"},
    },
    {
        "id": "house-robber",
        "title": "House Robber",
        "category": "dynamic-programming",
        "difficulty": "Medium",
        "tags": ["dynamic programming"],
        "link": "https://leetcode.com/problems/house-robber/",
        "summary": "Max money robbable without taking two adjacent houses.",
        "idea": D("""
            At each house you either **skip** it (keep the best total up to the previous house) or
            **rob** it (its money plus the best total up to two houses back):
            `dp[i] = max(dp[i-1], nums[i] + dp[i-2])`. Only the last two results matter, so track two
            rolling variables.
        """),
        "why": D("""
            **Why two variables instead of an array?** The recurrence only ever looks back one and two
            steps, so storing the whole `dp` array is wasteful. Collapsing it to `prev1`/`prev2` keeps
            the O(n) time but drops memory to O(1) — the classic "rolling DP" space optimization.
        """),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "files": [
            {"lang": "python", "label": "Python — rolling DP", "path": "python/dynamic_programming/house_robber.py"},
        ],
    },

    # ===================== BINARY SEARCH =====================
    {
        "id": "binary-search",
        "title": "Binary Search",
        "category": "binary-search",
        "difficulty": "Easy",
        "tags": ["binary search"],
        "link": "https://leetcode.com/problems/binary-search/",
        "summary": "Find a target in a sorted array in O(log n).",
        "idea": D("""
            Maintain a `[low, high]` range. Look at the middle: if it's the target you're done; if the
            middle is too big, discard the right half; otherwise discard the left. Each step halves the
            range.
        """),
        "why": D("""
            **Why it's O(log n):** sorted order means one comparison tells you which half can possibly
            contain the target, so you throw away half the candidates every step. Note the
            `low + (high - low) / 2` midpoint — it avoids the classic integer-overflow bug of
            `(low + high) / 2`. Both iterative and recursive forms are shown.
        """),
        "complexity": {"time": "O(log n)", "space": "O(1)",
                       "note": "Recursive form uses O(log n) stack space."},
        "files": [
            {"lang": "java", "label": "Java — iterative & recursive", "path": "java/src/com/dsalgo/searching/BinarySearch.java"},
        ],
        "viz": {"type": "binarySearch", "nums": [1, 3, 5, 7, 9, 11, 13, 15], "target": 11},
    },
    {
        "id": "search-rotated-array",
        "title": "Search in Rotated Sorted Array",
        "category": "binary-search",
        "difficulty": "Medium",
        "tags": ["binary search"],
        "link": "https://leetcode.com/problems/search-in-rotated-sorted-array/",
        "summary": "Binary search on a sorted array that's been rotated at an unknown pivot.",
        "idea": D("""
            At each midpoint, **one half is always still sorted**. Detect which (compare `nums[low]`
            to `nums[mid]`), check whether the target lies within that sorted half's range, and recurse
            into the correct side.
        """),
        "why": D("""
            **Why does binary search still apply?** Rotation breaks global order, but locally one side
            of `mid` remains sorted, which restores the "which half can contain the target?" decision
            that binary search needs. This "find the sorted half" trick is the heart of all
            rotated-array problems.
        """),
        "complexity": {"time": "O(log n)", "space": "O(1)"},
        "files": [
            {"lang": "python", "label": "Python — distinct values", "path": "python/binary_search/rotated_sorted_array.py"},
        ],
    },
    {
        "id": "search-rotated-array-ii",
        "title": "Search in Rotated Sorted Array II",
        "category": "binary-search",
        "difficulty": "Medium",
        "tags": ["binary search"],
        "link": "https://leetcode.com/problems/search-in-rotated-sorted-array-ii/",
        "summary": "Same as above, but duplicates are allowed.",
        "idea": D("""
            Duplicates create ambiguity: when `nums[low] == nums[mid] == nums[high]` you can't tell
            which half is sorted. Handle that case by **shrinking both ends inward by one** and
            continuing; otherwise it's identical to the no-duplicates version.
        """),
        "why": D("""
            **Why the worst case degrades to O(n):** the `low++/high--` fallback can fire on every step
            when the array is full of duplicates (e.g. `[1,1,1,1]`), so we can't guarantee halving.
            This problem is a great lesson that duplicates can quietly destroy a logarithmic
            guarantee.
        """),
        "complexity": {"time": "O(log n) avg, O(n) worst", "space": "O(1)"},
        "files": [
            {"lang": "python", "label": "Python — with duplicates", "path": "python/binary_search/rotated_sorted_array_ii.py"},
        ],
    },

    # ===================== TREES =====================
    {
        "id": "tree-traversals",
        "title": "Binary Tree Traversals (DFS)",
        "category": "trees",
        "difficulty": "Easy",
        "tags": ["tree", "dfs", "recursion"],
        "link": "https://leetcode.com/problems/binary-tree-inorder-traversal/",
        "summary": "In-order, pre-order, and post-order traversal — recursive and iterative.",
        "idea": D("""
            All three DFS orders visit the same nodes; they differ only in *when* the current node is
            recorded relative to its subtrees. **Pre** = node, left, right. **In** = left, node, right.
            **Post** = left, right, node. The iterative in-order uses an explicit stack to mimic the
            call stack.
        """),
        "why": D("""
            **Why recursion (and when a stack)?** Trees are recursive by definition, so recursive DFS
            reads almost like the definition of each order. The explicit-stack version matters when
            recursion depth could overflow or when an interviewer bans recursion — the stack literally
            replays what the call stack would do. In-order on a BST yields sorted output, which is why
            the order you pick matters.
        """),
        "complexity": {"time": "O(n)", "space": "O(h)",
                       "note": "h = tree height; O(n) worst case for a skewed tree."},
        "files": [
            {"lang": "python", "label": "Python — recursive (all orders)", "path": "python/trees/tree_traversal_dfs.py"},
            {"lang": "python", "label": "Python — iterative in-order", "path": "python/trees/tree_iterative_traversal.py"},
            {"lang": "python", "label": "Python — in-order helper", "path": "python/trees/bt_inorder_traversal.py"},
            {"lang": "java", "label": "Java — recursive (all orders)", "path": "java/src/com/dsalgo/trees/BinaryTreeTraversal.java"},
        ],
        "viz": {"type": "treeTraversal", "tree": [1, 2, 3, 4, 5, None, 6]},
    },
    {
        "id": "level-order",
        "title": "Binary Tree Level Order Traversal (BFS)",
        "category": "trees",
        "difficulty": "Medium",
        "tags": ["tree", "bfs", "queue"],
        "link": "https://leetcode.com/problems/binary-tree-level-order-traversal/",
        "summary": "Return node values grouped level by level, top to bottom.",
        "idea": D("""
            Use a **queue**. Process the tree in waves: record how many nodes are in the current level
            (the queue size), pop exactly that many, collect their values, and enqueue their children.
            Each wave is one level.
        """),
        "why": D("""
            **Why a queue (BFS) and the 'level size' snapshot?** Levels are explored breadth-first, and
            a queue's FIFO order naturally processes nodes in arrival (level) order. Snapshotting the
            queue size before draining a level is the trick that lets us group results per level
            instead of one flat list.
        """),
        "complexity": {"time": "O(n)", "space": "O(n)",
                       "note": "Queue holds up to one full level (~n/2 leaves)."},
        "files": [
            {"lang": "python", "label": "Python — BFS by level", "path": "python/trees/bt_level_order_traversal.py"},
            {"lang": "java", "label": "Java — BFS (two variants)", "path": "java/src/com/dsalgo/trees/LevelOrderTraversal.java"},
        ],
        "viz": {"type": "treeLevelOrder", "tree": [3, 9, 20, None, None, 15, 7]},
    },
    {
        "id": "max-depth",
        "title": "Maximum Depth of Binary Tree",
        "category": "trees",
        "difficulty": "Easy",
        "tags": ["tree", "dfs", "recursion"],
        "link": "https://leetcode.com/problems/maximum-depth-of-binary-tree/",
        "summary": "Number of nodes on the longest root-to-leaf path.",
        "idea": D("""
            A tree's depth is `1 + max(depth(left), depth(right))`, with an empty tree having depth 0.
            Recurse and combine.
        """),
        "why": D("""
            **Why recursion fits:** depth is defined in terms of subtree depths — a textbook
            self-similar problem. The recursion mirrors the definition exactly and visits each node
            once.
        """),
        "complexity": {"time": "O(n)", "space": "O(h)"},
        "files": [
            {"lang": "python", "label": "Python — recursive", "path": "python/trees/bt_max_depth.py"},
        ],
    },
    {
        "id": "balanced-tree",
        "title": "Balanced Binary Tree",
        "category": "trees",
        "difficulty": "Easy",
        "tags": ["tree", "dfs"],
        "link": "https://leetcode.com/problems/balanced-binary-tree/",
        "summary": "Is every node's two subtrees' heights within 1 of each other?",
        "idea": D("""
            Compute height bottom-up, but have the recursion **return -1 as a sentinel** the moment any
            subtree is unbalanced. That short-circuits the rest of the work — once you know it's
            unbalanced, you stop.
        """),
        "why": D("""
            **Why the -1 sentinel instead of checking height separately?** The naive approach computes
            height at every node and re-walks subtrees to verify balance — O(n²). Folding the balance
            check into the height computation (and bailing with -1) makes it a single O(n) pass. This
            "compute + validate in one traversal, signal failure with a sentinel" pattern is widely
            reusable.
        """),
        "complexity": {"time": "O(n)", "space": "O(h)"},
        "files": [
            {"lang": "python", "label": "Python — height + sentinel", "path": "python/trees/check_balanced_binary_tree.py"},
        ],
    },
    {
        "id": "max-path-sum",
        "title": "Binary Tree Maximum Path Sum",
        "category": "trees",
        "difficulty": "Hard",
        "tags": ["tree", "dfs"],
        "link": "https://leetcode.com/problems/binary-tree-maximum-path-sum/",
        "summary": "Largest sum along any path (need not pass through the root).",
        "idea": D("""
            For each node compute the best **downward gain** from each child, clamping negatives to 0
            (a negative branch is better skipped). The best path *through* this node is
            `node + leftGain + rightGain`; update a global max with it. Return `node + max(left, right)`
            upward, since a parent can only extend one side.
        """),
        "why": D("""
            **Why two different quantities (global vs. returned)?** A path that bends at a node can use
            both children, but a path that *continues to the parent* can only use one. Conflating these
            is the classic bug. Clamping negatives to 0 encodes the greedy "only take a branch if it
            helps." It's the definitive lesson in separating "answer at this node" from "value passed
            to the parent."
        """),
        "complexity": {"time": "O(n)", "space": "O(h)"},
        "files": [
            {"lang": "python", "label": "Python — DFS with global max", "path": "python/trees/binary_tree_max_path_sum.py"},
            {"lang": "java", "label": "Java — DFS with global max", "path": "java/src/com/dsalgo/trees/MaxPathSum.java"},
        ],
    },
    {
        "id": "lowest-common-ancestor",
        "title": "Lowest Common Ancestor of a Binary Tree",
        "category": "trees",
        "difficulty": "Medium",
        "tags": ["tree", "dfs", "recursion"],
        "link": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/",
        "summary": "Deepest node that has both target nodes as descendants.",
        "idea": D("""
            Recurse post-order. Each call reports back whether `p` or `q` was found below it. The
            **first node that sees one target on its left and the other on its right** (or is itself a
            target with the other beneath it) is the LCA.
        """),
        "why": D("""
            **Why post-order (children first)?** You can't decide if a node is the common ancestor until
            you know what each subtree contains, so the node must be processed *after* its children.
            Letting each call bubble up "I found one of them" turns a potentially O(n²) search into a
            single O(n) traversal.
        """),
        "complexity": {"time": "O(n)", "space": "O(h)"},
        "files": [
            {"lang": "python", "label": "Python — post-order DFS", "path": "python/trees/lowest_common_ancestor.py"},
        ],
    },
    {
        "id": "search-bst",
        "title": "Search in a Binary Search Tree",
        "category": "trees",
        "difficulty": "Easy",
        "tags": ["bst", "binary search"],
        "link": "https://leetcode.com/problems/search-in-a-binary-search-tree/",
        "summary": "Find the subtree rooted at a given value in a BST.",
        "idea": D("""
            Use the BST ordering: if the target is smaller than the current node go left, if larger go
            right, otherwise you've found it. It's binary search expressed on tree structure.
        """),
        "why": D("""
            **Why a BST gives O(h):** the ordering invariant means each comparison eliminates an entire
            subtree, just like binary search eliminates half an array. On a balanced BST that's
            O(log n); on a degenerate (linked-list-shaped) BST it's O(n) — motivating self-balancing
            trees.
        """),
        "complexity": {"time": "O(h)", "space": "O(h)"},
        "files": [
            {"lang": "java", "label": "Java — recursive", "path": "java/src/com/dsalgo/trees/SearchBST.java"},
        ],
    },
    {
        "id": "invert-tree",
        "title": "Invert Binary Tree",
        "category": "trees",
        "difficulty": "Easy",
        "tags": ["tree", "recursion"],
        "link": "https://leetcode.com/problems/invert-binary-tree/",
        "summary": "Mirror a binary tree by swapping every node's children.",
        "idea": D("""
            Swap the left and right child of the current node, then recurse into both children. The
            whole tree ends up mirrored.
        """),
        "why": D("""
            **Why it's the 'hello world' of tree recursion:** the transformation is purely local (swap
            two pointers) and recursion handles propagation. It cements the "do a tiny thing at each
            node, recurse on children" mental model.
        """),
        "complexity": {"time": "O(n)", "space": "O(h)"},
        "files": [
            {"lang": "java", "label": "Java — recursive swap", "path": "java/src/com/dsalgo/trees/InvertBinaryTreeRecursive.java"},
        ],
    },
    {
        "id": "branch-sums",
        "title": "Branch Sums",
        "category": "trees",
        "difficulty": "Easy",
        "tags": ["tree", "dfs"],
        "link": "https://www.algoexpert.io/questions/Branch%20Sums",
        "summary": "List the sum of every root-to-leaf path, left to right.",
        "idea": D("""
            Carry a running sum down the tree. At a leaf, the running sum is one branch's total — record
            it. Recursing left before right yields the sums in left-to-right order.
        """),
        "why": D("""
            **Why pass the running sum down (instead of returning it up)?** Each branch's total depends
            on the path taken from the root, so accumulating *on the way down* is natural and avoids
            recombining partial results. Pre-order left-then-right recursion gives the required output
            order for free.
        """),
        "complexity": {"time": "O(n)", "space": "O(h)"},
        "files": [
            {"lang": "java", "label": "Java — DFS with running sum", "path": "java/src/com/dsalgo/trees/BranchSum.java"},
        ],
    },

    # ===================== GRAPHS =====================
    {
        "id": "graph-traversal",
        "title": "Graph Traversal — BFS & DFS",
        "category": "graphs",
        "difficulty": "Easy",
        "tags": ["graph", "bfs", "dfs"],
        "link": "https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/",
        "summary": "Visit every reachable node using a queue (BFS) or a stack/recursion (DFS).",
        "idea": D("""
            Both keep a **visited set** to avoid revisiting nodes (graphs can have cycles, unlike
            trees). BFS uses a **queue** to explore in widening rings; DFS uses a **stack** (or the call
            stack) to plunge deep before backtracking.
        """),
        "why": D("""
            **Why the visited set, and queue vs. stack?** Without a visited set a cycle loops forever.
            The only structural difference between BFS and DFS is the container: FIFO queue → nearest
            nodes first (shortest path in unweighted graphs); LIFO stack → deepest path first (cheap
            cycle/connectivity checks). Internalizing "swap the container to swap the strategy" is the
            key takeaway.
        """),
        "complexity": {"time": "O(V + E)", "space": "O(V)"},
        "files": [
            {"lang": "python", "label": "Python — BFS, DFS (rec & iter)", "path": "python/graphs/graph_traversal.py"},
        ],
        "viz": {"type": "graphTraversal",
                "graph": {"A": ["B", "C"], "B": ["A", "D", "E"], "C": ["A", "F"],
                          "D": ["B"], "E": ["B", "F"], "F": ["C", "E"]},
                "start": "A"},
    },
    {
        "id": "number-of-islands",
        "title": "Number of Islands",
        "category": "graphs",
        "difficulty": "Medium",
        "tags": ["grid", "dfs", "connected components"],
        "link": "https://leetcode.com/problems/number-of-islands/",
        "summary": "Count groups of connected land cells in a grid.",
        "idea": D("""
            Scan the grid. Each time you hit unvisited land, that's a new island — run a **flood fill**
            (DFS) that sinks the whole connected landmass to water so it's counted once. The number of
            flood fills is the number of islands.
        """),
        "why": D("""
            **Why treat a grid as a graph?** Each cell is a node with edges to its 4 neighbors;
            "islands" are just connected components. Sinking visited land (overwriting '1'→'0') doubles
            as the visited set with zero extra memory. This grid-as-graph reframing unlocks a huge
            class of matrix problems.
        """),
        "complexity": {"time": "O(rows·cols)", "space": "O(rows·cols)",
                       "note": "Stack/recursion can hold a whole landmass in the worst case."},
        "files": [
            {"lang": "python", "label": "Python — iterative DFS flood fill", "path": "python/graphs/number_of_island.py"},
        ],
        "viz": {"type": "gridDFS",
                "grid": [["1", "1", "0", "0", "0"],
                         ["1", "1", "0", "0", "0"],
                         ["0", "0", "1", "0", "0"],
                         ["0", "0", "0", "1", "1"]]},
    },
    {
        "id": "number-of-provinces",
        "title": "Number of Provinces",
        "category": "graphs",
        "difficulty": "Medium",
        "tags": ["graph", "dfs", "connected components"],
        "link": "https://leetcode.com/problems/number-of-provinces/",
        "summary": "Count connected groups of cities from an adjacency matrix.",
        "idea": D("""
            The input is an adjacency **matrix**. Start a DFS from each unvisited city, mark everything
            reachable, and increment a province counter once per DFS launch.
        """),
        "why": D("""
            **Why count DFS launches?** Each launch consumes exactly one connected component, so the
            number of times you *start* a traversal equals the number of provinces. Same connected-
            components idea as Number of Islands, but over an explicit adjacency matrix instead of a
            grid — good for seeing the pattern in different input shapes.
        """),
        "complexity": {"time": "O(n²)", "space": "O(n)",
                       "note": "n² because the adjacency matrix has n² entries."},
        "files": [
            {"lang": "python", "label": "Python — iterative DFS", "path": "python/graphs/number_of_provinces.py"},
        ],
    },
    {
        "id": "clone-graph",
        "title": "Clone Graph",
        "category": "graphs",
        "difficulty": "Medium",
        "tags": ["graph", "bfs", "hash map"],
        "link": "https://leetcode.com/problems/clone-graph/",
        "summary": "Deep-copy a connected undirected graph.",
        "idea": D("""
            BFS the original graph while keeping a **map from original value → cloned node**. When you
            meet a neighbor for the first time, create its clone and enqueue it; always wire the current
            clone's neighbor list using the map. The map prevents copying the same node twice.
        """),
        "why": D("""
            **Why a value→clone map?** Cycles mean you'll revisit nodes; the map is both the visited set
            and the lookup that lets you connect clones correctly. Without it you'd recurse forever or
            duplicate nodes. The map-as-memo is the universal trick for cloning or memoizing over
            cyclic structures.
        """),
        "complexity": {"time": "O(V + E)", "space": "O(V)"},
        "files": [
            {"lang": "python", "label": "Python — BFS + clone map", "path": "python/graphs/clone_graph.py"},
        ],
    },
    {
        "id": "cycle-detect-directed",
        "title": "Detect Cycle in a Directed Graph (Kahn's)",
        "category": "graphs",
        "difficulty": "Medium",
        "tags": ["graph", "topological sort", "bfs"],
        "link": "https://leetcode.com/problems/course-schedule/",
        "summary": "Use topological sort to decide if a directed graph has a cycle.",
        "idea": D("""
            Compute each node's **in-degree** (number of incoming edges). Repeatedly remove nodes with
            in-degree 0 (no dependencies), decrementing their neighbors. If you can't process every node
            this way, the leftovers form a cycle.
        """),
        "why": D("""
            **Why Kahn's algorithm?** A directed acyclic graph always has at least one node with no
            incoming edges to start from; a cycle has none, so the process stalls. Counting how many
            nodes get processed gives a clean cycle test and, as a bonus, a valid topological order.
            This is exactly the engine behind Course Schedule I/II.
        """),
        "complexity": {"time": "O(V + E)", "space": "O(V)"},
        "files": [
            {"lang": "python", "label": "Python — Kahn's algorithm", "path": "python/graphs/cycle_detect_directed_graph.py"},
        ],
    },
    {
        "id": "cycle-detect-undirected",
        "title": "Detect Cycle in an Undirected Graph",
        "category": "graphs",
        "difficulty": "Medium",
        "tags": ["graph", "dfs"],
        "link": "https://www.geeksforgeeks.org/detect-cycle-undirected-graph/",
        "summary": "DFS that ignores the edge back to the parent.",
        "idea": D("""
            DFS each component, remembering each node's **parent**. If you reach an already-visited node
            that *isn't* the parent you came from, you've found a cycle.
        """),
        "why": D("""
            **Why track the parent?** In an undirected graph every edge looks like a 2-cycle (A→B and
            B→A). Excluding the parent avoids mistaking that back-edge for a real cycle. This parent-
            aware DFS is the standard way to find cycles (and bridges/articulation points) in undirected
            graphs.
        """),
        "complexity": {"time": "O(V + E)", "space": "O(V)"},
        "files": [
            {"lang": "python", "label": "Python — parent-aware DFS", "path": "python/graphs/cycle_detect_undirected_graph.py"},
        ],
    },
    {
        "id": "course-schedule",
        "title": "Course Schedule I",
        "category": "graphs",
        "difficulty": "Medium",
        "tags": ["graph", "topological sort", "bfs"],
        "link": "https://leetcode.com/problems/course-schedule/",
        "summary": "Can you finish every course given its prerequisites?",
        "idea": D("""
            Model each course as a node and each prerequisite pair `[course, prereq]` as a directed edge
            `prereq → course`. "Can I finish all courses?" then becomes "**is this dependency graph a DAG
            (no cycle)?**" Run Kahn's topological sort: repeatedly take any course whose prerequisites are
            all done (**in-degree 0**), and decrement its dependents. If every course gets processed, there
            is no cycle and you can finish; if some never reach in-degree 0, they form an impossible loop.
        """),
        "why": D("""
            **Why does counting processed courses detect a cycle?** A directed acyclic graph always has at
            least one course with no unmet prerequisites to start from, and removing it exposes more. A
            cycle is a knot of mutually-dependent courses — none ever reaches in-degree 0, so the queue
            drains early. Comparing `completed` against `numCourses` is therefore a clean yes/no cycle test.
            We build the adjacency list in the direction `prereq → course` so that finishing a prerequisite
            "unlocks" the courses that depend on it.
        """),
        "complexity": {
            "time": "O(V + E)",
            "space": "O(V + E)",
            "note": "`V` = courses, `E` = prerequisite pairs. One pass builds the graph; one BFS drains it. "
                    "Edge case: with **no** prerequisites every course is independent and trivially finishable.",
        },
        "viz": {"type": "kahn", "vertices": 4, "adj": [[1, 2], [3], [3], []]},
        "files": [
            {"lang": "python", "label": "Python — Kahn's (cycle test)", "path": "python/graphs/course_schedule_I.py"},
        ],
    },
    {
        "id": "course-schedule-ii",
        "title": "Course Schedule II",
        "category": "graphs",
        "difficulty": "Medium",
        "tags": ["graph", "topological sort", "bfs", "ordering"],
        "link": "https://leetcode.com/problems/course-schedule-ii/",
        "summary": "Return a valid order to take all courses (or empty if impossible).",
        "idea": D("""
            Same setup as Course Schedule I — courses are nodes, prerequisite `[course, prereq]` is an edge
            `prereq → course` — but now we **record the order** in which courses become available. Each time
            a course's in-degree hits 0 we append it to the result. That append order *is* a valid
            topological ordering. If a cycle blocks some courses, fewer than `numCourses` get recorded, so
            we return an empty list.
        """),
        "why": D("""
            **Why is the pop order a valid schedule?** A course is only enqueued once every one of its
            prerequisites has already been processed, so it can never appear before something it depends on.
            That's the definition of a topological order. This is the *same engine* as Course Schedule I —
            the only change is that we emit the order instead of a boolean. Recognising that I and II are one
            algorithm with a different return value is the real takeaway.
        """),
        "complexity": {
            "time": "O(V + E)",
            "space": "O(V + E)",
            "note": "Identical cost to Course Schedule I. The length check (`order` size vs `numCourses`) "
                    "doubles as the cycle guard — a cycle leaves the order short, so we return `[]`.",
        },
        "viz": {"type": "kahn", "vertices": 4, "adj": [[1, 2], [3], [3], []]},
        "files": [
            {"lang": "python", "label": "Python — Kahn's (topological order)", "path": "python/graphs/course_schedule_II.py"},
        ],
    },

    # ===================== GREEDY & MISC =====================
    {
        "id": "max-balloons",
        "title": "Maximum Number of Balloons",
        "category": "misc",
        "difficulty": "Easy",
        "tags": ["hash map", "counting"],
        "link": "https://leetcode.com/problems/maximum-number-of-balloons/",
        "summary": "How many times can you spell 'balloon' from the given letters?",
        "idea": D("""
            Count the letters you have. The word "balloon" needs `l` and `o` twice each, so the number
            of full words is limited by the **scarcest** required letter: `min(b, a, l//2, o//2, n)`.
        """),
        "why": D("""
            **Why a frequency count + min?** Each copy of the word consumes a fixed recipe of letters;
            the bottleneck letter caps how many you can build. Counting is O(n) and the `//2` neatly
            handles the doubled letters. A tidy example of turning a word problem into arithmetic on
            counts.
        """),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "files": [
            {"lang": "python", "label": "Python — counter + min", "path": "python/maps/max_num_balloons.py"},
        ],
    },
    {
        "id": "buckets-alternating",
        "title": "Minimum Moves to Alternate Buckets",
        "category": "misc",
        "difficulty": "Medium",
        "tags": ["greedy", "prefix sum", "sliding window"],
        "link": "#",
        "summary": "Fewest ball moves to space balls exactly two buckets apart.",
        "idea": D("""
            Balls must land on positions of a single parity (all even or all odd indices), spaced 2
            apart. For each parity, slide a window over the candidate positions and count how many balls
            are *already* correctly placed; the answer is total balls minus the best overlap.
        """),
        "why": D("""
            **Why parity + prefix sums?** A valid arrangement is fully determined by which parity class
            and which contiguous block of slots you target. Prefix sums make "how many balls already sit
            in this block?" an O(1) query, so a sliding window finds the placement needing the fewest
            moves. The two files contrast a quick heuristic with this rigorous counting solution.
        """),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "files": [
            {"lang": "java", "label": "Java — prefix-sum window (correct)", "path": "java/src/com/dsalgo/misc/BucketsSolution2.java"},
            {"lang": "java", "label": "Java — first attempt (heuristic)", "path": "java/src/com/dsalgo/misc/BucketsProblem.java"},
        ],
    },
    {
        "id": "wooden-sticks",
        "title": "Largest Square from Two Sticks",
        "category": "misc",
        "difficulty": "Easy",
        "tags": ["greedy", "math"],
        "link": "#",
        "summary": "Largest square side cuttable as 4 equal pieces from two sticks.",
        "idea": D("""
            A square needs 4 equal sides. For a candidate side length `L`, the two sticks yield
            `A//L + B//L` pieces. Try lengths from the largest downward and return the first `L` that
            produces at least 4 pieces.
        """),
        "why": D("""
            **Why scan from large to small (and the O(1) alternative)?** The first feasible length you
            meet going downward is the maximum, so you can stop immediately. The included note observes
            the answer is bounded by `(A+B)//4`, which lets you jump straight to the candidate instead of
            scanning — a nice "prove a bound to skip work" optimization.
        """),
        "complexity": {"time": "O(max(A,B))", "space": "O(1)",
                       "note": "O(1) if you start from the (A+B)//4 bound."},
        "files": [
            {"lang": "java", "label": "Java — greedy scan", "path": "java/src/com/dsalgo/misc/WoodenSticksProblem.java"},
        ],
    },
]


# ---------------------------------------------------------------------------
# Extra visualization bindings for complex problems (merged in build()).
# ---------------------------------------------------------------------------
EXTRA_VIZ = {
    "house-robber": {"type": "dpRolling", "nums": [2, 7, 9, 3, 1]},
    "max-depth": {"type": "treeDFS", "variant": "depth", "tree": [3, 9, 20, None, None, 15, 7]},
    "balanced-tree": {"type": "treeDFS", "variant": "balanced", "tree": [1, 2, 2, 3, 3, None, None, 4, 4]},
    "max-path-sum": {"type": "treeDFS", "variant": "maxpath", "tree": [-10, 9, 20, None, None, 15, 7]},
    "lowest-common-ancestor": {"type": "treeDFS", "variant": "lca",
                               "tree": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "p": 5, "q": 1},
    "cycle-detect-directed": {"type": "kahn", "vertices": 6, "adj": [[1, 2], [3], [3], [4, 5], [], []]},
    "number-of-provinces": {"type": "matrixComponents", "matrix": [[1, 1, 0], [1, 1, 0], [0, 0, 1]]},
    "clone-graph": {"type": "cloneBFS", "graph": {"1": [2, 4], "2": [1, 3], "3": [2, 4], "4": [1, 3]}, "start": 1},
    "cycle-detect-undirected": {"type": "undirectedCycle", "graph": {"0": [1, 2], "1": [0, 2], "2": [0, 1]}, "start": 0},
    "search-rotated-array": {"type": "rotatedSearch", "nums": [4, 5, 6, 7, 0, 1, 2], "target": 0},
    "search-rotated-array-ii": {"type": "rotatedSearch", "nums": [1, 3, 5, 7, 8, 0, 1, 1], "target": 8},
}

# ---------------------------------------------------------------------------
# "Deep dive" walkthroughs — detailed, worked-example explanations for the
# harder problems (rendered as an extra panel on the site).
# ---------------------------------------------------------------------------
DEEP_DIVES = {
    "graph-traversal": D("""
        **Walk through BFS on this graph** (`A–B`, `A–C`, `B–D`, `B–E`, `C–F`, `E–F`), starting at `A`:

        - Mark `A` visited, queue = `[A]`.
        - Pop `A`, record it, enqueue its unvisited neighbours `B, C` → queue `[B, C]`.
        - Pop `B`, enqueue `D, E` → queue `[C, D, E]`.
        - Pop `C`, enqueue `F` → queue `[D, E, F]`.
        - Pop `D, E, F` (their neighbours are all visited) → done.

        Visit order `A, B, C, D, E, F` — nodes come out in **non-decreasing distance** from the source,
        which is exactly why BFS finds shortest paths in unweighted graphs.

        **Swap the queue for a stack** and you get DFS: after popping `A` you'd push `B, C`, then
        immediately dive from `C` (LIFO) before finishing `B`'s side. Same code, different container,
        completely different traversal shape.

        **Two pitfalls to remember:** (1) mark a node visited *when you enqueue/push it*, not when you
        pop it — otherwise it can be added twice; (2) graphs have cycles, so the visited set is not
        optional like it is for trees.
    """),
    "number-of-islands": D("""
        **Why this is secretly a graph problem.** Treat every cell as a node connected to its 4
        orthogonal neighbours. An "island" is then just a **connected component** of land cells.

        **The flood-fill trick.** Scan row by row. The first `'1'` you touch belongs to a brand-new
        island, so increment the counter and then *sink the entire landmass* with DFS/BFS: starting
        from that cell, keep visiting neighbouring `'1'`s and flipping them to `'0'`. After the fill,
        that whole island is gone, so it can never be counted again.

        **Worked example** on the 4×4 grid in the visualization: the top-left 2×2 block of land is
        discovered first → island #1, sunk entirely. Scanning continues, finds the lone `1` in the
        middle → island #2. Then the bottom-right pair → island #3. Answer: **3**.

        **Why overwrite the grid instead of a visited set?** Flipping `'1'→'0'` *is* the visited
        marker — it costs zero extra memory. If you're not allowed to mutate the input, use a separate
        `visited` matrix; the logic is identical.

        Complexity is O(rows·cols): every cell is visited a constant number of times.
    """),
    "number-of-provinces": D("""
        **Same idea as Number of Islands, different input shape.** Here the graph is given as an
        `n × n` adjacency *matrix* (`isConnected[i][j] == 1` means cities `i` and `j` are directly
        linked). A "province" is a connected component of cities.

        **The counting insight:** loop over all cities; whenever you find one that hasn't been
        visited, that city must belong to a province you haven't seen yet — so increment the counter
        and DFS to mark every city reachable from it. **The number of times you *launch* a DFS equals
        the number of provinces.**

        **Worked example** `[[1,1,0],[1,1,0],[0,0,1]]`: start at city 0 (unvisited) → province #1; DFS
        marks 0 and 1 (they're connected). City 1 is now visited, skip. City 2 is unvisited →
        province #2; DFS marks just 2. Answer: **2**.

        Because we may scan the whole matrix row for each city, the cost is O(n²) — unavoidable when
        the graph is stored as a dense matrix.
    """),
    "clone-graph": D("""
        **The core challenge isn't copying values — it's copying *structure* without looping forever.**
        The graph has cycles, so a naive recursive copy would revisit nodes endlessly and create
        duplicate clones.

        **The fix: a `value → clone` hash map** that doubles as the visited set. BFS the original:

        - Create `clone(start)` up front and put it in the map.
        - Pop a node, look up its clone, then for each neighbour: if it isn't in the map yet, create
          its clone and enqueue the *original*; either way, append the neighbour's clone to the current
          clone's neighbour list.

        **Worked example** on the 4-cycle `1–2–3–4–1`: visiting `1` creates clones of `2` and `4` and
        links `clone(1)→[clone(2), clone(4)]`. Later, when we process `2`, its neighbour `1` is already
        in the map, so we reuse `clone(1)` instead of making a second copy — that reuse is what keeps
        the cycle intact and the algorithm terminating.

        The map is the whole trick: it's simultaneously "have I cloned this?" and "where is the clone?"
        — the universal pattern for copying or memoizing over cyclic structures. O(V+E) time, O(V) space.
    """),
    "cycle-detect-directed": D("""
        **Reframe "is there a cycle?" as "can I schedule all the tasks?"** (this is literally Course
        Schedule). Kahn's algorithm builds a topological order, and a directed graph has a valid
        topological order **iff** it has no cycle.

        **How it runs:**

        1. Compute every node's *in-degree* (number of prerequisites).
        2. Put all in-degree-0 nodes (no prerequisites) in a queue.
        3. Repeatedly pop a node, "complete" it, and decrement each neighbour's in-degree; when a
           neighbour hits 0, enqueue it.
        4. Count how many nodes you processed.

        **The verdict:** if you processed *every* node, you found a full ordering → **no cycle**. If
        some nodes were never reachable with in-degree 0, they're mutually waiting on each other →
        **cycle**.

        **Why it works:** a DAG always has at least one source (in-degree 0) to start from, and removing
        it keeps the rest a DAG. A cycle has no such entry point, so the process stalls with nodes left
        over. Bonus: the order you pop nodes in *is* a valid topological sort. O(V+E).
    """),
    "cycle-detect-undirected": D("""
        **The twist that trips people up:** in an undirected graph, every single edge `u–v` looks like
        a tiny cycle, because from `v` you can immediately walk back to `u`. If you naively flag "I
        reached an already-visited node," you'll report a cycle on a plain tree.

        **The fix: track where you came from (the parent).** During DFS, when you look at a neighbour:

        - If it's unvisited → visit it, recording the current node as its parent.
        - If it's visited **and it's not your parent** → you've found a genuine *second* way to reach
          it → a real cycle.

        **Worked example:** on the triangle `0–1–2–0`, DFS goes `0 → 1 → 2`. From `2`, neighbour `0` is
        already visited and `0` is *not* `2`'s parent (that's `1`) → cycle. On the path `0–1–2`, every
        already-visited neighbour you meet *is* your parent, so no false alarm.

        This parent-aware DFS is also the backbone of finding bridges and articulation points. O(V+E).
    """),
    "tree-traversals": D("""
        **The single mental model:** every DFS order runs the same three actions — *visit node*,
        *go left*, *go right* — and they differ **only in where "visit node" sits**:

        - **Pre-order** = visit, left, right → roots come out before their subtrees (great for copying
          a tree or serializing it).
        - **In-order** = left, visit, right → on a **binary search tree** this prints values in
          **sorted** order.
        - **Post-order** = left, right, visit → children finish before the parent (great for deleting a
          tree, or any "combine results from children" computation like height or max-path-sum).

        **Worked example** on `1(2(4,5),3(_,6))` in-order: dive to `4`, visit `4`, back to `2`, visit
        `2`, visit `5`, back to `1`, visit `1`, into `3`, visit `3`, visit `6` → `4 2 5 1 3 6`.

        **Recursive vs. iterative:** recursion leans on the call stack to remember "where to resume."
        The iterative in-order version makes that stack explicit — push left children all the way down,
        pop to visit, then turn right — which is what an interviewer wants when they say "no recursion."
    """),
    "level-order": D("""
        **Depth-first won't group nodes by level — breadth-first will.** Use a queue (FIFO) so nodes
        come out in the order they were discovered, which is level by level.

        **The "level size snapshot" trick** is the key detail. At the top of each iteration, record
        `size = len(queue)` — that's exactly how many nodes are on the current level. Pop precisely
        `size` nodes, collect their values into one list, and enqueue their children (which become the
        next level). Without that snapshot you'd get one flat list instead of a list-per-level.

        **Worked example** on `[3, 9, 20, null, null, 15, 7]`:

        - queue `[3]`, size 1 → level `[3]`, enqueue `9, 20`.
        - queue `[9, 20]`, size 2 → level `[9, 20]`, enqueue `15, 7`.
        - queue `[15, 7]`, size 2 → level `[15, 7]`, no children.

        Result `[[3], [9, 20], [15, 7]]`. The same BFS skeleton solves right-side-view, zigzag order,
        and "max value per level." O(n) time, O(n) space for the queue.
    """),
    "max-depth": D("""
        **A textbook self-similar definition:** the depth of a tree is `1 + max(depth(left),
        depth(right))`, and an empty subtree has depth `0`. The recursion is almost a transcription of
        that sentence.

        **Worked example** on `[3, 9, 20, null, null, 15, 7]`: `9` is a leaf → depth 1. `15` and `7`
        are leaves → depth 1 each, so `20` → `1 + max(1,1) = 2`. Finally the root `3` →
        `1 + max(depth(9)=1, depth(20)=2) = 3`.

        **Why post-order (children before parent)?** A node can't know its own height until both
        children report theirs, so values bubble *up* from the leaves. The recursion visits each node
        once → O(n) time; the call stack goes as deep as the tree → O(h) space (O(n) for a degenerate,
        list-shaped tree). This same bottom-up shape underlies *balanced tree*, *diameter*, and
        *max path sum*.
    """),
    "balanced-tree": D("""
        **The naive solution is accidentally O(n²).** "For every node, compute the height of its left
        and right subtree and compare" re-walks the same subtrees over and over.

        **The optimization: compute height and check balance in one pass, using `-1` as a failure
        signal.** The recursion returns the subtree's height normally, but returns `-1` the moment it
        discovers *any* imbalance below it. As soon as a child returns `-1`, the parent immediately
        returns `-1` too — short-circuiting the rest of the work.

        **Worked example** on `[1, 2, 2, 3, 3, null, null, 4, 4]`: the left spine `1→2→3→4` is much
        deeper than the right side. When DFS unwinds, some node sees a left height that exceeds the
        right by more than 1, returns `-1`, and that `-1` propagates straight to the root → **not
        balanced**.

        Folding the check into the height computation turns it into a single O(n) traversal. The
        "return a sentinel to abort early" pattern shows up constantly in tree problems.
    """),
    "max-path-sum": D("""
        **The defining subtlety:** a node participates in the answer in two *different* ways, and
        conflating them is the classic bug.

        1. A path can **bend** at a node, using *both* children: `node.val + leftGain + rightGain`.
           This is a candidate for the global maximum — but it can't be extended further upward (a
           parent can't pass through a "V").
        2. A path can **continue up** through a node to its parent, using only *one* child:
           `node.val + max(leftGain, rightGain)`. This is what we *return* to the caller.

        **Clamp negative gains to 0** — `max(gain(child), 0)` — because a branch with a negative total
        is better left out entirely.

        **Worked example** on `[-10, 9, 20, null, null, 15, 7]`: at `20`, left/right gains are 15 and 7,
        so the bend `15 + 20 + 7 = 42` updates the global best, and `20` returns `20 + max(15,7) = 27`
        upward. At the root `-10`, using its branch would only shrink the sum, so the best path never
        passes through it. Answer: **42**.

        Keep "answer recorded at this node" (the global max) strictly separate from "value returned to
        the parent." O(n) time, O(h) space.
    """),
    "lowest-common-ancestor": D("""
        **Why post-order is mandatory:** you can't decide whether a node is the common ancestor until
        you know what each of its subtrees contains. So process children first, and let every call
        report back a simple fact: "did I find `p` or `q` somewhere below me?"

        **The three cases at each node:**

        - The node *is* `p` or `q` → return it (a node can be its own ancestor).
        - Both the left and right recursion return non-null → `p` and `q` were found on *different
          sides*, so **this node is the LCA**.
        - Only one side returns non-null → bubble that result upward unchanged.

        **Worked example** on the tree with `p = 5`, `q = 1`: searching from the root `3`, the left
        recursion finds `5` and the right recursion finds `1`. Root `3` sees a hit on both sides →
        it's the LCA. If instead `p = 5`, `q = 4` (where `4` lives under `5`), the call at `5` returns
        itself before recursing deeper, so `5` is the answer.

        One clean O(n) traversal, O(h) stack. The "let recursion return a found-flag" trick generalizes
        to many tree-search problems.
    """),
    "house-robber": D("""
        **Set up the recurrence by asking one yes/no question at each house:** do I rob it?

        - **Skip it** → my best total is whatever I had through the previous house: `dp[i-1]`.
        - **Rob it** → I take its money but the adjacency rule forbids the previous house, so I add to
          the best total through house `i-2`: `nums[i] + dp[i-2]`.

        So `dp[i] = max(dp[i-1], nums[i] + dp[i-2])`.

        **Worked example** on `[2, 7, 9, 3, 1]`:

        - house 0: best = 2
        - house 1: max(2, 7) = 7
        - house 2: max(7, 2+9=11) = 11
        - house 3: max(11, 7+3=10) = 11
        - house 4: max(11, 11+1=12) = **12** (rob houses 0, 2, 4)

        **The space optimization:** the formula only ever looks back one and two steps, so the full
        `dp` array is unnecessary — keep two rolling variables `prev1` (`dp[i-1]`) and `prev2`
        (`dp[i-2]`). That drops memory from O(n) to **O(1)** while staying O(n) time. Recognizing
        "my recurrence has a bounded look-back" is the trigger for this very common optimization.
    """),
    "lcs": D("""
        **Define the subproblem precisely:** `dp[i][j]` = length of the LCS of the first `i` characters
        of `text1` and the first `j` characters of `text2`. The full answer is `dp[m][n]`.

        **The recurrence, by cases on the last characters:**

        - If `text1[i-1] == text2[j-1]`, that shared character extends the best LCS of the smaller
          prefixes: `dp[i][j] = 1 + dp[i-1][j-1]` (the diagonal).
        - Otherwise we must drop the last character of one string and take the better result:
          `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` (up vs. left).

        Row/column `0` represents an empty string, so it's all zeros — that's why the table is
        `(m+1) × (n+1)`.

        **Worked example** `"abcde"` vs `"ace"`: matches on `a`, `c`, `e` accumulate down the diagonal,
        giving `dp[5][3] = 3` → the LCS is `"ace"`. Watch the visualization fill the grid cell by cell
        and you'll see the diagonal "1+" jumps exactly at matching characters.

        O(m·n) time and space; the space drops to O(min(m,n)) since each row only needs the previous
        one. This grid recurrence is the template for edit distance and sequence alignment.
    """),
    "longest-common-substring": D("""
        **Almost LCS — but with one decisive change.** A *substring* must be contiguous, whereas a
        *subsequence* may skip characters. That single constraint rewrites the mismatch case:

        - Match: `dp[i][j] = 1 + dp[i-1][j-1]` (extend the current contiguous run, same as LCS).
        - **Mismatch: `dp[i][j] = 0`** — the run is broken, so it resets. (LCS instead carries forward
          `max(up, left)`, because a subsequence can tolerate a gap.)

        Because a reset can happen anywhere, the answer is the **maximum value in the whole table**, not
        the bottom-right corner.

        **Worked example** `"ABABC"` vs `"BABCA"`: the diagonal run for `B→A→B→C` climbs `1, 2, 3, 4`,
        so the longest common substring is `"BABC"`, length **4**. Toggle the visualization between the
        two modes to see "carry forward the max" (subsequence) versus "reset to 0" (substring) — it's
        the clearest way to internalize the difference.

        O(m·n) time and space.
    """),
    "search-rotated-array": D("""
        **Binary search seems impossible — the array isn't fully sorted.** But here's the saving grace:
        no matter where you split a rotated sorted array, **at least one half is still sorted.**

        **At each midpoint:**

        1. Compare `nums[low]` with `nums[mid]`. If `nums[low] <= nums[mid]`, the **left** half is the
           sorted one; otherwise the **right** half is.
        2. Check whether the target lies *within the sorted half's value range*. If yes, search that
           half; if no, search the other half.

        That single decision restores the "throw away half the candidates" guarantee that makes binary
        search O(log n).

        **Worked example** `[4,5,6,7,0,1,2]`, target `0`: `mid` is `7` (index 3). Left half `[4..7]` is
        sorted, but `0` isn't in `[4,7]`, so go right → `[0,1,2]`. Now `mid` is `1`; `0 < 1`, search
        left → find `0` at index 4.

        **The duplicates wrinkle (part II):** when `nums[low] == nums[mid] == nums[high]` you can't tell
        which half is sorted, so you shrink both ends by one (`low++, high--`). That fallback can fire
        every step on input like `[1,1,1,1]`, degrading the worst case to O(n).
    """),
    "search-rotated-array-ii": D("""
        Everything from *Search in Rotated Sorted Array* applies — find the sorted half, decide which
        way to go — but **duplicates introduce genuine ambiguity.**

        **The problem case:** when `nums[low] == nums[mid] == nums[high]`, you literally cannot tell
        which side is the sorted one (e.g. `[1,1,1,0,1]` vs `[1,0,1,1,1]` look identical at the ends).
        The only safe move is to **shrink the window by one on both sides** (`low++, high--`) and retry.

        **Why the complexity changes:** that fallback discards just two elements instead of half, so on
        a pathological all-duplicates array it can run on every step → **O(n) worst case**, versus the
        clean **O(log n)** when values are distinct. Average case stays logarithmic.

        The lesson is bigger than this problem: duplicates can quietly destroy the guarantees an
        algorithm relies on, and recognizing that ambiguity is exactly what an interviewer is probing.
    """),
}


# ---------------------------------------------------------------------------
# Curated problem statements for files that have no usable docstring/javadoc.
# ---------------------------------------------------------------------------
STATEMENTS = {
    "group-anagrams": D("""
        Given an array of strings strs, group the anagrams together. You can return the answer in
        any order.

        An anagram is a word or phrase formed by rearranging the letters of another, using all the
        original letters exactly once.

        Example 1:

        Input: strs = ["eat","tea","tan","ate","nat","bat"]
        Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

        Example 2:

        Input: strs = [""]
        Output: [[""]]
    """),
    "longest-common-substring": D("""
        Given two strings text1 and text2, return the length of their longest common substring.

        A substring is a contiguous sequence of characters within a string. Unlike a subsequence, it
        cannot skip characters.

        Example 1:

        Input: text1 = "ABABC", text2 = "BABCA"
        Output: 4
        Explanation: The longest common substring is "BABC", with length 4.

        Example 2:

        Input: text1 = "abcde", text2 = "abfce"
        Output: 2
        Explanation: The longest common substring is "ab".
    """),
    "graph-traversal": D("""
        Given a graph represented as an adjacency list, visit every node reachable from a given start
        node.

        Breadth-First Search (BFS) explores the graph level by level using a queue. Depth-First Search
        (DFS) goes as deep as possible along each branch before backtracking, using a stack (or
        recursion). Both use a visited set so cycles don't cause infinite loops.

        Example:

        Input: graph = {A:[B,C], B:[A,D,E], C:[A,F], D:[B], E:[B,F], F:[C,E]}, start = A
        BFS order: A, B, C, D, E, F
        DFS order: A, C, F, E, B, D   (one valid ordering)
    """),
    "clone-graph": D("""
        Given a reference to a node in a connected undirected graph, return a deep copy (clone) of the
        graph.

        Each node contains an integer value and a list of its neighbors. The clone must be entirely
        independent of the original — same structure and values, but all-new node objects.

        Example 1:

        Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
        Output: [[2,4],[1,3],[2,4],[1,3]]
        Explanation: 4 nodes form the cycle 1-2-3-4-1; the output is an identical, independent copy.

        Example 2:

        Input: adjList = []
        Output: []
    """),
    "cycle-detect-directed": D("""
        Given a directed graph with V vertices and an adjacency list adj, determine whether the graph
        contains a cycle.

        Equivalently (Course Schedule): given dependencies between tasks, decide whether all tasks can
        be finished — possible if and only if the dependency graph has no cycle.

        Example 1:

        Input: V = 3, adj = [[1], [2], [0]]
        Output: true   (0 -> 1 -> 2 -> 0 is a cycle)

        Example 2:

        Input: V = 3, adj = [[1, 2], [2], []]
        Output: false  (a DAG, no cycle)
    """),
    "binary-search": D("""
        Given a sorted (ascending) array of integers nums and an integer target, return whether target
        exists in nums. You must write an algorithm with O(log n) runtime complexity.

        Example 1:

        Input: nums = [1,2,3,4,5,7,9,10], target = 9
        Output: true

        Example 2:

        Input: nums = [1,2,3,4,5,7,9,10], target = 6
        Output: false
    """),
    "search-bst": D("""
        You are given the root of a binary search tree (BST) and an integer val. Find the node whose
        value equals val and return the subtree rooted at that node. If the node does not exist, return
        null.

        Example 1:

        Input: root = [4,2,7,1,3], val = 2
        Output: [2,1,3]

        Example 2:

        Input: root = [4,2,7,1,3], val = 5
        Output: []
    """),
    "invert-tree": D("""
        Given the root of a binary tree, invert the tree (mirror it by swapping every node's left and
        right children) and return its root.

        Example 1:

        Input: root = [4,2,7,1,3,6,9]
        Output: [4,7,2,9,6,3,1]

        Example 2:

        Input: root = [2,1,3]
        Output: [2,3,1]
    """),
}

# ---------------------------------------------------------------------------
# Concept GUIDES — long-form, visual "how to actually solve these" walkthroughs.
# Each guide is a list of sections; a section may carry prose (`body`, rendered
# with the richer guide markdown) and/or an embedded, playable visualization
# (`viz`, reusing the same visualizers the problem pages use).
# ---------------------------------------------------------------------------
GUIDES = [
    {
        "id": "trees",
        "icon": "🌳",
        "title": "How to Solve Tree Problems",
        "shortTitle": "Trees",
        "blurb": "From 'I freeze when I see a tree problem' to interview-ready. Master the 3 building "
                 "blocks and 5 recurring patterns, then go deep on traversals, BSTs, LCA, construction, "
                 "tries, and segment trees — every concept made mechanical, intuitive, and visual.",
        "sections": [
            {
                "title": "The mental model that fixes everything",
                "body": D("""
                    Every tree problem is **one of two questions in disguise**:

                    1. *"Visit every node and collect or compute something."* — this is a **traversal**.
                    2. *"At each node, combine the answers from my children into my own answer."* — this is **recursion on the tree** (a DFS that returns a value).

                    That is the whole game. Tree problems *feel* hard only because the recursion hides the work. So we are going to make the recursion **mechanical**: a base case plus a combine step, every single time.

                    > When you are stuck, you are stuck on exactly one of two things: *"What is the answer for an empty tree?"* (the base case) or *"How do I combine my children's answers with my own value?"* (the combine step). Ask both out loud.
                """),
            },
            {
                "title": "Building block 1 — what a tree node really is",
                "body": D("""
                    A binary tree is just objects pointing at up to two other objects.

                    ```python
                    class TreeNode:
                        def __init__(self, val=0, left=None, right=None):
                            self.val = val
                            self.left = left      # another TreeNode, or None
                            self.right = right    # another TreeNode, or None
                    ```

                    Facts you must keep in your head:

                    - A node whose `left` and `right` are both `None` is a **leaf**.
                    - `None` is a legal value meaning *"no child here"*. **Half of all tree bugs are forgetting a child can be `None`.**
                    - The whole tree is one variable, `root`. If `root is None`, the tree is empty — your most common base case.
                """),
            },
            {
                "title": "Tree vocabulary — the words interviewers won't define",
                "body": D("""
                    A tree is formally *a connected graph with no cycles*. On `N` nodes it has exactly `N-1` edges, and there's exactly **one path between any two nodes**. One node is the **root**, which gives every other node a single parent and a sense of "above / below" that plain graphs lack.

                    | Term | Meaning |
                    |------|---------|
                    | **Root** | the single top node (no parent) |
                    | **Leaf** | a node with no children (`left` and `right` both `None`) |
                    | **Parent / Child** | A points down to B ⇒ A is B's parent, B is A's child |
                    | **Ancestor / Descendant** | every node on the root→X path is an ancestor of X |
                    | **Depth of a node** | edges from the **root** down to it (root = depth 0) |
                    | **Height of a node** | edges on the longest path **down** to a leaf (leaf = height 0) |
                    | **Subtree at X** | X plus all of its descendants |
                    | **Balanced** | every node's two subtree heights differ by ≤ 1 → operations stay `O(log n)` |
                    | **BST** | for every node: all left values &lt; node &lt; all right values |

                    > **Depth vs height** trips people up constantly. Depth counts *down from the root*; height counts *up from the leaves*. Read it as a picture:

                    ```text
                    depth 0   →          (1)            height 2   ← root
                    depth 1   →       (2)     (3)        height 1 / 0
                    depth 2   →    (4)   (5)             height 0   ← leaves
                    ```
                """),
            },
            {
                "title": "Tree representations — three ways to store one",
                "body": D("""
                    **1. Linked nodes (the default).** The `TreeNode` above — objects with `left`/`right` pointers. This is what 95% of interview problems hand you.

                    **2. Array / heap layout.** A *complete* tree can live in a flat array with no pointers: the node at index `i` has children at `2i+1` and `2i+2`, and parent at `(i-1)//2`. This is exactly how a binary heap (`heapq`) works — cache-friendly, but only valid for complete trees.

                    ```python
                    left_child  = 2 * i + 1
                    right_child = 2 * i + 2
                    parent      = (i - 1) // 2
                    ```

                    **3. Parent map.** Some problems (e.g. *all nodes at distance K*) need to walk **upward**. Rather than mutating nodes, build a `child → parent` dictionary in one pass, then treat the tree as an undirected graph.

                    ```python
                    def build_parent_map(root):
                        parent = {root: None}
                        def dfs(node):
                            for child in (node.left, node.right):
                                if child:
                                    parent[child] = node
                                    dfs(child)
                        if root: dfs(root)
                        return parent
                    ```

                    > Choosing the representation *is* part of the solution. "Walk upward" → parent map. "Complete tree / heap" → array indices. Everything else → linked nodes.
                """),
            },
            {
                "title": "Building block 2 — recursion = base case + combine",
                "body": D("""
                    The single biggest unlock is this sentence:

                    > **Assume the recursive call already works on a smaller subtree. Now just combine.**

                    This is the *recursive leap of faith*. You do **not** trace 10 levels deep in your head. You write the function as if it already works on the children, and trust it. Every recursive tree function has exactly two parts:

                    ```python
                    def solve(node):
                        # 1. BASE CASE — the smallest input. Almost always "empty tree".
                        if node is None:
                            return <the answer for an empty tree>

                        # 2. RECURSIVE CASE — trust the child calls, then combine.
                        left  = solve(node.left)     # trust it
                        right = solve(node.right)    # trust it
                        return <combine left, right, and node.val>
                    ```

                    Fill in the two blanks and you have solved the problem.
                """),
            },
            {
                "title": "DFS vs BFS — and the four traversals",
                "body": D("""
                    There are two orders to visit nodes, and you must know both cold.

                    | Traversal | Order | Use it when… |
                    |-----------|-------|--------------|
                    | **Pre-order** | Root, Left, Right | you process a node *before* its subtree (copy/clone, serialize) |
                    | **In-order** | Left, Root, Right | working with a **Binary Search Tree** — in-order yields *sorted* values |
                    | **Post-order** | Left, Right, Root | you need children's results *before* the parent (height, "is my subtree OK?") — **the most common interview shape** |
                    | **Level-order (BFS)** | level by level | anything about *levels*, *depth*, or *shortest distance* |

                    The only thing that changes between the three DFS traversals is **where you process the node** relative to the two recursive calls. Play the visualization below and switch the mode to *watch the same tree print in a different order*.

                    ```python
                    def pre_order(node):      # process BEFORE children
                        if not node: return
                        process(node)
                        pre_order(node.left); pre_order(node.right)

                    def in_order(node):       # process BETWEEN children
                        if not node: return
                        in_order(node.left); process(node); in_order(node.right)

                    def post_order(node):     # process AFTER children
                        if not node: return
                        post_order(node.left); post_order(node.right); process(node)
                    ```

                    > **Memory hook:** Pre / In / Post tells you where **Root** sits — first, middle, or last.
                """),
                "viz": {"type": "treeTraversal", "tree": [1, 2, 3, 4, 5, None, 6]},
                "vizTitle": "DFS traversals — switch In / Pre / Post and press Play",
                "caption": "Notice the node is *recorded* (turns green) at a different moment in each mode, but the path the DFS walks is identical.",
            },
            {
                "title": "Level-order (BFS) — the queue template",
                "body": D("""
                    For anything *per level*, use a queue. The trick is the `level_size` line: freeze the count so you process exactly one level per outer loop.

                    ```python
                    from collections import deque

                    def level_order(root):
                        if not root: return []
                        result, queue = [], deque([root])
                        while queue:
                            level_size = len(queue)        # nodes in THIS level
                            level = []
                            for _ in range(level_size):
                                node = queue.popleft()
                                level.append(node.val)
                                if node.left:  queue.append(node.left)
                                if node.right: queue.append(node.right)
                            result.append(level)
                        return result
                    ```

                    *Right side view* = last node of each level. *Average per level* = mean of each level. *Zigzag* = reverse alternate levels. All the same template, one line changed.
                """),
                "viz": {"type": "treeLevelOrder", "tree": [3, 9, 20, None, None, 15, 7]},
                "vizTitle": "BFS — draining the queue one level at a time",
                "caption": "Each outer loop drains every node currently in the queue (one level), then enqueues their children for the next round.",
            },
            {
                "title": "Iterative traversals — when recursion is banned (or too deep)",
                "body": D("""
                    Interviewers sometimes ask for an *iterative* traversal — either to test depth of understanding, or because Python's default recursion limit (~1000) overflows on a skewed tree. The recursion's call stack just becomes an **explicit stack**.

                    **Iterative pre-order** is easiest because you process a node the moment you see it. Push *right before left* so left pops first:

                    ```python
                    def preorder_iterative(root):
                        if not root: return []
                        out, stack = [], [root]
                        while stack:
                            node = stack.pop()
                            out.append(node.val)
                            if node.right: stack.append(node.right)   # right first…
                            if node.left:  stack.append(node.left)    # …so left is processed next
                        return out
                    ```

                    **Iterative in-order** dives left while pushing, then pops to process, then turns right:

                    ```python
                    def inorder_iterative(root):
                        out, stack, node = [], [], root
                        while node or stack:
                            while node:                 # go as far left as possible
                                stack.append(node); node = node.left
                            node = stack.pop()          # leftmost unvisited
                            out.append(node.val)
                            node = node.right           # then explore the right subtree
                        return out
                    ```

                    > **Post-order trick:** do a modified pre-order in order *root → right → left*, then **reverse** the result — that gives *left → right → root*, which is post-order. Far easier than a true two-pass post-order stack.
                """),
            },
            {
                "title": "Pattern 1 — combine children's answers (the workhorse)",
                "body": D("""
                    **Signs:** *maximum depth, height, count nodes, sum of…, diameter, is it balanced.* You return information **up** the tree, from children to parent — a post-order DFS.

                    ```python
                    def max_depth(node):
                        if not node:
                            return 0                          # empty tree has depth 0
                        return 1 + max(max_depth(node.left), max_depth(node.right))
                    ```

                    Read it as: *"my depth = 1 (for myself) + the deeper of my two children."* That is the combine step; the base case is *"empty = 0."* Watch each node compute its height **only after both children report back** (`h=…` badges appear bottom-up).
                """),
                "viz": {"type": "treeDFS", "variant": "depth", "tree": [3, 9, 20, None, None, 15, 7]},
                "vizTitle": "Max depth — heights bubble up from the leaves",
                "caption": "A parent cannot compute its height until both children have returned theirs. That bottom-up flow IS post-order.",
            },
            {
                "title": "Pattern 1, the twist — what you return ≠ what you record",
                "body": D("""
                    Sometimes the value you *return to your parent* differs from the value you're *tracking overall*. This is the trick behind **diameter** and **maximum path sum**.

                    ```python
                    def max_path_sum(root):
                        best = float('-inf')                       # the global answer
                        def dfs(node):                             # returns: best DOWNWARD path
                            nonlocal best
                            if not node: return 0
                            left  = max(dfs(node.left), 0)         # drop negative branches
                            right = max(dfs(node.right), 0)
                            best = max(best, node.val + left + right)   # path that BENDS here
                            return node.val + max(left, right)          # path you can EXTEND up
                        dfs(root)
                        return best
                    ```

                    A node *records* the bent path that peaks at itself, but *returns* only a straight path its parent can extend. When a problem feels impossible, ask: **"are these two quantities actually different?"**
                """),
                "viz": {"type": "treeDFS", "variant": "maxpath", "tree": [-10, 9, 20, None, None, 15, 7]},
                "vizTitle": "Max path sum — 'through' is recorded, '↑return' goes to the parent",
                "caption": "The ↑ badge is what the node hands upward (one side only); the global best tracks the best path that bends at some node.",
            },
            {
                "title": "Pattern 2 — validate a property of every node",
                "body": D("""
                    **Signs:** *is it balanced, is it a valid BST, is it symmetric, are two trees identical.* You recurse and return a boolean (or a sentinel like `-1`). For **balanced**, compute height bottom-up and short-circuit with `-1` the instant a subtree is unbalanced.

                    For **valid BST** the key insight is you must pass an allowed `(low, high)` range **down** as arguments — because a node on the far left must be smaller than every ancestor it descended right of, not just its parent:

                    ```python
                    def is_valid_bst(node, low=float('-inf'), high=float('inf')):
                        if not node: return True
                        if not (low < node.val < high): return False
                        return (is_valid_bst(node.left,  low, node.val) and
                                is_valid_bst(node.right, node.val, high))
                    ```
                """),
                "viz": {"type": "treeDFS", "variant": "balanced", "tree": [1, 2, 2, 3, 3, None, None, 4, 4]},
                "vizTitle": "Balanced check — returning −1 the moment a subtree is too lopsided",
                "caption": "As soon as a subtree reports unbalanced, the −1 propagates straight up and the rest of the tree is skipped.",
            },
            {
                "title": "Pattern 4 — Lowest Common Ancestor (the bubble-up)",
                "body": D("""
                    **Signs:** *lowest common ancestor, "where do two nodes meet?"* The trick is slick and reused everywhere: each call reports whether a target lives below it.

                    ```python
                    def lca(node, p, q):
                        if not node or node is p or node is q:
                            return node
                        left  = lca(node.left,  p, q)
                        right = lca(node.right, p, q)
                        if left and right:     # targets in different subtrees -> THIS is the LCA
                            return node
                        return left or right   # both on one side (or neither) -> bubble it up
                    ```

                    The *"if left and right → I'm the meeting point"* logic appears in many tree problems.
                """),
                "viz": {"type": "treeDFS", "variant": "lca",
                        "tree": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "p": 5, "q": 1},
                "vizTitle": "LCA — the node that first sees a target on BOTH sides",
                "caption": "Each subtree reports a found target upward; the first node receiving a hit from both sides is the answer.",
            },
            {
                "title": "Binary Search Trees — the ordered tree",
                "body": D("""
                    A **BST** adds one invariant to a binary tree: for *every* node, all values in its left subtree are smaller and all values in its right subtree are larger. That single rule buys two superpowers:

                    1. **In-order traversal yields values in sorted order** — the source of most BST tricks.
                    2. **Search / insert / delete in `O(height)`** — each comparison throws away half the tree.

                    Search is the purest illustration: compare with the current node, then go left or right. Play it below.

                    ```python
                    def search_bst(root, target):
                        node = root
                        while node:
                            if target == node.val: return node
                            node = node.left if target < node.val else node.right
                        return None
                    ```

                    > The `O(height)` is `O(log n)` only on a **balanced** BST. Insert sorted data into a plain BST and it degenerates into a linked list — `O(n)`. (Self-balancing AVL / Red-Black trees fix this; you rarely implement them, just name them.)
                """),
                "viz": {"type": "bstSearch", "tree": [8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13], "target": 7},
                "vizTitle": "BST search — halve the tree at every comparison",
                "caption": "Each comparison eliminates an entire subtree. Searching for 7: 7<8 go left, 7>3 go right, 7>6 go right — found. Three steps in a 7-node tree.",
            },
            {
                "title": "Validate a BST — the range trick (a classic trap)",
                "body": D("""
                    The tempting wrong answer: check `left.val < node.val < right.val` at each node. **It's insufficient.** A node must be larger than *every* value in its left subtree, not just its immediate child. Counterexample: root 10, left child 5, but 5's right child is 15 — every parent/child pair looks fine, yet 15 sits in 10's left subtree.

                    The fix: pass a valid **`(low, high)` range** down. Going left tightens the upper bound; going right tightens the lower bound.

                    ```python
                    def is_valid_bst(node, low=float('-inf'), high=float('inf')):
                        if not node: return True
                        if not (low < node.val < high): return False
                        return (is_valid_bst(node.left,  low, node.val) and
                                is_valid_bst(node.right, node.val, high))
                    ```

                    > This "carry constraints down through arguments" idea is a pattern in itself — the same shape solves *range-restricted* problems where each node inherits limits from all its ancestors.
                """),
            },
            {
                "title": "K-th smallest — a BST is a sorted stream",
                "body": D("""
                    Because in-order visits a BST in ascending order, the **k-th smallest** value is just the k-th node an in-order traversal emits. Use the *iterative* in-order so you can stop the instant you've counted k — no need to traverse the whole tree.

                    ```python
                    def kth_smallest(root, k):
                        stack, node = [], root
                        while node or stack:
                            while node:
                                stack.append(node); node = node.left
                            node = stack.pop()
                            k -= 1
                            if k == 0: return node.val      # early exit
                            node = node.right
                    ```

                    Whenever you see *"BST" + "k-th"* or *"BST" + "sorted"* or *"BST" + "validate"*, your first thought should be **in-order**.
                """),
            },
            {
                "title": "Path problems — state flows DOWN, plus backtracking",
                "body": D("""
                    Path problems are the mirror image of Pattern 1: instead of answers flowing **up**, accumulated state flows **down** as a parameter. *Does any root-to-leaf path sum to a target?*

                    ```python
                    def has_path_sum(node, target):
                        if not node: return False
                        if not node.left and not node.right:        # a real leaf
                            return node.val == target
                        rest = target - node.val
                        return has_path_sum(node.left, rest) or has_path_sum(node.right, rest)
                    ```

                    Note the distinct **leaf** test — *both* children `None`. A one-child node is not a leaf. To return *all* qualifying paths, add **backtracking**: append on the way down, pop on the way back up, and store a **copy** when you hit a match.

                    ```python
                    def all_paths(root, target):
                        out, path = [], []
                        def dfs(node, rest):
                            if not node: return
                            path.append(node.val); rest -= node.val
                            if not node.left and not node.right and rest == 0:
                                out.append(path[:])         # COPY — path keeps mutating
                            else:
                                dfs(node.left, rest); dfs(node.right, rest)
                            path.pop()                      # backtrack: undo the append
                        dfs(root, target)
                        return out
                    ```

                    > **The #1 backtracking bug:** appending `path` instead of `path[:]`. You'd store a reference that later gets mutated empty. Every `append` must be paired with a matching `pop`.
                """),
            },
            {
                "title": "Reconstruct a tree from traversals",
                "body": D("""
                    Classic construction: rebuild a tree from its **pre-order + in-order** lists. Two facts do all the work:

                    - The **first element of pre-order is always the current root**.
                    - That root's position in **in-order splits left subtree from right subtree**.

                    Recurse on the two halves. A `value → in-order index` hashmap makes the split `O(1)`, giving `O(n)` overall.

                    ```python
                    def build_tree(preorder, inorder):
                        idx = {v: i for i, v in enumerate(inorder)}
                        self_pos = 0
                        def build(lo, hi):
                            nonlocal self_pos
                            if lo > hi: return None
                            root = TreeNode(preorder[self_pos]); self_pos += 1
                            mid = idx[root.val]
                            root.left  = build(lo, mid - 1)     # pre-order does left first
                            root.right = build(mid + 1, hi)
                            return root
                        return build(0, len(inorder) - 1)
                    ```

                    > Why pre-order + in-order (and not in-order alone)? In-order by itself is ambiguous — many trees share it. Pre-order pins down each subtree's root, removing the ambiguity.
                """),
            },
            {
                "title": "Serialize & deserialize — pre-order with null markers",
                "body": D("""
                    To turn a tree into a string and back, use **pre-order and write explicit `None` markers**. The markers are what make the structure unambiguous — without them you can't tell where a subtree ends.

                    ```python
                    def serialize(root):
                        out = []
                        def go(node):
                            if not node: out.append("#"); return
                            out.append(str(node.val)); go(node.left); go(node.right)
                        go(root)
                        return ",".join(out)

                    def deserialize(data):
                        vals = iter(data.split(","))
                        def go():
                            v = next(vals)
                            if v == "#": return None
                            node = TreeNode(int(v)); node.left = go(); node.right = go()
                            return node
                        return go()
                    ```

                    Deserialize works because pre-order emits the root first: consume one token, then the remaining stream is *left subtree serialization followed by right subtree serialization* — exactly what the two recursive `go()` calls consume in order.
                """),
            },
            {
                "title": "Trie — the prefix tree for fast string lookup",
                "body": D("""
                    A **trie** is a tree specialized for strings: each edge is a character, and a root→node path spells a prefix. Prefix queries ("does any word start with…", autocomplete, spell-check) become `O(length)` regardless of how many words are stored.

                    ```python
                    class TrieNode:
                        def __init__(self):
                            self.children = {}            # char -> TrieNode
                            self.is_word = False          # a word ENDS here

                    class Trie:
                        def __init__(self): self.root = TrieNode()
                        def insert(self, word):
                            node = self.root
                            for ch in word:
                                node = node.children.setdefault(ch, TrieNode())
                            node.is_word = True
                        def _walk(self, s):
                            node = self.root
                            for ch in s:
                                if ch not in node.children: return None
                                node = node.children[ch]
                            return node
                        def search(self, word):
                            node = self._walk(word); return bool(node) and node.is_word
                        def starts_with(self, prefix):
                            return self._walk(prefix) is not None
                    ```

                    > **The #1 trie bug:** forgetting `is_word`. Without it you can't tell that "app" was inserted but "ap" wasn't — both are just prefixes on the path to "apple".
                """),
            },
            {
                "title": "Segment tree — range queries with live updates",
                "body": D("""
                    When an array is **mutable** and you need many range queries (sum / min / max), a **segment tree** does both *update* and *range query* in `O(log n)`. Each node stores the aggregate of a range; leaves are single elements; a parent combines its two children.

                    The query splits the asked range against each node's range into **three cases**:

                    1. **No overlap** → contribute the identity (0 for sum).
                    2. **Total overlap** (node range fully inside the query) → return the node's stored value.
                    3. **Partial overlap** → recurse into both children and combine.

                    ```python
                    def range_sum(self, node, seg_lo, seg_hi, q_lo, q_hi):
                        if q_hi < seg_lo or seg_hi < q_lo:          # 1. no overlap
                            return 0
                        if q_lo <= seg_lo and seg_hi <= q_hi:       # 2. total overlap
                            return self.tree[node]
                        mid = (seg_lo + seg_hi) // 2                 # 3. partial — split
                        return (self.range_sum(2*node,   seg_lo, mid,   q_lo, q_hi) +
                                self.range_sum(2*node+1, mid+1, seg_hi, q_lo, q_hi))
                    ```

                    > Allocate `4 * n` for the tree array — the safe universal bound (the tighter `2 * n` only works when `n` is a power of two and invites off-by-one bugs). For pure prefix-sum-with-updates, a Fenwick (Binary Indexed) tree is a lighter alternative.
                """),
            },
            {
                "title": "Your repeatable procedure (run this when you blank out)",
                "body": D("""
                    1. **Draw a small tree** (3–5 nodes). Always. You cannot solve what you cannot see.
                    2. **Pick DFS or BFS.** Mentions *levels / depth / shortest*? → BFS. Otherwise → DFS.
                    3. **If DFS, choose the direction of information flow.** Answers flow **up** (children → parent)? → post-order, return values (Patterns 1 & 2). State flows **down** (root → node)? → pass parameters (path / valid-BST).
                    4. **Write the base case first.** Literally: *"What's the answer for an empty tree (`node is None`)?"*
                    5. **Write the combine step**, trusting the recursive calls already work.
                    6. **Ask: is what I return the same as what I track?** If not, use a `nonlocal` global (the Pattern 1 twist).
                    7. **Trace your small tree by hand**, paying attention to leaves and `None` children.

                    Do steps 4 and 5 *in writing* every time and you will stop freezing.
                """),
            },
            {
                "title": "Complexity — what to say in the interview",
                "body": D("""
                    | | Cost | Why |
                    |---|------|-----|
                    | **Time** | `O(n)` | you visit each node a constant number of times |
                    | **Space (DFS)** | `O(h)` | the recursion/call stack; `h` = height |
                    | balanced tree | `O(log n)` | height ≈ log n |
                    | worst case (a "stick") | `O(n)` | height = n |
                    | **Space (BFS)** | `O(w)` | max width — up to `O(n)` at the bottom level |

                    > **One paragraph to remember:** Every tree problem is *traverse* or *combine children's answers*. Pick DFS (default) or BFS (levels/shortest). For DFS, decide whether info flows **up** (return values, post-order) or **down** (parameters). Write the **base case** first, then the **combine step** trusting the recursion already works. Draw a small tree. That's the whole skill.
                """),
            },
            {
                "title": "Common mistakes that quietly cost offers",
                "body": D("""
                    - **Validating a BST with only immediate-child comparisons.** Each node faces constraints from *all* its ancestors — use the `(low, high)` range.
                    - **Confusing depth and height.** Depth counts down from the root; height counts up from the leaves. Many problems are sensitive to which one they ask for.
                    - **Treating a one-child node as a leaf.** A leaf has *both* children `None`. This breaks path-sum problems if you terminate early.
                    - **Appending the path list instead of a copy.** `out.append(path)` stores a reference that later mutates to empty — always `path[:]`.
                    - **Re-computing height at every node (`O(n²)`).** Fuse the work: one post-order pass returns the height *and* updates your global (diameter, max-path-sum).
                    - **Recursion depth on skewed trees.** Python's ~1000-frame limit overflows on a "stick". Use an iterative traversal or raise the limit — and *say so* in the interview.
                    - **Assuming BST ops are `O(log n)` unconditionally.** They're `O(log n)` only when balanced; degenerate BSTs are `O(n)`.
                """),
            },
        ],
    },
    {
        "id": "graphs",
        "icon": "🕸️",
        "title": "How to Solve Graph Problems",
        "shortTitle": "Graphs",
        "blurb": "Step 1 is always recognising 'this is a graph' and turning it into one — then the "
                 "right algorithm does the rest. This guide goes from BFS/DFS to topological sort, "
                 "Union-Find, Dijkstra, MST, and the compound-state BFS that senior interviews love.",
        "sections": [
            {
                "title": "The mental model — four buckets",
                "body": D("""
                    A tree is just a graph with no cycles. Graphs add two complications: **cycles** (so you must track *visited*) and **many ways to represent the input**. Almost every graph problem is one of four buckets — your first job on any problem is to decide which:

                    1. **Connectivity / components** — *"can I reach B from A?", "how many separate groups / islands?"* → **DFS or BFS flood fill.**
                    2. **Shortest path** — *"fewest steps", "minimum cost", "nearest"* → **BFS** (unweighted) or **Dijkstra** (weighted).
                    3. **Ordering with dependencies** — *"course schedule", "build order", "is there a cycle?"* → **topological sort (Kahn's).**
                    4. **Minimum spanning tree** — *"connect everything as cheaply as possible"* → **Prim's / Kruskal's.**
                """),
            },
            {
                "title": "Graph vocabulary — terms interviewers use without explaining",
                "body": D("""
                    Formally a graph is `G = (V, E)`: a set of **vertices** (nodes) and **edges** between them. Every other structure is a restricted graph — a linked list, a tree, a grid are all graphs. Know these terms cold:

                    | Term | Meaning |
                    |------|---------|
                    | **Directed vs undirected** | A→B implies B→A only when *undirected* (Twitter follows = directed; Facebook friends = undirected) |
                    | **Weighted vs unweighted** | edges carry a cost (distance/time/price) vs all edges equal |
                    | **Cycle** | a path that returns to its start; a **DAG** is a directed graph with *no* cycles |
                    | **Connected** | every node can reach every other (for directed: *strongly* connected) |
                    | **Degree** | edges touching a node; directed splits into **in-degree** / **out-degree** |
                    | **Sparse vs dense** | edge count near `V` vs near `V²` — drives your representation choice |

                    > Two facts decide your whole approach, so extract them first: **directed or undirected?** and **weighted or unweighted?** In-degree (number of incoming edges) is the engine of topological sort — a node with in-degree 0 has no unmet dependencies.
                """),
            },
            {
                "title": "Difference 1 — you MUST track visited nodes",
                "body": D("""
                    A tree cannot loop back on itself; a graph can. DFS a graph without remembering where you've been and you loop **forever**. The single most common graph bug is a missing `visited` set.

                    ```python
                    visited = set()
                    def dfs(node):
                        if node in visited:        # without this line: infinite loop
                            return
                        visited.add(node)
                        for nb in graph[node]:
                            dfs(nb)
                    ```

                    > **Rule:** every graph traversal needs a `visited` set (or a `visited` grid for 2D problems). No exceptions.
                """),
            },
            {
                "title": "Difference 2 — recognise the graph in disguise",
                "body": D("""
                    The graph is rarely handed to you as `{node: [neighbours]}`. Learning to spot the format and **build the adjacency list** is the skill that's missing when you "can't start."

                    | Input format | What to do |
                    |--------------|------------|
                    | **Edge list** `[[0,1],[0,2]]` | loop and append to a `defaultdict(list)`; add **both** directions if undirected |
                    | **Adjacency matrix** `M[i][j]==1` | neighbours are the columns equal to 1 — often no list needed |
                    | **2D grid** | each **cell is a node**; neighbours are up/down/left/right cells |
                    | **Object with `.neighbors`** | already a graph; just traverse it |

                    ```python
                    from collections import defaultdict
                    graph = defaultdict(list)
                    for u, v in edges:
                        graph[u].append(v)
                        graph[v].append(u)      # add BOTH only if UNDIRECTED
                    ```

                    For a **grid**, memorise the four deltas and the bounds check — you'll write them a hundred times:

                    ```python
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:   # up, down, left, right
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                            ...   # (nr, nc) is a valid neighbour
                    ```
                """),
            },
            {
                "title": "Adjacency list vs matrix — and the 'implicit graph' you build yourself",
                "body": D("""
                    Your representation choice decides the cost of every operation. Two explicit forms, and one you construct on the fly:

                    | Representation | Space | "Are u,v adjacent?" | Best for |
                    |----------------|-------|---------------------|----------|
                    | **Adjacency list** | `O(V + E)` | `O(degree)` | almost everything — sparse graphs (use this 90% of the time) |
                    | **Adjacency matrix** | `O(V²)` | `O(1)` | dense graphs, or when you constantly test edge existence / use Floyd-Warshall |

                    A sparse graph of 10,000 nodes and 20,000 edges costs ~30K entries as a list but **100 million** as a matrix — that's why the list is the default.

                    **Implicit graphs — the skill that separates strong candidates.** Many problems never hand you a graph; you *recognise* one:

                    - **Grid:** each cell is a node, neighbours are the 4 (or 8) adjacent cells. The grid *is* the adjacency list.
                    - **String transformation:** each word is a node; an edge is a single-character change (*Word Ladder*, *Open the Lock*).
                    - **State space:** the node is a *compound state* like `(row, col, keys)` or `(row, col, walls_left)`; each legal transition is an edge.

                    > At senior level no one says "this is a graph problem." You're given an ambiguous scenario and must *define* what a node and an edge are. Practice saying it in one sentence before you code.
                """),
            },
            {
                "title": "The two core traversals (memorise both)",
                "body": D("""
                    **BFS** uses a queue and explores level by level — it finds the **shortest path in an unweighted graph for free**. **DFS** uses a stack (or recursion) and dives deep — great for "explore everything / is it connected?".

                    ```python
                    from collections import deque
                    def bfs(graph, start):
                        visited = {start}              # mark when you ENQUEUE, not when you dequeue
                        queue = deque([start])
                        while queue:
                            node = queue.popleft()
                            for nb in graph[node]:
                                if nb not in visited:
                                    visited.add(nb)
                                    queue.append(nb)
                    ```

                    > **Critical subtlety:** mark a node visited the moment you **add it to the queue**, not when you pop it — otherwise the same node gets enqueued many times.

                    Play the visualization and toggle **BFS vs DFS** to see the queue (FIFO) and stack (LIFO) produce very different visit orders on the *same* graph.
                """),
                "viz": {"type": "graphTraversal",
                        "graph": {"A": ["B", "C"], "B": ["A", "D", "E"], "C": ["A", "F"],
                                  "D": ["B"], "E": ["B", "F"], "F": ["C", "E"]},
                        "start": "A"},
                "vizTitle": "BFS vs DFS — same graph, different frontier",
                "caption": "BFS (queue) fans out level by level; DFS (stack) plunges down one branch first. Watch the side panel switch between queue and stack.",
            },
            {
                "title": "BFS for shortest paths — distance, grids, and multi-source",
                "body": D("""
                    BFS expands in concentric rings, so **the first time it reaches a node it has found the shortest path** (in an unweighted graph). Carry the distance alongside each node:

                    ```python
                    def bfs_distance(graph, start, target):
                        visited = {start}
                        queue = deque([(start, 0)])           # (node, distance)
                        while queue:
                            node, dist = queue.popleft()
                            if node == target: return dist
                            for nb in graph[node]:
                                if nb not in visited:
                                    visited.add(nb)
                                    queue.append((nb, dist + 1))
                        return -1
                    ```

                    **Multi-source BFS** is the move when distance is measured from *any* of several starts (Rotting Oranges, 01 Matrix). Don't run BFS from each source — **seed the queue with all sources at distance 0** and expand once. Because BFS processes nodes in distance order, every cell is reached first by its nearest source.

                    ```python
                    queue = deque()
                    for r in range(rows):
                        for c in range(cols):
                            if grid[r][c] == SOURCE:
                                dist[r][c] = 0
                                queue.append((r, c))          # ALL sources start together
                    ```

                    > Reach for multi-source BFS whenever the question is "minimum distance to the *nearest* X" or "how many rounds until everything is infected/filled."
                """),
            },
            {
                "title": "Which traversal do I pick?",
                "body": D("""
                    | If the problem asks… | Use |
                    |----------------------|-----|
                    | Shortest path / fewest moves (unweighted) | **BFS** |
                    | "Is everything connected?" / count components | either (DFS is shorter) |
                    | Explore or flood-fill a region | either |
                    | Shortest path with **weights / costs** | **Dijkstra** (heap) |
                    | Dependency order / cycle in a directed graph | **topological sort** |

                    > **Default to BFS when you see "shortest" or "minimum steps."** BFS reaches nodes in increasing order of distance, so it gets the shortest unweighted path for free. DFS does not.
                """),
            },
            {
                "title": "Pattern: count connected components (flood fill)",
                "body": D("""
                    The most common graph pattern. *Loop over every node; if it's unvisited it's a **new** component — increment a counter and flood-fill to drown the whole component so you don't count it twice.*

                    ```python
                    def count_components(graph, n):
                        visited, count = set(), 0
                        for node in range(n):
                            if node not in visited:
                                count += 1            # found a new component
                                dfs(graph, node, visited)   # drown the whole island
                        return count
                    ```

                    *Number of Provinces* is this exact shape on an adjacency matrix — each DFS launch is one province.
                """),
                "viz": {"type": "matrixComponents", "matrix": [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]},
                "vizTitle": "Number of Provinces — every DFS launch = one component",
                "caption": "The outer loop finds an unvisited seed; the inner DFS marks its entire group visited. The number of launches is the answer.",
            },
            {
                "title": "A grid IS a graph — Number of Islands",
                "body": D("""
                    This trips everyone up. In grid problems each **cell is a node** and its neighbours are the four adjacent cells. There's no `graph` dict — the grid itself is the adjacency structure. Scan every cell; each unvisited land cell starts a new island, and the flood-fill sinks it.

                    > **Mantra for component problems:** *the outer loop finds a new seed; the inner traversal drowns its whole island.*
                """),
                "viz": {"type": "gridDFS",
                        "grid": [["1", "1", "0", "0", "1"],
                                 ["1", "0", "0", "1", "1"],
                                 ["0", "0", "1", "0", "0"],
                                 ["0", "1", "1", "0", "1"]]},
                "vizTitle": "Number of Islands — flood fill on a grid",
                "caption": "Each time the scan hits un-sunk land, that's a new island; the flood fill sinks every connected land cell before the scan continues.",
            },
            {
                "title": "Cycle detection in an UNDIRECTED graph",
                "body": D("""
                    DFS while remembering each node's **parent**. If you reach an already-visited neighbour that **isn't the parent** you came from, you've looped back → there's a cycle.

                    ```python
                    def has_cycle(graph, node, parent, visited):
                        visited.add(node)
                        for nb in graph[node]:
                            if nb not in visited:
                                if has_cycle(graph, nb, node, visited): return True
                            elif nb != parent:        # visited AND not the parent -> cycle
                                return True
                        return False
                    ```
                """),
                "viz": {"type": "undirectedCycle",
                        "graph": {"0": [1, 2], "1": [0, 2], "2": [0, 1, 3], "3": [2]}, "start": 0},
                "vizTitle": "Undirected cycle — a back-edge to a non-parent",
                "caption": "The cycle is flagged the instant DFS meets an already-visited node that is not the parent it arrived from.",
            },
            {
                "title": "Cycle detection in a DIRECTED graph — three colors",
                "body": D("""
                    Parent-tracking *only works for undirected graphs* — direction changes what counts as a back-edge. For directed graphs, give each node one of **three colors**:

                    - **White** — not visited yet.
                    - **Gray** — *on the current DFS path* (entered, not finished).
                    - **Black** — fully explored (all descendants done).

                    A cycle exists exactly when DFS reaches a **Gray** node: you've looped back to something still on your own path. Reaching a Black node is harmless — that subtree is finished, not part of your path.

                    ```python
                    WHITE, GRAY, BLACK = 0, 1, 2
                    def has_cycle_directed(adj, n):
                        color = [WHITE] * n
                        def dfs(u):
                            color[u] = GRAY
                            for v in adj[u]:
                                if color[v] == GRAY: return True          # back-edge → cycle
                                if color[v] == WHITE and dfs(v): return True
                            color[u] = BLACK
                            return False
                        return any(color[u] == WHITE and dfs(u) for u in range(n))
                    ```

                    > Kahn's algorithm (next) detects directed cycles too — if it can't output all `n` nodes, a cycle blocked the rest. Use whichever the problem makes cleaner: Kahn's when you also need the *order*, 3-color when you just need *yes/no* via DFS.
                """),
            },
            {
                "title": "Dependency order — Kahn's topological sort",
                "body": D("""
                    **Triggers:** *course schedule, prerequisites, build/compile order, "is there a cycle in a directed graph?"* Idea: repeatedly remove nodes with **no remaining prerequisites** (in-degree 0). Remove them all → valid order, no cycle. Some get stuck → cycle.

                    ```python
                    from collections import defaultdict, deque
                    def topo_sort(n, edges):                   # edges: [u_before, v_after]
                        graph, indeg = defaultdict(list), [0]*n
                        for u, v in edges:
                            graph[u].append(v); indeg[v] += 1
                        queue = deque(i for i in range(n) if indeg[i] == 0)
                        order = []
                        while queue:
                            node = queue.popleft(); order.append(node)
                            for nb in graph[node]:
                                indeg[nb] -= 1                 # "remove" the edge
                                if indeg[nb] == 0: queue.append(nb)
                        return order if len(order) == n else []   # empty => cycle
                    ```

                    *Course Schedule I* = "is `len(order) == n`?"; *Course Schedule II* = "return `order`." **Same code.** That's the payoff of recognising the pattern.
                """),
                "viz": {"type": "kahn", "vertices": 6, "adj": [[1, 2], [3], [3], [4, 5], [], []]},
                "vizTitle": "Kahn's algorithm — peeling off in-degree-0 nodes",
                "caption": "Watch each in-degree badge tick down as edges are removed; a node joins the queue the moment its in-degree hits 0. Processing all nodes proves there is no cycle.",
            },
            {
                "title": "Clone a graph — traversal + an old→new map",
                "body": D("""
                    **Trigger:** *deep copy this graph.* BFS/DFS the original while keeping a dictionary mapping each original node to its clone. That map both prevents cloning twice and doubles as your `visited` set.
                """),
                "viz": {"type": "cloneBFS",
                        "graph": {"1": [2, 4], "2": [1, 3], "3": [2, 4], "4": [1, 3]}, "start": 1},
                "vizTitle": "Clone graph — BFS building a value→clone map",
                "caption": "The first time a node is seen, its clone is created and enqueued; revisits just reuse the map. One pass copies every node and re-links every edge.",
            },
            {
                "title": "Union-Find — near-O(1) connectivity",
                "body": D("""
                    When the question is *"are these two connected?"* or *"connect them dynamically"* — without needing the actual path — **Union-Find** (Disjoint Set Union) beats BFS/DFS. It supports `find` (which group am I in?) and `union` (merge two groups) in *near-constant* amortised time.

                    Two optimisations make it fast: **path compression** (point every node straight at its root during `find`) and **union by rank** (hang the shorter tree under the taller). Together: `O(α(n))` per op — effectively constant.

                    ```python
                    class UnionFind:
                        def __init__(self, n):
                            self.parent = list(range(n))
                            self.rank = [0] * n
                        def find(self, x):
                            if self.parent[x] != x:
                                self.parent[x] = self.find(self.parent[x])   # path compression
                            return self.parent[x]
                        def union(self, a, b):
                            ra, rb = self.find(a), self.find(b)
                            if ra == rb: return False        # already connected (edge is redundant)
                            if self.rank[ra] < self.rank[rb]: ra, rb = rb, ra
                            self.parent[rb] = ra
                            if self.rank[ra] == self.rank[rb]: self.rank[ra] += 1
                            return True
                    ```

                    > That `False` return is gold: it means the two endpoints were *already* connected, so this edge forms a cycle — exactly how you solve *Redundant Connection* and the cycle check inside Kruskal's MST.
                """),
            },
            {
                "title": "Dijkstra — shortest path with weights",
                "body": D("""
                    Dijkstra is **BFS generalised to weighted graphs**. A plain queue processes nodes in discovery order; Dijkstra swaps it for a **min-heap** that always expands the node with the smallest known distance. When a node is popped, its distance is *final* — because every alternative route goes through nodes that are already at least as far, and all weights are non-negative.

                    ```python
                    import heapq
                    def dijkstra(adj, start, n):              # adj[u] = [(v, weight), ...]
                        dist = [float('inf')] * n
                        dist[start] = 0
                        heap = [(0, start)]                   # (distance, node)
                        while heap:
                            d, u = heapq.heappop(heap)
                            if d > dist[u]: continue          # stale entry — lazy deletion
                            for v, w in adj[u]:
                                if d + w < dist[v]:
                                    dist[v] = d + w
                                    heapq.heappush(heap, (dist[v], v))
                        return dist
                    ```

                    The `if d > dist[u]: continue` guard is essential: we can't delete outdated heap entries, so we push fresh ones and skip the stale ones on pop. Play it below — watch the heap always serve the closest node, and a distance go *final* the instant it's popped.

                    > **Why not BFS?** BFS treats every edge as cost 1, so a 3-hop cheap path can beat a 1-hop expensive one and BFS would miss it. **Why non-negative only?** A later negative edge could undercut a distance you already declared final — that breaks the greedy guarantee (use Bellman-Ford instead).
                """),
                "viz": {"type": "dijkstra", "nodes": [0, 1, 2, 3, 4],
                        "edges": [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1], [2, 3, 5], [3, 4, 3]],
                        "start": 0},
                "vizTitle": "Dijkstra — the min-heap always serves the closest node",
                "caption": "Edge weights are labelled; node badges show the best-known distance. Popping a node finalizes it (green). Final distances from 0: [0, 3, 1, 4, 7].",
            },
            {
                "title": "More shortest-path tools (know when, not just how)",
                "body": D("""
                    Dijkstra isn't always the answer. Match the tool to the constraints:

                    | Situation | Tool | Time |
                    |-----------|------|------|
                    | Unweighted | **BFS** | `O(V + E)` |
                    | Non-negative weights | **Dijkstra** | `O(E log V)` |
                    | **Negative** weights possible | **Bellman-Ford** | `O(V · E)` |
                    | All-pairs, small V (≤ ~400) | **Floyd-Warshall** | `O(V³)` |
                    | Weights are only **0 or 1** | **0-1 BFS** (deque) | `O(V + E)` |

                    **Bellman-Ford** relaxes every edge `V-1` times (the longest simple path has `V-1` edges); one extra round that still improves a distance proves a **negative cycle**. **Floyd-Warshall** is a 3-line DP — `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])` with `k` as the *outermost* loop. **0-1 BFS** uses a deque: push 0-weight edges to the **front**, 1-weight edges to the **back**, keeping the deque distance-sorted without a heap.

                    ```python
                    # 0-1 BFS core
                    if w == 0: dq.appendleft(v)     # same distance layer
                    else:      dq.append(v)          # next distance layer
                    ```
                """),
            },
            {
                "title": "Minimum spanning tree — Kruskal & Prim",
                "body": D("""
                    An **MST** connects all `V` nodes of a weighted undirected graph with `V-1` edges at minimum total cost. Two greedy algorithms, both correct by the *cut property* (the lightest edge crossing any cut is in some MST):

                    **Kruskal's (edge-centric):** sort all edges by weight, add each one unless it would form a cycle — the cycle test is exactly Union-Find's `union` returning `False`.

                    ```python
                    def kruskal(n, edges):                    # edges: (u, v, weight)
                        uf, total, used = UnionFind(n), 0, 0
                        for u, v, w in sorted(edges, key=lambda e: e[2]):
                            if uf.union(u, v):
                                total += w; used += 1
                                if used == n - 1: break
                        return total if used == n - 1 else None    # None = disconnected
                    ```

                    **Prim's (node-centric):** grow the tree from one node, repeatedly taking the cheapest edge to a node not yet in the tree — a min-heap, almost identical in shape to Dijkstra.

                    > **Pick by input:** edge list / sparse → **Kruskal's**; adjacency list / dense → **Prim's**. Either is accepted; write whichever you can produce bug-free. Trigger phrase: *"connect all nodes at minimum total cost."*
                """),
            },
            {
                "title": "Bipartite check — 2-coloring",
                "body": D("""
                    A graph is **bipartite** if its nodes split into two groups with edges only *between* groups, never within one. Equivalent question: *can we 2-color it with no same-colored edge?* BFS/DFS and alternate colors; a clash means an odd cycle, so it's not bipartite.

                    ```python
                    def is_bipartite(adj, n):
                        color = [-1] * n
                        for s in range(n):
                            if color[s] != -1: continue
                            color[s] = 0; queue = deque([s])
                            while queue:
                                u = queue.popleft()
                                for v in adj[u]:
                                    if color[v] == -1:
                                        color[v] = 1 - color[u]; queue.append(v)
                                    elif color[v] == color[u]:
                                        return False        # same color on an edge
                        return True
                    ```

                    Trigger phrases: *"split into two teams", "two groups with no internal conflict", "is this graph 2-colorable?"*
                """),
                "viz": {"type": "bipartite", "graph": {"0": [1, 3], "1": [0, 2], "2": [1, 3], "3": [0, 2]}},
                "vizTitle": "Bipartite — force neighbours the opposite color",
                "caption": "Color A and color B alternate across every edge. This 4-cycle 2-colors cleanly → bipartite. An odd cycle (triangle) would hit a same-color edge and fail.",
            },
            {
                "title": "BFS on compound state — the senior-level pattern",
                "body": D("""
                    The pattern that separates strong candidates: the node isn't a plain position, it's a **tuple encoding all relevant state**, and each legal transition is an edge. *Shortest path in a grid where you may break up to `k` walls* — the state is `(row, col, walls_left)`, **not** `(row, col)`. Arriving at the same cell with a different wall budget opens different futures, so it's a different node.

                    ```python
                    start = (0, 0, k)
                    visited = {start}
                    queue = deque([(0, 0, k, 0)])             # row, col, walls_left, steps
                    while queue:
                        r, c, walls, steps = queue.popleft()
                        if (r, c) == (rows-1, cols-1): return steps
                        for nr, nc in neighbours(r, c):
                            nw = walls - grid[nr][nc]         # spend a wall if cell is blocked
                            if nw >= 0 and (nr, nc, nw) not in visited:
                                visited.add((nr, nc, nw))
                                queue.append((nr, nc, nw, steps + 1))
                    ```

                    BFS still gives the shortest path because every move costs 1 — the graph is just *bigger* (`R × C × (k+1)` nodes instead of `R × C`).

                    > **The defining bug:** putting only `(row, col)` in `visited`. You'd collapse genuinely different states and get a wrong answer. The `visited` set must hold the **full** state tuple. This same idea powers *Shortest Path to Get All Keys* (`(pos, keys_bitmask)`) and *Cheapest Flights within K Stops* (`(city, stops_used)`).
                """),
            },
            {
                "title": "Your repeatable procedure",
                "body": D("""
                    1. **Identify the graph.** What are the nodes? When are two connected? Say it in one sentence: *"Nodes are cells; edges connect adjacent land cells."*
                    2. **Note the input format** (edge list / matrix / grid / object) and decide whether to **build an adjacency list** or traverse the input directly.
                    3. **Directed or undirected?** This decides whether you add one direction or both.
                    4. **Classify into one of the four buckets** (connectivity, shortest path, dependency order, MST).
                    5. **Pick the tool:** components → DFS/BFS flood fill (or Union-Find) · shortest unweighted → BFS · shortest weighted → Dijkstra (negative → Bellman-Ford) · dependency order / directed cycle → Kahn's or 3-color · connect-all-cheaply → MST · two groups → bipartite · constraints in the state → compound-state BFS.
                    6. **Write the `visited` set first** (with the *full* state), then the traversal, then the bookkeeping (counter / distance array / order list / clone map).
                    7. **Test on a tiny example with a cycle** to confirm `visited` saves you.
                """),
            },
            {
                "title": "Complexity — what to say in the interview",
                "body": D("""
                    Let **V** = vertices, **E** = edges.

                    | Algorithm | Time | Space |
                    |-----------|------|-------|
                    | BFS / DFS | `O(V + E)` | `O(V)` |
                    | Grid (R×C) | `O(R · C)` | `O(R · C)` |
                    | Topological sort (Kahn's) | `O(V + E)` | `O(V)` |
                    | Union-Find (per op, amortised) | `O(α(n))` ≈ `O(1)` | `O(V)` |
                    | Dijkstra (binary heap) | `O(E log V)` | `O(V)` |
                    | Bellman-Ford | `O(V · E)` | `O(V)` |
                    | Floyd-Warshall (all pairs) | `O(V³)` | `O(V²)` |
                    | MST (Kruskal / Prim) | `O(E log E)` / `O(E log V)` | `O(V)` |

                    > **One paragraph to remember:** Step 1 is always *turn the input into a graph* — identify nodes, identify when two are connected, decide directed vs undirected and weighted vs unweighted. Then **classify**: connectivity → flood fill or Union-Find; shortest unweighted → BFS; shortest weighted → Dijkstra (negative → Bellman-Ford); dependency order or directed cycle → Kahn's; cheapest connection → MST; two groups → bipartite; constraints baked into the node → compound-state BFS. **Always keep a `visited` set** — the one thing trees let you skip and graphs never do.
                """),
            },
            {
                "title": "Common mistakes that quietly cost offers",
                "body": D("""
                    - **Marking visited at *dequeue* instead of *enqueue* in BFS.** Multiple parents enqueue the same node before it's processed → blows `O(V+E)` up to `O(V²)`. Mark when you enqueue.
                    - **Using DFS for a shortest-path question.** DFS can reach a node by a longer route first. If it says "minimum / shortest / fewest," use BFS (or Dijkstra).
                    - **Not handling disconnected components.** Loop over *all* nodes as potential starts; a single `bfs(0)` misses everything not reachable from 0.
                    - **Undirected cycle logic on a directed graph.** Parent-tracking is undirected-only; directed graphs need the 3-color method.
                    - **Forgetting Dijkstra fails on negative weights.** A later negative edge can undercut a "finalized" distance. Switch to Bellman-Ford.
                    - **Wrong (too small) state in `visited`.** For compound-state BFS, track the *full* tuple `(pos, constraint)` — tracking only `pos` collapses distinct states and gives wrong answers.
                """),
            },
        ],
    },
    {
        "id": "dynamic-programming",
        "icon": "🧩",
        "title": "How to Solve Dynamic Programming Problems",
        "shortTitle": "Dynamic Programming",
        "blurb": "DP looks like wizardry until you see the trick: it is just recursion where you "
                 "stop re-solving the same subproblem. Master one 5-step framework and DP turns "
                 "from 'no idea where to start' into 'fill in the blanks'.",
        "sections": [
            {
                "title": "What DP actually is (the honest definition)",
                "body": D("""
                    Dynamic programming is **recursion + memory**. Nothing more mystical than that. A problem is a DP problem when it has both:

                    1. **Overlapping subproblems** — the naive recursion solves the *same* smaller problem again and again. (Plain `fib(n) = fib(n-1) + fib(n-2)` recomputes `fib(3)` an exponential number of times.)
                    2. **Optimal substructure** — the best answer to the whole is built from the best answers to its parts.

                    DP's whole job is to compute each subproblem **once**, store it, and reuse it. That single idea collapses exponential time into polynomial time.

                    > **The reframe that unlocks DP:** stop trying to find a clever formula. Instead, ask *"what is the smallest piece of information I'd need from smaller versions of this problem to answer the current one?"* That piece is your **state**, and the relationship is your **recurrence**.
                """),
            },
            {
                "title": "The 5-step framework (use this on every DP problem)",
                "body": D("""
                    When you don't know where to start, answer these five questions **in order, in writing**. Filling them in *is* solving the problem.

                    1. **Define the state.** What does `dp[i]` (or `dp[i][j]`) *mean* in one English sentence? e.g. *"`dp[i]` = the most money I can rob from houses `0..i`."* If you can't say it in words, you don't have it yet.
                    2. **Write the recurrence (transition).** How is `dp[i]` built from smaller states? This is the heart. e.g. *"`dp[i] = max(dp[i-1], nums[i] + dp[i-2])`."*
                    3. **Set the base cases.** The smallest states you can answer directly (`dp[0]`, empty input, etc.).
                    4. **Decide the evaluation order.** Bottom-up: fill states so every value you depend on already exists (usually a simple `for` loop). Top-down: recurse + cache.
                    5. **Read off the answer.** Which cell holds the final result? `dp[n]`? `dp[m][n]`? The max over the whole table?

                    | Question | "max subarray" | "coin change" | "longest common subsequence" |
                    |----------|----------------|---------------|------------------------------|
                    | **State** | best sum ending at `i` | fewest coins for amount `a` | LCS of `A[..i]`, `B[..j]` |
                    | **Transition** | `max(nums[i], cur+nums[i])` | `min(dp[a-c]+1)` over coins | match → `1+dp[i-1][j-1]`; else `max(up,left)` |
                    | **Base** | `dp[0]=nums[0]` | `dp[0]=0` | empty string → 0 |
                    | **Answer** | max over all `dp[i]` | `dp[amount]` | `dp[m][n]` |
                """),
            },
            {
                "title": "Memoization vs Tabulation — two ways to add memory",
                "body": D("""
                    There are exactly two implementation styles. They compute the same thing.

                    **Top-down (memoization)** — write the natural recursion, then cache results so each subproblem runs once. Easiest to *derive*.

                    ```python
                    from functools import lru_cache
                    @lru_cache(maxsize=None)
                    def solve(i):
                        if i < 0: return 0                 # base case
                        return max(solve(i-1), nums[i] + solve(i-2))   # recurrence
                    ```

                    **Bottom-up (tabulation)** — fill an array from the base cases up. Often faster (no recursion overhead) and lets you *space-optimize*.

                    ```python
                    dp = [0] * (n + 1)
                    for i in range(n):                     # evaluation order
                        dp[i+1] = max(dp[i], nums[i] + (dp[i-1] if i else 0))
                    return dp[n]
                    ```

                    > **Practical advice:** *derive* with top-down (it mirrors your recurrence), then *convert* to bottom-up if you need the speed or the space saving. They are interchangeable.
                """),
            },
            {
                "title": "Pattern A — 1D DP: best run ending here (Kadane)",
                "body": D("""
                    The simplest DP family: `dp[i]` summarises *the best answer that ends exactly at index `i`*. Maximum-subarray (Kadane) is the canonical example.

                    *State:* `dp[i]` = largest subarray sum ending at `i`. *Transition:* either start fresh at `nums[i]`, or extend the previous run: `dp[i] = max(nums[i], dp[i-1] + nums[i])`. *Answer:* the max over all `dp[i]`.

                    Watch the `current` value either reset or grow at each step — that single decision is the entire recurrence.
                """),
                "viz": {"type": "kadane", "nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]},
                "vizTitle": "Kadane — extend the run or restart, at every index",
                "caption": "`current` = best sum ending here; `best` = the global maximum seen so far. The highlighted band at the end is the winning subarray.",
            },
            {
                "title": "Pattern B — 1D DP: take-or-skip decisions (House Robber)",
                "body": D("""
                    A huge DP family is *"at each item, choose one of a few options."* House Robber: rob the most money without taking two adjacent houses.

                    *State:* `dp[i]` = max money from houses `0..i`. *Transition:* `dp[i] = max(skip = dp[i-1], rob = nums[i] + dp[i-2])`. Since each state only looks back two steps, you can drop the whole array and keep **two rolling variables** — O(1) space.

                    This *"take it (and jump) vs skip it"* shape also powers Coin Change, Knapsack, Jump Game, and Decode Ways.
                """),
                "viz": {"type": "dpRolling", "nums": [2, 7, 9, 3, 1]},
                "vizTitle": "House Robber — rolling DP with two variables",
                "caption": "Each house compares `rob` (its value + dp two back) against `skip` (dp one back). The robbed houses are highlighted at the end.",
            },
            {
                "title": "Pattern C — 1D tabulation table (Coin Change)",
                "body": D("""
                    When the answer for `n` depends on several smaller amounts, build the **full table bottom-up**. Coin Change: fewest coins to make a target amount.

                    *State:* `dp[a]` = fewest coins to make amount `a`. *Transition:* try every coin `c`: `dp[a] = min(dp[a], dp[a-c] + 1)`. *Base:* `dp[0] = 0`; everything else starts at ∞ (unreachable). *Answer:* `dp[amount]`.

                    ```python
                    dp = [0] + [float('inf')] * amount
                    for a in range(1, amount + 1):
                        for c in coins:
                            if c <= a:
                                dp[a] = min(dp[a], dp[a - c] + 1)
                    return dp[amount] if dp[amount] != float('inf') else -1
                    ```

                    The visualization shows each cell being filled from a *smaller already-solved cell* — that backward arrow is the recurrence made visible. This is the mental model for nearly every tabulated DP.
                """),
                "viz": {"type": "coinChange", "coins": [1, 3, 4], "amount": 6},
                "vizTitle": "Coin Change — filling dp[amount] from smaller subproblems",
                "caption": "Each new amount reuses the best answer of a smaller amount (the highlighted earlier cell) plus one coin. dp[0]=0 is the seed everything grows from.",
            },
            {
                "title": "Pattern D — 2D grid DP (Longest Common Subsequence)",
                "body": D("""
                    When the state needs **two indices** — two strings, a grid, or an item-and-capacity pair — use a 2D table. Longest Common Subsequence is the archetype.

                    *State:* `dp[i][j]` = LCS length of `A[..i]` and `B[..j]`. *Transition:* if the characters match, `dp[i][j] = 1 + dp[i-1][j-1]` (diagonal); otherwise `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` (drop one char). *Answer:* bottom-right cell.

                    The same grid shape solves Edit Distance, Unique Paths, 0/1 Knapsack, and Regex Matching — only the transition changes.
                """),
                "viz": {"type": "dpGrid", "a": "ABCBDAB", "b": "BDCAB", "mode": "subsequence"},
                "vizTitle": "LCS — each cell looks diagonal (match) or up/left (mismatch)",
                "caption": "Green cells are character matches that extend the diagonal; others copy the better of the neighbour above or to the left. The answer accumulates into the bottom-right corner.",
            },
            {
                "title": "Pattern D variant — when a mismatch resets (substring)",
                "body": D("""
                    A tiny change to the transition gives a completely different problem. **Longest common *substring*** (contiguous) must reset to 0 on a mismatch, because a substring can't have gaps:

                    ```python
                    if a[i-1] == b[j-1]:
                        dp[i][j] = 1 + dp[i-1][j-1]
                    else:
                        dp[i][j] = 0          # subsequence would do max(up, left) instead
                    best = max(best, dp[i][j])
                    ```

                    Compare this visualization to the previous one: same grid, one line different, and the answer is now *the largest cell anywhere*, not the corner. Recognising which transition a problem wants is the real DP skill.
                """),
                "viz": {"type": "dpGrid", "a": "ABABC", "b": "BABCA", "mode": "substring"},
                "vizTitle": "Longest common substring — mismatches reset the streak to 0",
                "caption": "Unlike subsequence, a mismatch wipes the running streak. The answer is the maximum value found anywhere in the grid.",
            },
            {
                "title": "How to recognise a DP problem in the wild",
                "body": D("""
                    Reach for DP when you see these signals:

                    - The problem asks for an **optimum** — *maximum / minimum / longest / fewest / how many ways* — over a set of choices.
                    - At each step you make a **choice** (take/skip, which coin, which character) and choices interact.
                    - A brute-force recursion would **recompute** the same situation. (Draw the recursion tree — repeated nodes = DP.)
                    - The answer for size `n` can be expressed using answers for **smaller sizes**.

                    Anti-signals (probably *not* DP): you just need any one valid answer fast (greedy/BFS), or each element is independent (a simple scan).
                """),
            },
            {
                "title": "Procedure + complexity",
                "body": D("""
                    **When you blank out, run this:**

                    1. Write the **brute-force recursion** first — don't optimise yet.
                    2. Spot the **repeated subproblems** in its recursion tree → that's your signal + your state.
                    3. Name `dp[...]` in **one English sentence**.
                    4. Write the **recurrence** and **base cases**.
                    5. Add a cache (top-down) **or** flip to a bottom-up loop.
                    6. **Space-optimise** only if the recurrence looks back a fixed number of rows/cells.

                    **Complexity rule of thumb:** `time = (number of states) × (work per transition)`; `space = number of states` (minus any dimension you roll away).

                    | DP shape | States | Time | Space (optimised) |
                    |----------|--------|------|-------------------|
                    | 1D rolling (House Robber) | `n` | `O(n)` | `O(1)` |
                    | 1D table (Coin Change) | `amount` | `O(amount · coins)` | `O(amount)` |
                    | 2D grid (LCS) | `m·n` | `O(m · n)` | `O(min(m, n))` |

                    > **One paragraph to remember:** DP is recursion that refuses to re-solve the same subproblem. For any problem, write the state in one sentence, the transition that builds it from smaller states, the base cases, and where the answer lives. Derive it top-down, convert to bottom-up for speed, and only then think about shaving space.
                """),
            },
        ],
    },
    {
        "id": "strings",
        "icon": "🔤",
        "title": "How to Solve String Problems",
        "shortTitle": "Strings",
        "blurb": "A string is just an array of characters — so the same handful of techniques "
                 "(frequency counts, two pointers, sliding windows, and DP) cover almost every "
                 "string problem. Learn to map the question to the technique and you're done.",
        "sections": [
            {
                "title": "The mental model",
                "body": D("""
                    A string is an **array of characters**, so everything you know about arrays applies — plus a few string-specific habits. Almost every string problem is one of these four:

                    1. **Counting / frequency** — anagrams, "can we rearrange…", character histograms → **hash map or a size-26 array**.
                    2. **Two pointers** — palindromes, reversing, comparing from both ends → **converging pointers**.
                    3. **Sliding window** — longest/shortest substring with a property → **a moving range with running state**.
                    4. **String DP** — edit distance, longest common subsequence, matching → **a 2D table** (see the DP guide).

                    > Your first move on any string problem: ask *"am I counting characters, walking from both ends, sliding a window, or comparing two strings cell-by-cell?"* That one question picks your technique.
                """),
            },
            {
                "title": "Technique 1 — frequency counting",
                "body": D("""
                    The workhorse for anagrams, permutations, and "can these characters form X". Count occurrences in a hash map (or a fixed `int[26]` for lowercase letters — faster and O(1) space).

                    ```python
                    from collections import Counter

                    def is_anagram(s, t):
                        return Counter(s) == Counter(t)          # same multiset of chars

                    def group_anagrams(words):
                        groups = {}
                        for w in words:
                            key = tuple(sorted(w))               # anagrams share a sorted key
                            groups.setdefault(key, []).append(w)
                        return list(groups.values())
                    ```

                    > **Two canonical keys for "same letters":** the **sorted string** (`O(k log k)`) or the **26-length count signature** (`O(k)`). Both make anagrams collide in a hash map.
                """),
            },
            {
                "title": "Technique 2 — two pointers (palindromes)",
                "body": D("""
                    For symmetry problems, walk one pointer from each end toward the middle. Palindrome check: compare `s[left]` and `s[right]`, step inward, stop on the first mismatch.

                    ```python
                    def is_palindrome(s):
                        s = [c.lower() for c in s if c.isalnum()]   # clean first
                        l, r = 0, len(s) - 1
                        while l < r:
                            if s[l] != s[r]: return False
                            l += 1; r -= 1
                        return True
                    ```

                    The same two-pointer idea drives reversing words, merging, and "expand around center" for *longest palindromic substring*.
                """),
                "viz": {"type": "stringTwoPointer", "s": "A man, a plan, a canal: Panama"},
                "vizTitle": "Palindrome — compare from both ends inward",
                "caption": "After cleaning to letters/digits, the two pointers march toward the center; a single mismatch ends it. Matches turn green.",
            },
            {
                "title": "Technique 3 — fixed sliding window",
                "body": D("""
                    When the problem fixes the window *size* (e.g. "any substring of length k with all-distinct characters"), slide a window of exactly `k`: add the entering character, drop the leaving one, and keep running state (a frequency map) instead of recomputing.

                    ```python
                    def has_distinct_window(s, k):
                        freq, l = {}, 0
                        for r, ch in enumerate(s):
                            freq[ch] = freq.get(ch, 0) + 1
                            if r - l + 1 > k:                    # shrink to size k
                                freq[s[l]] -= 1
                                if freq[s[l]] == 0: del freq[s[l]]
                                l += 1
                            if r - l + 1 == k and len(freq) == k:
                                return True
                        return False
                    ```

                    The point of the window: each character enters and leaves **once**, so the whole scan is O(n) instead of O(n·k).
                """),
                "viz": {"type": "fixedWindow", "nums": [1, 2, 1, 3, 4, 2, 3], "k": 3, "distinct": True},
                "vizTitle": "Fixed window of size k — slide, don't rescan",
                "caption": "As the window slides one step, exactly one element enters and one leaves; the running state updates in O(1). Here it checks whether all k entries are distinct.",
            },
            {
                "title": "Technique 4 — variable sliding window",
                "body": D("""
                    The most powerful string technique. When you want the *longest* (or shortest) substring satisfying a property, grow the window with the right pointer and **shrink from the left only when the property breaks**.

                    *Longest substring without repeating characters:* expand `right`; if the new char is already in the window, jump `left` past its previous position. Track the best length.

                    ```python
                    def longest_unique(s):
                        last, l, best = {}, 0, 0
                        for r, ch in enumerate(s):
                            if ch in last and last[ch] >= l:
                                l = last[ch] + 1            # jump left past the duplicate
                            last[ch] = r
                            best = max(best, r - l + 1)
                        return best
                    ```

                    > **The window invariant** is the secret: define what must always be true inside the window (here: "no duplicates"), expand greedily, and shrink the moment the invariant is violated.
                """),
                "viz": {"type": "slidingWindow", "s": "abcabcbb"},
                "vizTitle": "Variable window — grow right, jump left on a repeat",
                "caption": "The window expands until a duplicate appears, then the left edge jumps just past the earlier copy — never re-scanning. The longest valid window is the answer.",
            },
            {
                "title": "Technique 5 — string DP (compare two strings)",
                "body": D("""
                    When a problem compares or transforms **two** strings — edit distance, longest common subsequence, regex/wildcard matching, interleaving — it's a 2D DP. `dp[i][j]` answers the subproblem for the first `i` chars of one string and first `j` of the other; matches extend the diagonal, mismatches take the best neighbour.

                    This is the bridge to the DP guide — the grid below is the exact same engine. If you see "minimum edits", "longest common…", or "does pattern match", reach for this table.
                """),
                "viz": {"type": "dpGrid", "a": "intention", "b": "execution", "mode": "subsequence"},
                "vizTitle": "Two-string DP — the longest common subsequence grid",
                "caption": "Each cell combines smaller subproblems: a character match extends the diagonal; a mismatch inherits the larger of up/left. The corner holds the final answer.",
            },
            {
                "title": "Pattern recognition + procedure",
                "body": D("""
                    | The problem says… | Reach for |
                    |--------------------|-----------|
                    | "anagram", "permutation", "rearrange", "same characters" | **frequency count** (Counter or `int[26]`) |
                    | "palindrome", "reverse", "from both ends" | **two pointers** |
                    | "substring of length k", "window of size k" | **fixed sliding window** |
                    | "longest/shortest substring with property", "at most k distinct" | **variable sliding window** |
                    | "edit distance", "longest common…", "does pattern match" | **2D string DP** |
                    | "prefix", "starts with", many lookups | **trie / hashing** |

                    **Procedure:**

                    1. Clarify the alphabet (lowercase only? unicode?) — it decides hash map vs `int[26]`.
                    2. Map the question to a technique using the table above.
                    3. For windows, state the **invariant** (what's always true inside the window) before coding.
                    4. Watch the edges: empty string, single char, all-same characters, case/spacing.

                    **Complexity:** counting and both window styles are **O(n)** time; sorting-based anagram keys add a `log k` per word; two-string DP is **O(m·n)**.

                    > **One paragraph to remember:** A string is an array of characters. Decide up front whether you're *counting characters*, *walking from both ends*, *sliding a window*, or *comparing two strings in a grid*. Name the window invariant, reuse running state instead of rescanning, and most string problems collapse to a clean O(n) pass.
                """),
            },
        ],
    },
    {
        "id": "arrays",
        "icon": "📊",
        "title": "Array Patterns & Techniques",
        "shortTitle": "Array Patterns",
        "blurb": "Arrays are where interviews start, and a small toolbox — hashing, two pointers, "
                 "prefix sums, sliding windows, Kadane, and binary search — solves the vast majority. "
                 "This guide teaches you to recognise which tool a problem is asking for.",
        "sections": [
            {
                "title": "The mental model — a toolbox, not a pile of tricks",
                "body": D("""
                    Most array problems are a brute-force `O(n²)` scan in disguise, and each technique is a specific way to **knock that down to O(n) or O(n log n)**. There are really only a handful of tools:

                    | Technique | Turns this… | …into this | Trigger |
                    |-----------|-------------|-----------|---------|
                    | **Hashing** | re-scanning for a value | O(1) lookup | "have I seen…", "complement", "duplicate" |
                    | **Two pointers** | nested loops on sorted data | one pass | sorted array, pair/triplet, "from both ends" |
                    | **Prefix sums** | recomputing range sums | O(1) per query | "sum of range", "subarray sums" |
                    | **Sliding window** | recomputing each window | one pass | "subarray of size k", "longest/shortest subarray" |
                    | **Kadane / running aggregate** | trying every subarray | one pass | "maximum subarray / product" |
                    | **Binary search** | linear scan of sorted data | O(log n) | sorted input, or a monotonic answer space |

                    > Your job on any array problem: figure out **which row of this table** it belongs to. The rest of this guide is one visual per row.
                """),
            },
            {
                "title": "Technique 1 — hashing for O(1) lookup (Two Sum)",
                "body": D("""
                    The space-for-time trade that shows up everywhere. Instead of re-scanning the array to find a needed value, remember what you've seen in a hash map and look it up in O(1).

                    *Two Sum:* for each `x`, the only partner is `target - x`. Keep a map of `value → index`; check it before storing the current number.

                    ```python
                    def two_sum(nums, target):
                        seen = {}
                        for i, x in enumerate(nums):
                            if target - x in seen:
                                return [seen[target - x], i]
                            seen[x] = i
                    ```

                    Same idea powers "contains duplicate", "first unique element", subarray-sum-equals-k (hashing prefix sums), and group-by problems.
                """),
                "viz": {"type": "twoSumHash", "nums": [2, 7, 11, 15], "target": 9},
                "vizTitle": "Two Sum — one pass, O(1) complement lookups",
                "caption": "For each number we ask the map 'have I seen your complement?' — an O(1) question. Storing as we go avoids reusing the same element.",
            },
            {
                "title": "Technique 2 — two pointers on sorted data",
                "body": D("""
                    On a **sorted** array, two converging pointers replace a nested loop. To find a pair summing to a target: start `L` at the smallest and `R` at the largest; if the sum is too small move `L` right, too big move `R` left.

                    ```python
                    def two_sum_sorted(nums, target):
                        l, r = 0, len(nums) - 1
                        while l < r:
                            s = nums[l] + nums[r]
                            if s == target: return [l, r]
                            if s < target: l += 1          # need a bigger sum
                            else:           r -= 1          # need a smaller sum
                    ```

                    This is the backbone of 3Sum/4Sum, container-with-most-water, merging sorted arrays, and removing duplicates in place.
                """),
                "viz": {"type": "twoPointers", "nums": [2, 7, 11, 15], "target": 18},
                "vizTitle": "Two pointers — converging on a sorted array",
                "caption": "Sortedness guarantees that moving L up only increases the sum and moving R down only decreases it — so one pass suffices, no nested loop.",
            },
            {
                "title": "Technique 3 — prefix sums (range queries in O(1))",
                "body": D("""
                    When you need the sum of many sub-ranges, precompute a running total once. Then any range sum is a single subtraction: `sum(l..r) = prefix[r] - prefix[l-1]`.

                    ```python
                    prefix = [0] * len(nums)
                    run = 0
                    for i, x in enumerate(nums):
                        run += x
                        prefix[i] = run
                    # sum of nums[l..r]:
                    range_sum = prefix[r] - (prefix[l-1] if l > 0 else 0)
                    ```

                    Combine prefix sums with a **hash map** and you get the classic "count subarrays summing to k" in O(n). The idea generalises to 2D (sub-matrix sums) and to prefix XOR / prefix product.
                """),
                "viz": {"type": "prefixSum", "nums": [3, 1, 4, 1, 5, 9, 2], "queryL": 2, "queryR": 5},
                "vizTitle": "Prefix sums — build once, then answer any range instantly",
                "caption": "The prefix row is filled in one pass. Afterwards a range sum is just prefix[R] minus prefix[L-1] — no matter how many queries you get.",
            },
            {
                "title": "Technique 4 — sliding window (fixed size)",
                "body": D("""
                    For "best subarray of size k", don't recompute each window from scratch. Slide it: add the new element, subtract the one that fell off. Each element is touched twice total → O(n).

                    ```python
                    def max_sum_window(nums, k):
                        s = sum(nums[:k]); best = s
                        for r in range(k, len(nums)):
                            s += nums[r] - nums[r - k]      # add entering, drop leaving
                            best = max(best, s)
                        return best
                    ```

                    The same machinery handles "max average subarray", "count of windows meeting a condition", and fixed-length pattern matching.
                """),
                "viz": {"type": "fixedWindow", "nums": [2, 1, 5, 1, 3, 2], "k": 3},
                "vizTitle": "Fixed window — running sum, one add and one drop per step",
                "caption": "The window sum updates in O(1) each slide. No element is ever summed twice, so the whole scan is linear.",
            },
            {
                "title": "Technique 5 — Kadane / running aggregate",
                "body": D("""
                    When you must consider *all subarrays* for a max/min, a running aggregate avoids the O(n²) blowup. Kadane's: keep the best subarray ending at the current index, and either extend it or start fresh.

                    *State (it's a tiny DP):* `cur = max(nums[i], cur + nums[i])`; the answer is the max `cur` ever reached. (Maximum-product variant tracks both a running max and min, because a negative flips them.)
                """),
                "viz": {"type": "kadane", "nums": [5, -3, 5, -2, 8, -10, 4]},
                "vizTitle": "Kadane — the running 'best ending here' aggregate",
                "caption": "Whenever the running sum would do better by restarting, it does. The maximum value it ever reaches is the answer — one pass, O(1) extra space.",
            },
            {
                "title": "Technique 6 — binary search (sorted data & answer spaces)",
                "body": D("""
                    On sorted data, halve the search space each step: `O(log n)`. The deeper skill is **binary search on the answer** — when you can ask a yes/no question that flips monotonically (e.g. "can we finish in ≤ X days?"), binary-search the smallest X that works.

                    ```python
                    def binary_search(nums, target):
                        lo, hi = 0, len(nums) - 1
                        while lo <= hi:
                            mid = lo + (hi - lo) // 2
                            if nums[mid] == target: return mid
                            if nums[mid] < target:  lo = mid + 1
                            else:                    hi = mid - 1
                        return -1
                    ```

                    > **`lo + (hi - lo) // 2`** avoids overflow and is the habit to keep. Variants: first/last occurrence, rotated-array search, "minimum capacity / speed" optimisation.
                """),
                "viz": {"type": "binarySearch", "nums": [1, 3, 5, 7, 9, 11, 13, 15], "target": 11},
                "vizTitle": "Binary search — discard half the array every step",
                "caption": "Each comparison eliminates half the remaining range, so even a million elements take ~20 steps. The dimmed cells are the discarded halves.",
            },
            {
                "title": "Technique 7 — in-place & cyclic manipulation",
                "body": D("""
                    Some array problems are about *rearranging in O(1) extra space*: reverse tricks, cyclic swaps, and index-as-hash. Rotating a matrix 90° clockwise = **transpose, then reverse each row** — all in place.

                    ```python
                    def rotate(matrix):
                        n = len(matrix)
                        for i in range(n):                       # transpose
                            for j in range(i + 1, n):
                                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
                        for row in matrix:                       # reverse each row
                            row.reverse()
                    ```

                    Related in-place ideas: Dutch-national-flag (3-way partition), moving zeroes, cyclic sort for "find the missing/duplicate number", and reversing to rotate a 1D array.
                """),
                "viz": {"type": "matrixRotate", "matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
                "vizTitle": "Rotate a matrix in place — transpose, then reverse rows",
                "caption": "No second matrix is allocated: swapping across the diagonal then reversing each row yields the 90° rotation with O(1) extra space.",
            },
            {
                "title": "Procedure + complexity cheat-sheet",
                "body": D("""
                    **When you blank out on an array problem:**

                    1. **Is the array sorted (or can sorting help)?** → two pointers or binary search.
                    2. **Am I asked about a range/subarray sum?** → prefix sums (± a hash map).
                    3. **Am I asked about a contiguous window?** → sliding window (fixed or variable).
                    4. **Am I re-scanning to find a value?** → a hash map / set for O(1) lookup.
                    5. **Max/min over all subarrays?** → Kadane / running aggregate.
                    6. **O(1) space required?** → in-place swaps, cyclic sort, index-as-hash.

                    Always sanity-check the brute force first, then pick the technique that removes the redundant work.

                    | Technique | Time | Extra space |
                    |-----------|------|-------------|
                    | Hashing | `O(n)` | `O(n)` |
                    | Two pointers | `O(n)` (`O(n log n)` if you sort) | `O(1)` |
                    | Prefix sums | `O(n)` build, `O(1)` query | `O(n)` |
                    | Sliding window | `O(n)` | `O(1)`–`O(k)` |
                    | Kadane | `O(n)` | `O(1)` |
                    | Binary search | `O(log n)` | `O(1)` |

                    > **One paragraph to remember:** Most array problems are a hidden `O(n²)` scan. Identify the redundant work, then pick the tool that removes it — hashing for repeated lookups, two pointers for sorted data, prefix sums for range queries, a sliding window for contiguous ranges, Kadane for best-subarray, and binary search for sorted or monotonic answer spaces.
                """),
            },
        ],
    },
    {
        "id": "heaps",
        "icon": "⛰️",
        "title": "Heaps & Priority Queues",
        "shortTitle": "Heaps",
        "blurb": "A heap is the data structure for 'give me the best one, fast.' It keeps the min (or max) "
                 "instantly available and updates in O(log n). Master the array trick, sift up/down, and "
                 "the killer apps — top-K and running median — all made visual.",
        "sections": [
            {
                "title": "What a heap actually is (and isn't)",
                "body": D("""
                    A **heap** is a tree that keeps the *most extreme* element — the minimum (min-heap) or maximum (max-heap) — instantly reachable at the root. It answers one question superbly: *"what's the best element right now, and let me remove it?"* — in `O(log n)` per change.

                    The only rule is the **heap property**: every parent is ≤ both its children (min-heap) — applied at *every* node.

                    > **The #1 misconception:** a heap is **not sorted**. Siblings have no order, left isn't smaller than right. The *only* guarantee is parent-vs-child. So you can grab the min in `O(1)` and pop it in `O(log n)`, but you **cannot** binary-search a heap or list it in order cheaply. If you need full ordering or arbitrary lookup, use a balanced BST instead.

                    A heap is also exactly what a **priority queue** is built on: "process items by priority, highest first" = a max-heap keyed by priority.
                """),
            },
            {
                "title": "The array trick — a tree with no pointers",
                "body": D("""
                    A heap is always a **complete binary tree** (every level full except possibly the last, filled left-to-right). That completeness lets you store it in a **flat array with no node objects at all** — the parent/child links become arithmetic:

                    ```python
                    parent(i) = (i - 1) // 2
                    left(i)   = 2 * i + 1
                    right(i)  = 2 * i + 2
                    ```

                    So the array `[1, 3, 6, 5, 9, 8]` *is* this tree:

                    ```text
                    index:  0   1   2   3   4   5
                    value:  1   3   6   5   9   8

                                  (1)              index 0  ← root = minimum
                                 /   \\
                              (3)     (6)          index 1, 2
                             /  \\     /
                          (5)  (9)  (8)            index 3, 4, 5
                    ```

                    > This is why heaps are cache-friendly and memory-light: no left/right pointers, just one contiguous array. Every operation below is really just **swapping array slots** while walking up or down using that index math.
                """),
            },
            {
                "title": "The two core operations — sift up & sift down",
                "body": D("""
                    Every heap operation is one of two "bubble" moves that restore the heap property after a change. Toggle the two modes in the visualization below.

                    **Insert (sift up).** Drop the new value at the end of the array (keeps the tree complete), then **swap it upward** while it's smaller than its parent.

                    ```python
                    def sift_up(heap, i):
                        while i > 0 and heap[i] < heap[(i - 1) // 2]:
                            par = (i - 1) // 2
                            heap[i], heap[par] = heap[par], heap[i]
                            i = par
                    ```

                    **Extract-min (sift down).** The answer is `heap[0]`. Remove it, move the **last** element into the root (keeps it complete), then **sink it down**, always swapping with the *smaller* child until it sits correctly.

                    ```python
                    def sift_down(heap, i):
                        n = len(heap)
                        while True:
                            smallest, l, r = i, 2*i + 1, 2*i + 2
                            if l < n and heap[l] < heap[smallest]: smallest = l
                            if r < n and heap[r] < heap[smallest]: smallest = r
                            if smallest == i: break
                            heap[i], heap[smallest] = heap[smallest], heap[i]
                            i = smallest
                    ```

                    > Both walk a single root-to-leaf path, whose length is the tree height `log n` → both are **O(log n)**. That's the whole engine; everything else is an application of these two.
                """),
                "viz": {"type": "heapOps", "heap": [1, 3, 6, 5, 9, 8], "value": 2},
                "vizTitle": "Insert vs Extract-Min — switch modes and press Play",
                "caption": "Insert bubbles the new value UP toward the root; extract-min moves the last element to the root and sinks it DOWN past the smaller child. Each is one path, O(log n).",
            },
            {
                "title": "Build-heap (heapify) in O(n), not O(n log n)",
                "body": D("""
                    Got a raw array and want a heap? Pushing all `n` elements one by one is `O(n log n)`. **Heapify** does better: sift *down* every node from the last parent up to the root.

                    ```python
                    def build_heap(arr):
                        for i in range(len(arr) // 2 - 1, -1, -1):   # last parent → root
                            sift_down(arr, i)
                        return arr
                    ```

                    Why is this only **O(n)**? Most nodes are near the bottom and barely move — the leaves (half the array) don't move at all, the next level moves at most one step, and so on. The weighted sum collapses to `O(n)`. Start at the *last parent* because all the leaves below it are already valid one-element heaps.
                """),
                "viz": {"type": "heapify", "array": [9, 4, 7, 1, 2, 6, 5]},
                "vizTitle": "Heapify — sink each parent, bottom-up",
                "caption": "Leaves (dimmed) are already valid heaps, so we start at the last parent and sift down toward the root. Cheap because deep nodes barely move.",
            },
            {
                "title": "Python's heapq — the practical toolkit",
                "body": D("""
                    You rarely hand-roll a heap in an interview — you use `heapq`, Python's **min-heap** on a plain list. Know these by heart:

                    ```python
                    import heapq
                    heap = []
                    heapq.heappush(heap, x)      # insert, O(log n)
                    smallest = heapq.heappop(heap)   # remove & return min, O(log n)
                    smallest = heap[0]           # peek min, O(1)
                    heapq.heapify(arr)           # build in place, O(n)
                    heapq.nlargest(k, arr)       # k largest, O(n log k)
                    ```

                    **Faking a max-heap** (heapq is min-only): push **negated** values, negate on the way out.

                    ```python
                    heapq.heappush(heap, -x)
                    largest = -heapq.heappop(heap)
                    ```

                    **Custom priority:** push **tuples** — they compare lexicographically, so put the sort key first.

                    ```python
                    heapq.heappush(pq, (priority, tie_breaker, item))
                    ```

                    > **Tie-breaker tip:** if two priorities are equal, Python compares the *next* tuple element. If that's an un-comparable object it crashes — add a unique counter as a middle element to break ties safely.
                """),
            },
            {
                "title": "Killer app #1 — Top-K with a size-K heap",
                "body": D("""
                    *"Find the k largest / k most frequent / k closest."* Sorting the whole input is `O(n log n)`. A heap does it in **`O(n log k)`** — a big win when `k` is small.

                    The trick is counter-intuitive: to find the **k largest**, keep a **min-heap of size k**. Its root is the *smallest* of your current top-k, so it's exactly the element to evict when a bigger one arrives.

                    ```python
                    def k_largest(nums, k):
                        heap = []
                        for x in nums:
                            heapq.heappush(heap, x)
                            if len(heap) > k:
                                heapq.heappop(heap)      # drop the smallest survivor
                        return heap                       # heap[0] is the k-th largest
                    ```

                    > **Why a *min*-heap for the *largest*?** Because you want O(1) access to the *weakest* member of your elite group, so you can kick it out the instant something better shows up. (Symmetrically: k *smallest* → size-k *max*-heap.) This powers *Kth Largest Element*, *Top K Frequent*, and *K Closest Points to Origin*.
                """),
                "viz": {"type": "topKHeap", "nums": [3, 2, 1, 5, 6, 4], "k": 2},
                "vizTitle": "Top-K — a size-K min-heap evicts its own smallest",
                "caption": "The heap never grows past k. Each new value pushes in; if the heap overflows, the smallest is popped. The survivors are the k largest; the root is the k-th largest.",
            },
            {
                "title": "Killer app #2 — running median with two heaps",
                "body": D("""
                    *"Median of a stream"* is the classic two-heap problem. Split the numbers into a smaller half and a larger half:

                    - a **max-heap** holds the lower half (its top = the largest of the small side),
                    - a **min-heap** holds the upper half (its top = the smallest of the large side).

                    Keep the sizes within one of each other. The two tops straddle the middle, so the median is an `O(1)` read.

                    ```python
                    low, high = [], []     # low = max-heap (store negated), high = min-heap
                    def add(x):
                        heapq.heappush(low, -x)
                        heapq.heappush(high, -heapq.heappop(low))      # push low's max into high
                        if len(high) > len(low):                       # keep low ≥ high in size
                            heapq.heappush(low, -heapq.heappop(high))
                    def median():
                        if len(low) > len(high): return -low[0]
                        return (-low[0] + high[0]) / 2
                    ```

                    > **The intuition:** you never need the *whole* sorted order — only the two elements next to the middle. Two heaps give you exactly those, each insert costing `O(log n)`. Watch the two tops in the visualization converge on the median.
                """),
                "viz": {"type": "twoHeaps", "nums": [5, 15, 1, 3, 8, 7, 9, 10]},
                "vizTitle": "Two heaps — the median lives between the two tops",
                "caption": "The max-heap (low half) and min-heap (high half) stay balanced in size. The median is read straight from their tops — O(1) — after each O(log n) insert.",
            },
            {
                "title": "When to reach for a heap — and when not to",
                "body": D("""
                    **Signals that scream 'heap':**

                    - *"k largest / smallest / most frequent / closest"* → size-k heap.
                    - *"median of a stream"*, *"balance two halves"* → two heaps.
                    - *"merge k sorted lists/arrays"* → min-heap of the k current heads.
                    - *"schedule by priority"*, *"always process the most urgent next"* → priority queue.
                    - *"repeatedly take the current min/max, then add new items"* (Dijkstra, Prim's, Huffman) → heap.

                    **Heap vs the alternatives:**

                    | Need | Use |
                    |------|-----|
                    | Repeated *get + remove* the best one | **Heap** — `O(log n)` |
                    | Just the best one *once* (no removals) | a single `min()` / `max()` scan — `O(n)` |
                    | Full sorted order, or arbitrary search | **Sorting** / **balanced BST** |
                    | Membership / dedupe | **hash set** |

                    > A heap shines when "best element" is a *moving target* — you keep pulling the extreme and feeding in new data. If you only need the answer once, don't build a heap; just scan.
                """),
            },
            {
                "title": "Procedure, complexity & common mistakes",
                "body": D("""
                    **Procedure when a problem smells like a heap:**

                    1. Decide **min-heap or max-heap** — do you repeatedly want the *smallest* or *largest*?
                    2. Decide **what to store** — raw values, or `(priority, item)` tuples?
                    3. Decide the **size** — unbounded, or capped at `k` (top-K), or two balanced heaps (median)?
                    4. Reach for `heapq` (negate for a max-heap). Don't hand-roll unless asked.

                    | Operation | Cost |
                    |-----------|------|
                    | Peek min/max (`heap[0]`) | `O(1)` |
                    | Push / pop | `O(log n)` |
                    | Build-heap (heapify) | `O(n)` |
                    | Top-K over n items | `O(n log k)` |
                    | Heapsort (pop all) | `O(n log n)` |

                    **Common mistakes that cost offers:**

                    - **Assuming a heap is sorted.** It isn't — only the root is special. No binary search, no ordered iteration.
                    - **Using a max-heap of size k for the k *largest*.** Backwards — use a *min*-heap so you can evict the weakest. (And a *max*-heap for the k *smallest*.)
                    - **Forgetting heapq is min-only.** Negate values for a max-heap.
                    - **Un-comparable tuples.** `(priority, obj)` crashes when priorities tie and `obj` can't be compared — insert a unique counter as a tie-breaker.
                    - **Building with n pushes when heapify would do.** `O(n log n)` vs `O(n)`.

                    > **One paragraph to remember:** A heap keeps the best element at the root and restores order with one `O(log n)` sift-up (insert) or sift-down (extract). Store it as an array using `(i-1)//2`, `2i+1`, `2i+2`. Use `heapq` (negate for max). When you see *k largest/smallest*, *stream median*, *merge k lists*, or *process by priority* — that's a heap.
                """),
            },
        ],
    },
]


def build():
    problems_out = []
    for p in PROBLEMS:
        files_out = []
        for f in p["files"]:
            files_out.append({
                "lang": f["lang"],
                "label": f["label"],
                "path": f["path"],
                "code": code(f["path"]),
            })
        entry = dict(p)
        entry["files"] = files_out
        # problem statement: curated override, else extracted from the source docstring/javadoc
        statement = STATEMENTS.get(p["id"]) or extract_statement(files_out)
        if statement:
            entry["statement"] = statement
        # merge in extra visualization bindings (only if not already set)
        if not entry.get("viz") and p["id"] in EXTRA_VIZ:
            entry["viz"] = EXTRA_VIZ[p["id"]]
        # merge in deep-dive walkthroughs
        if p["id"] in DEEP_DIVES:
            entry["deepDive"] = DEEP_DIVES[p["id"]]
        problems_out.append(entry)

    # counts per category
    counts = {}
    for p in problems_out:
        counts[p["category"]] = counts.get(p["category"], 0) + 1

    data = {
        "categories": CATEGORIES,
        "problems": problems_out,
        "counts": counts,
        "total": len(problems_out),
        "guides": GUIDES,
    }

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    payload = json.dumps(data, indent=2, ensure_ascii=False)
    with open(OUTPUT, "w", encoding="utf-8") as fh:
        fh.write("// AUTO-GENERATED by scripts/generate_site.py — do not edit by hand.\n")
        fh.write("// Re-run `python3 scripts/generate_site.py` after changing source files or the catalog.\n")
        fh.write("window.SITE_DATA = ")
        fh.write(payload)
        fh.write(";\n")

    print(f"Wrote {OUTPUT}")
    print(f"  {len(problems_out)} problems across {len(CATEGORIES)} categories")
    viz = sum(1 for p in problems_out if p.get("viz"))
    dd = sum(1 for p in problems_out if p.get("deepDive"))
    st = sum(1 for p in problems_out if p.get("statement"))
    print(f"  {viz} problems have interactive visualizations")
    print(f"  {dd} problems have deep-dive walkthroughs")
    print(f"  {st} problems have a full problem statement")
    gv = sum(1 for g in GUIDES for s in g.get("sections", []) if s.get("viz"))
    print(f"  {len(GUIDES)} concept guides with {gv} embedded visualizations")


if __name__ == "__main__":
    build()
