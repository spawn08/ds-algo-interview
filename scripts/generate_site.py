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
import textwrap

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(REPO_ROOT, "docs", "data", "problems.js")


def code(path):
    """Read a source file relative to the repo root."""
    full = os.path.join(REPO_ROOT, path)
    with open(full, "r", encoding="utf-8") as fh:
        return fh.read()


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
    print(f"  {viz} problems have interactive visualizations")


if __name__ == "__main__":
    build()
