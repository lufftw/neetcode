---
title: LeetCode Knowledge Graph Mind Map (Core Patterns → API Kernels → Problems) 🎯
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## How to use this map 📚
- **Goal**: learn *transferable kernels* (APIs) → recognize *patterns* → solve *problems*
- **Legend / tags**
  - 🔥 Must-know (high frequency / anchor)
  - ⭐ Common (frequent follow-up)
  - 🧊 Nice-to-know (optional / lower ROI)
- **Progress tracker**
  - [ ] Do 1 problem per kernel (breadth)
  - [ ] Do 3 problems per kernel (depth)
  - [ ] Re-solve “anchor” problems from scratch under 20 minutes ⚡

## Kernel Index (the “APIs” you should internalize) 🔥
- 🔥 **SubstringSlidingWindow** → contiguous substring state machine
- 🔥 **TwoPointersTraversal** → coordinated pointer movement
- 🔥 **TwoPointerPartition** → in-place partitioning
- 🔥 **FastSlowPointers** → cycle / midpoint
- 🔥 **MergeSortedSequences** + **KWayMerge** → merging sorted streams
- 🔥 **BacktrackingExploration** → choose → explore → unchoose
- 🔥 **GridBFSMultiSource** → wavefront BFS on grid
- 🔥 **BinarySearchBoundary** → boundary + answer-space search
- 🔥 **HeapTopK** → top-k / kth / streaming median
- 🔥 **MonotonicStack** → next greater/smaller, histogram, water
- 🔥 **PrefixSumRangeQuery** → range sums, subarray sums
- 🔥 **UnionFindConnectivity** → connectivity / components
- 🔥 **TreeTraversalDFS/BFS** → recursive/iterative DFS, level order BFS
- 🔥 **TopologicalSort** → DAG ordering
- 🔥 **TriePrefixSearch** → prefix dictionary / multi-word search
- 🔥 **DPSequence/DPInterval** → sequence DP, interval DP
- ⭐ **HashIndexLookup** → hash map complement lookup (Two Sum default)

- **API contracts (compact)**
  - **SubstringSlidingWindow**
    - **Inputs**: sequence (string/array); contiguous window; `L,R` move forward only
    - **State**: counts/map/last-seen, counters, running sum
    - **Hooks**: `add(R)`, `remove(L)`, `is_valid()`, `record_answer(L,R)`
    - **Complexities**: $O(n)$ amortized (plus map ops); **failure modes**: `L` decreases; invalid/valid shrink direction mismatch
  - **TwoPointersTraversal**
    - **Inputs**: array/string; often sorted or symmetric; pointers move monotically
    - **State**: indices + small scalar state; sometimes writer index
    - **Hooks**: `advance_L()`, `advance_R()`, `should_move_left?`, `should_move_right?`, `record_answer()`
    - **Complexities**: $O(n)$; **failure modes**: using opposite pointers without sorted/monotone property; forgetting dedup rules
  - **TwoPointerPartition**
    - **Inputs**: mutable array; predicate / categories; swaps allowed
    - **State**: region boundaries (e.g., `low,mid,high`)
    - **Hooks**: `classify(x)`, `swap(i,j)`, `advance_region()`
    - **Complexities**: $O(n)$, $O(1)$ space; **failure modes**: broken region invariants; off-by-one at boundaries
  - **FastSlowPointers**
    - **Inputs**: linked list / function iteration `f(x)`; pointers move at 1x/2x
    - **State**: two pointers; optional visited not needed
    - **Hooks**: `step_slow()`, `step_fast()`, `meet?`, `reset_to_head()`
    - **Complexities**: $O(n)$ time, $O(1)$ space; **failure modes**: null checks; wrong phase-2 reset
  - **MergeSortedSequences**
    - **Inputs**: two sorted sequences (arrays/lists); output new or in-place (when supported)
    - **State**: i/j pointers; output pointer; sentinel/dummy head
    - **Hooks**: `pick_min(i,j)`, `append(x)`, `advance_source()`
    - **Complexities**: $O(m+n)$; **failure modes**: stability assumptions; forgetting tail append
  - **KWayMerge**
    - **Inputs**: k sorted sequences/iterators; streaming-friendly
    - **State**: min-heap of current heads (or pairwise merge recursion)
    - **Hooks**: `push(head_of_stream)`, `pop_min()`, `advance_stream(s)`
    - **Complexities**: heap $O(N\log k)$; divide&conquer $O(N\log k)$; **failure modes**: pushing nulls; comparator mistakes
  - **BacktrackingExploration**
    - **Inputs**: decision space; constraints; optional sort for dedup
    - **State**: current path + used[]/start index + constraint sets
    - **Hooks**: `choose(x)`, `is_valid()`, `explore()`, `unchoose(x)`, `record(path)`
    - **Complexities**: exponential; **failure modes**: “ghost marks” (not unchoosing), duplicate emission
  - **GridBFSMultiSource**
    - **Inputs**: grid graph; multiple sources; unweighted edges
    - **State**: queue; visited (mutate grid or separate); level counter
    - **Hooks**: `enqueue_sources()`, `neighbors(r,c)`, `mark_visited()`, `process_level()`
    - **Complexities**: $O(R\cdot C)$; **failure modes**: enqueueing same cell multiple times; wrong level counting
  - **BinarySearchBoundary**
    - **Inputs**: monotone predicate `P(x)` over index space or answer space
    - **State**: `lo,hi,mid`; predicate function
    - **Hooks**: `P(mid)`, `move_lo/hi`, `return_boundary()`
    - **Complexities**: $O(\log n)$ calls to predicate; **failure modes**: non-monotone predicate; off-by-one return
  - **HeapTopK**
    - **Inputs**: stream/array; comparator; k
    - **State**: heap size ≤ k (or two heaps for median)
    - **Hooks**: `push(x)`, `pop()`, `peek()`, `rebalance()`
    - **Complexities**: $O(n\log k)$ typical; **failure modes**: wrong heap type; k=0; overflow in comparator
  - **MonotonicStack**
    - **Inputs**: array; next-greater/smaller or span queries
    - **State**: stack of indices maintaining monotone property
    - **Hooks**: `while stack violates: pop`, `answer[popped]=i`, `push(i)`
    - **Complexities**: $O(n)$ amortized; **failure modes**: wrong strict vs non-strict monotonicity; forgetting sentinel cleanup
  - **PrefixSumRangeQuery**
    - **Inputs**: array; range queries or target-sum subarrays
    - **State**: running prefix; hash map from prefix→count/earliest index
    - **Hooks**: `pref += x`, `lookup(pref-target)`, `update_map(pref)`
    - **Complexities**: $O(n)$; **failure modes**: missing base case `pref=0`; integer overflow
  - **UnionFindConnectivity**
    - **Inputs**: elements + union operations; undirected connectivity queries
    - **State**: parent[], rank/size[]
    - **Hooks**: `find(x)`, `union(a,b)`, `connected(a,b)`
    - **Complexities**: ~amortized inverse-Ackermann; **failure modes**: forgetting path compression; wrong component count updates
  - **TreeTraversalDFS/BFS**
    - **Inputs**: tree root; recursion/stack/queue
    - **State**: stack/queue; visited not needed for trees
    - **Hooks**: `visit(node)`, `push(children)`, `record_level()`
    - **Complexities**: $O(n)$; **failure modes**: null handling; recursion depth (stack overflow)
  - **TopologicalSort**
    - **Inputs**: DAG; adjacency list; indegree
    - **State**: queue (Kahn) or visited states (DFS)
    - **Hooks**: `build_indegree()`, `enqueue_zero_indegree()`, `pop()`, `decrement_indegree()`
    - **Complexities**: $O(V+E)$; **failure modes**: cycles; missing nodes with zero outdegree
  - **TriePrefixSearch**
    - **Inputs**: dictionary of strings; prefix queries
    - **State**: trie nodes; children map/array; terminal flags
    - **Hooks**: `insert(word)`, `walk(prefix)`, `dfs_collect()`
    - **Complexities**: $O(total_chars)$ build; query $O(|prefix|)$; **failure modes**: memory blowup; wrong terminal handling
  - **DPSequence/DPInterval**
    - **Inputs**: sequence or interval `[i..j]`; recurrence
    - **State**: dp[] or dp[i][j]
    - **Hooks**: `transition()`, `base_cases()`, `iterate_order()`
    - **Complexities**: varies; **failure modes**: wrong iteration order; missing base cases

- **Chooser guide (routing layer) 🧭**
  - Contiguous subarray/substring + incremental validity ⇒ **SubstringSlidingWindow**
  - Sorted + pair/interval reasoning or symmetric scan ⇒ **TwoPointersTraversal**
  - In-place classify into regions (swaps, partition) ⇒ **TwoPointerPartition**
  - Linked-list cycle / midpoint / implicit iteration cycle ⇒ **FastSlowPointers**
  - Two sorted streams ⇒ **MergeSortedSequences**
  - K sorted streams / merge logs ⇒ **KWayMerge**
  - Minimum steps/time in unweighted grid/graph ⇒ **GridBFSMultiSource** (BFS)
  - Monotone predicate over index/answer space ⇒ **BinarySearchBoundary**
  - Kth/top-k/streaming metrics ⇒ **HeapTopK**
  - Need next-greater/smaller spans ⇒ **MonotonicStack**
  - Many subarray sums / range sums ⇒ **PrefixSumRangeQuery**
  - Connectivity under unions ⇒ **UnionFindConnectivity**
  - Tree structure ⇒ **TreeTraversalDFS/BFS**
  - DAG prerequisites/order ⇒ **TopologicalSort**
  - Prefix dictionary / multi-word search ⇒ **TriePrefixSearch**
  - Optimal substructure/overlaps ⇒ **DPSequence/DPInterval**

- **Find by domain 🗂️**
  - **Arrays/Strings** → SubstringSlidingWindow, TwoPointersTraversal, TwoPointerPartition, PrefixSumRangeQuery, MonotonicStack, BinarySearchBoundary, HeapTopK
  - **Linked Lists** → FastSlowPointers, Linked list manipulation (DummyHeadSplice / ReverseSegment / KGroupReverse)
  - **Trees** → TreeTraversalDFS/BFS, BinarySearchBoundary (BST), DP (tree DP variants)
  - **Graphs** → Grid/Graph BFS, TopologicalSort, UnionFindConnectivity
  - **Heaps / Streams** → HeapTopK, KWayMerge

- **Compositions (common kernel combos) 🧩**
  - **BinarySearchBoundary + FeasibilityCheck** (answer-space search)
  - **HeapTopK + Streaming** (median/percentiles)
  - **BacktrackingExploration + Memoization (DFS DP)** (string segmentation variants)
  - **KWayMerge + HeapTopK** (merge streams then keep top-k)
  - **BinarySearchBoundary + Merge partition-by-count** (Median of two sorted arrays)

---

## 1) Sliding Window (SubstringSlidingWindow) 🪟
- **API contract**
  - **Inputs**: string/array; contiguous window; `L` and `R` only move forward
  - **State**: `last_seen` or `freq/need/have`, counters, `window_sum`
  - **Hooks**: `add(R)`, `remove(L)`, `is_valid()`, `record_answer(L,R)`
  - **Complexities**: $O(n)$ amortized (monotone pointers); **failure modes**: `L` decreases; wrong shrink condition; missing `max()` on jump-left
- **Invariant**: maintain a predicate `Valid(L,R)` for the current window while advancing pointers monotonically.
- **Core invariant (formalized)**: Maintain an invariant predicate `Valid(L,R)` over the current window. Advance `R` monotonically; while `Valid` is violated (or while `Valid` holds for minimization problems), advance `L` monotonically restoring the invariant. **If both pointers only move forward**, each index is processed $O(1)$ times ⇒ $O(n)$ time (plus cost of map operations).
- **State choices**
  - `last_seen_index` map (jump-L optimization)
    - When doing `L = max(L, last_seen[c] + 1)`, ensure `L` never decreases; update `last_seen` after processing `R`.
  - `freq` map + `distinct_count`
  - `need/have` maps + `satisfied/required`
  - numeric `window_sum`
- **Pattern comparison table**
  - | Problem | Invariant | State | Window Size | Goal |
    |---------|-----------|-------|-------------|------|
    | 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/0003_longest_substring_without_repeating_characters/) | all unique (jump-left) | last index map | variable | maximize |
    | ⭐ [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/0340_longest_substring_with_at_most_k_distinct/) | ≤K distinct | freq map | variable | maximize |
    | 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/0076_minimum_window_substring/) | covers all required | need/have + satisfied | variable | minimize |
    | ⭐ [LeetCode 567 - Permutation in String](https://leetcode.com/problems/0567_permutation_in_string/) | exact freq match | freq + matched | fixed | exists |
    | ⭐ [LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/0438_find_all_anagrams_in_a_string/) | exact freq match | freq + matched | fixed | all positions |
    | ⭐ [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/0209_minimum_size_subarray_sum/) | sum ≥ target (monotone under nonnegativity) | integer sum | variable | minimize *(assumes nums[i] ≥ 0; negatives break shrink logic)* |
- **Template archetypes (stable entrypoints)**
  - **(1) Jump-left uniqueness** (`L = max(L, last[x]+1)`)
    - Pseudocode
      - ```text
        L = 0
        last = {}
        for R in [0..n-1]:
          if s[R] in last:
            L = max(L, last[s[R]] + 1)   # L never decreases
          last[s[R]] = R
          record_answer(L, R)
        ```
    - Anchor (🔥): [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/0003_longest_substring_without_repeating_characters/)
    - Follow-up 1 (⭐): [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/0340_longest_substring_with_at_most_k_distinct/)
    - Follow-up 2 (🧊): large alphabet/Unicode → prefer hash map; careful about per-char costs
  - **(2) While-valid shrink (minimize / enforce bound)** (`while valid: shrink`)
    - Pseudocode
      - ```text
        L = 0
        init_state()
        for R in [0..n-1]:
          add(R)
          while is_valid():      # for minimize; invert condition for "shrink until valid"
            record_answer(L, R)
            remove(L)
            L += 1
        ```
    - Anchor (🔥): [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/0076_minimum_window_substring/)
    - Follow-up 1 (⭐): [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/0209_minimum_size_subarray_sum/) *(assumes nums[i] ≥ 0; if negatives allowed use prefix sums + monotone deque / binary search variants depending on problem)*
    - Follow-up 2 (⭐): [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/0340_longest_substring_with_at_most_k_distinct/) *(freq + shrink when >K)*
  - **(3) Fixed-size rolling window (exact match / anagrams)** (`size == k`)
    - Pseudocode
      - ```text
        L = 0
        init_state_for_window()
        for R in [0..n-1]:
          add(R)
          if R - L + 1 > k:
            remove(L)
            L += 1
          if R - L + 1 == k and is_match():
            record_answer(L, R)
        ```
    - Anchor (⭐): [LeetCode 567 - Permutation in String](https://leetcode.com/problems/0567_permutation_in_string/)
    - Follow-up 1 (⭐): [LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/0438_find_all_anagrams_in_a_string/)
    - Follow-up 2 (🧊): streaming window checks → maintain `matched` counter to avoid full map compare
- **Mini decision guides**
  - `last_seen` jump-left vs `freq + shrink`
    - Use **jump-left** when the invariant is “no repeats” and you can jump directly to restore uniqueness.
    - Use **freq + shrink** when duplicates are allowed but bounded (≤K distinct / counts / sum constraints).
- **Common interview pitfalls**
  - “minimize window” needs: **while valid → shrink** (not just one shrink)
  - “exact match” works best with: **fixed window** + `matched` counter
- **Real-world mappings**
  - rate limiting windows / quota enforcement
  - log scanning for patterns / alert rules over event streams
  - fraud heuristics over recent events (rolling constraints)

---

## 2) Two Pointers Traversal (TwoPointersTraversal) 👯
- **API contract**
  - **Inputs**: array/string; often sorted/symmetric; pointers move monotonically
  - **State**: indices + small invariants; optional writer index for stable compaction
  - **Hooks**: `should_move_left/right`, `advance()`, `record_answer()`
  - **Complexities**: $O(n)$; **failure modes**: applying opposite pointers without sorted/monotone reasoning; missing dedup skip
- **Invariant**: after each pointer move, the discarded region is provably irrelevant (cannot improve feasibility/optimality under the problem’s dominance argument).
- **Mental model**: every move *proves* excluded region can’t contain the answer
- **Boundary & Non-goals**
  - Traversal moves pointers to *prove impossibility* / dominance; usually read-only or stable writes.
  - Counterexample: **Sort Colors** is not traversal; it’s **Partition** because swaps maintain 3 regions.
- **Subfamilies**
  - **Opposite pointers** (sorted/symmetric optimization)
    - Maximize objective
      - Anchor (🔥): [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/0011_container_with_most_water/) *(move shorter side)*
      - Follow-up 1 (⭐): height ties / duplicates → still safe to move either shorter side; reasoning is dominance
      - Follow-up 2 (🧊): need indices under constraints → store best pair as you go
    - Palindrome validation
      - Anchor (🔥): [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/0125_valid_palindrome/)
      - Follow-up 1 (⭐): [LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/0680_valid_palindrome_ii/) *(one skip branch)*
      - Follow-up 2 (🧊): custom normalization rules → define `next_alnum()` helper carefully
    - “Two Sum family”
      - **Two Sum (unsorted)** → default kernel is **HashIndexLookup** (hash map / complement)
        - Anchor (🔥): [LeetCode 1 - Two Sum](https://leetcode.com/problems/0001_two_sum/)
      - **Two Sum (sorted / after sort)** → opposite pointers
        - Note: sorting is $O(n\log n)$ and loses original indices unless you track them.
  - **Dedup + enumeration on sorted array**
    - Anchor (🔥): [LeetCode 15 - 3Sum](https://leetcode.com/problems/0015_3sum/) *(outer i + inner L/R + skip duplicates)*
    - Follow-up 1 (⭐): [LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/0016_3sum_closest/)
    - Follow-up 2 (🧊): general k-sum → recursion + two-pointer base case (index dedup rules)
  - **Same-direction (Reader/Writer) in-place**
    - Deduplicate
      - Anchor (⭐): [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/0026_remove_duplicates_from_sorted_array/)
      - Follow-up 1 (⭐): [LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/0080_remove_duplicates_from_sorted_array_ii/)
      - Follow-up 2 (🧊): allow up to k duplicates → parameterize write rule
    - Remove elements
      - Anchor (⭐): [LeetCode 27 - Remove Element](https://leetcode.com/problems/0027_remove_element/)
      - Follow-up 1 (🧊): stable vs unstable removal → writer pointer is stable, swap-with-end is not
    - Compact / stable filtering
      - Anchor (⭐): [LeetCode 283 - Move Zeroes](https://leetcode.com/problems/0283_move_zeroes/)
      - Follow-up 1 (🧊): stable compaction of “keep predicate” for arbitrary values
- **Quick invariant table**
  - | Pattern | Invariant | Typical problems |
    |---------|-----------|------------------|
    | Opposite (maximize) | For [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/0011_container_with_most_water/): moving the shorter side cannot improve any container that keeps the taller side as a boundary, so discarding it is safe. | [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/0011_container_with_most_water/) |
    | Opposite (palindrome) | For [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/0125_valid_palindrome/): all characters outside `[L..R]` have been validated to match (ignoring non-alphanumerics as specified). | [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/0125_valid_palindrome/) |
    | Writer | `arr[0:write]` is “kept” (stable) | [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/0026_remove_duplicates_from_sorted_array/), [LeetCode 283 - Move Zeroes](https://leetcode.com/problems/0283_move_zeroes/) |
    | Sorted enumeration | no duplicate tuples emitted | [LeetCode 15 - 3Sum](https://leetcode.com/problems/0015_3sum/) |

---

## 3) Partitioning (TwoPointerPartition) 🚧
- **API contract**
  - **Inputs**: mutable array; classification predicate/categories; swaps allowed
  - **State**: region boundaries; pivot/category function
  - **Hooks**: `classify(x)`, `swap(i,j)`, `advance pointers by region`
  - **Complexities**: $O(n)$ time, $O(1)$ space; **failure modes**: broken region invariants, infinite loop when mid not advanced
- **Invariant**: maintain region invariants (classified | unknown | classified) after every swap/advance.
- **Use when**: in-place classification into regions; often a building block for selection/sorting
- **Boundary & Non-goals**
  - Partition swaps to enforce *region invariants*; mutation is central.
  - Counterexample: **Valid Palindrome** is not partitioning; it’s traversal (no swap-based regions).
- **Canonical region invariants**
  - Dutch flag: maintain indices `(low, mid, high)` with:
    - `A[0..low-1] = 0`, `A[low..mid-1] = 1`, `A[mid..high]` unknown, `A[high+1..n-1] = 2`.
  - Two-way partition: maintain:
    - `A[0..i-1]` satisfies predicate `P`, `A[j+1..n-1]` satisfies `¬P`, `A[i..j]` unknown.
- **Patterns**
  - **Dutch flag (3-way partition)** (`dutch_flag_partition`)
    - Anchor (🔥): [LeetCode 75 - Sort Colors](https://leetcode.com/problems/0075_sort_colors/)
    - Follow-up 1 (⭐): quicksort 3-way partition (duplicates heavy)
    - Follow-up 2 (🧊): stable partition requires extra space (this kernel is not stable)
  - **Two-way partition** (`two_way_partition`)
    - Anchor (⭐): [LeetCode 905 - Sort Array By Parity](https://leetcode.com/problems/0905_sort_array_by_parity/)
    - Follow-up 1 (🧊): [LeetCode 922 - Sort Array By Parity II](https://leetcode.com/problems/0922_sort_array_by_parity_ii/) *(optional variant)*
- **Mutate/stability/edge cases (engineering)**
  - **Mutates input?** Yes (swap-based)
  - **Stable?** No (relative order not preserved)
  - **Typical time/space**: $O(n)$ / $O(1)$
  - **Edge cases**: all in one class; many equals; pointer crossing boundaries

---

## 4) Fast–Slow Pointers (FastSlowPointers) 🐢🐇
- **API contract**
  - **Inputs**: linked list head or function `f(x)` producing next state
  - **State**: `slow`, `fast` pointers; optional phase toggle
  - **Hooks**: `step_slow()`, `step_fast()`, `meet?`, `reset_to_head()`
  - **Complexities**: $O(n)$ time, $O(1)$ space; **failure modes**: null deref on `fast.next`, wrong reset logic
- **Invariant**: distance between fast and slow changes predictably (fast advances 2x), enabling cycle detection and entry recovery.
- **Two phases (Floyd)**
  - Phase 1: detect cycle
  - Phase 2: find cycle start
  - Proof nugget: At the meeting point, if the cycle length is `λ` and the distance from head to cycle entry is `μ`, then the meeting occurs after `t` steps with `t ≡ μ (mod λ)`; resetting one pointer to head and moving both 1-step preserves equal distance-to-entry, so they meet at the entry.
- **Problems**
  - Anchor (🔥) Detect cycle: [LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/0141_linked_list_cycle/)
  - Anchor (🔥) Find cycle start: [LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/0142_linked_list_cycle_ii/)
  - Follow-up 1 (⭐) Implicit cycle (function iteration): [LeetCode 202 - Happy Number](https://leetcode.com/problems/0202_happy_number/)
  - Follow-up 2 (⭐) Midpoint: [LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/0876_middle_of_the_linked_list/)
- **Real-world mappings**
  - detecting loops in pointer graphs / corrupted next pointers
  - repeated-state detection in deterministic simulations
  - finding midpoint for split/merge operations on linked structures

---

## 5) Merging Sorted Sequences (MergeSortedSequences + KWayMerge) 🔗
- **API contract**
  - **Inputs**: sorted sequences (2-way or k-way); may be arrays or linked lists
  - **State**: pointers into sources; output builder; heap for k-way
  - **Hooks**: `pick_next()`, `append(x)`, `advance(source)`
  - **Complexities**: 2-way $O(m+n)$; k-way $O(N\log k)$ (heap) or $O(N\log k)$ (divide&conquer); **failure modes**: forgetting tail; wrong comparator; stability assumptions
- **Invariant**: output is monotone; sources are advanced monotonically; for k-way, heap contains the current head of each active stream.
- **Boundary & Non-goals**
  - Merge advances across *monotonic sources* to build monotonic output.
  - Counterexample: **Median of Two Sorted Arrays** is primarily **BinarySearchBoundary** on partition, not a merge routine.
- **Two sorted streams (two pointers)**
  - Anchor (🔥) Linked list merge: [LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/0021_merge_two_sorted_lists/)
  - Follow-up 1 (⭐) Array merge (often from ends): [LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/0088_merge_sorted_array/)
  - Follow-up 2 (⭐) Merge-from-ends trick: [LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/0977_squares_of_a_sorted_array/)
- **K-way merge**
  - Anchor (🔥): [LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/0023_merge_k_sorted_lists/)
  - Heap-based $O(N \log k)$: [LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/0023_merge_k_sorted_lists/)
  - Divide-and-conquer $O(N \log k)$: [LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/0023_merge_k_sorted_lists/)
  - Mini decision guide
    - Heap: best for **streaming** / iterators; simpler incremental merge; memory $O(k)$
    - Divide&conquer: often lower constants when data is materialized; clean recursion; not streaming-friendly
- **Mutate/stability/edge cases (engineering)**
  - **Mutates input?** Linked-list merge rewires nodes (mutates list pointers); array merge may mutate destination buffer (LeetCode 88).
  - **Stable?** Yes if you tie-break consistently (`<=` from left stream first).
  - **Typical time/space**: 2-way $O(m+n)$; k-way heap $O(N\log k)$ + $O(k)$ heap
  - **Edge cases**: null lists; differing lengths; duplicates; array destination capacity (LeetCode 88)
- **Real-world mappings**
  - merging sorted logs from shards (time series)
  - LSM compaction / merge of sorted runs
  - merge of pre-sorted segments in ETL pipelines

---

<!-- markmap: fold -->
## 6) Backtracking Exploration (BacktrackingExploration) 🧠
- **API contract**
  - **Inputs**: candidate set; constraints; optional sorted input for dedup
  - **State**: `path`, `used[]`/`start`, constraint sets (cols/diags), memo (optional)
  - **Hooks**: `choose(x)`, `is_valid()`, `explore(next)`, `unchoose(x)`, `record(path)`
  - **Complexities**: exponential; **failure modes**: missing unchoose; duplicate emission without same-level skip
- **Invariant**: state exactly matches current path (no “ghost marks”)
- **Core rhythm**: **Choose → Explore → Unchoose**
- **Decision-tree shapes**
  - **Permutation** (used[])
    - Anchor (🔥): [LeetCode 46 - Permutations](https://leetcode.com/problems/0046_permutations/)
    - Follow-up 1 (⭐) With duplicates (sort + same-level skip): [LeetCode 47 - Permutations II](https://leetcode.com/problems/0047_permutations_ii/)
    - Follow-up 2 (🧊): generate next permutation iteratively (non-backtracking) when only need lexicographic next
  - **Subset** (start index)
    - Anchor (🔥): [LeetCode 78 - Subsets](https://leetcode.com/problems/0078_subsets/)
    - Follow-up 1 (⭐) With duplicates (sort + same-level skip): [LeetCode 90 - Subsets II](https://leetcode.com/problems/0090_subsets_ii/)
    - Follow-up 2 (🧊): subsets with fixed size k (combine with length bound)
  - **Combination / fixed size** (start index + length bound)
    - Anchor (⭐): [LeetCode 77 - Combinations](https://leetcode.com/problems/0077_combinations/)
    - Follow-up 1 (🧊): prune using remaining slots vs remaining candidates
  - **Target sum search**
    - Anchor (🔥) Reuse allowed: [LeetCode 39 - Combination Sum](https://leetcode.com/problems/0039_combination_sum/)
    - Follow-up 1 (⭐) No reuse + duplicates: [LeetCode 40 - Combination Sum II](https://leetcode.com/problems/0040_combination_sum_ii/)
    - Follow-up 2 (⭐) Fixed count + bounded domain: [LeetCode 216 - Combination Sum III](https://leetcode.com/problems/0216_combination_sum_iii/)
  - **Constraint satisfaction**
    - Anchor (🔥): [LeetCode 51 - N-Queens](https://leetcode.com/problems/0051_n_queens/)
    - Follow-up 1 (⭐): [LeetCode 52 - N-Queens II](https://leetcode.com/problems/0052_n_queens_ii/)
    - Follow-up 2 (🧊): bitmask optimization for columns/diagonals
  - **String segmentation**
    - Anchor (⭐): [LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/0093_restore_ip_addresses/) *(4 segments + length bounds prune)*
    - Follow-up 1 (⭐): [LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/0131_palindrome_partitioning/) *(optional DP precompute for palindrome checks)*
    - Follow-up 2 (🧊): add memoization to avoid recomputation (DFS DP composition)
  - **Grid path search**
    - Anchor (⭐): [LeetCode 79 - Word Search](https://leetcode.com/problems/0079_word_search/) *(visited mark/unmark)*
    - Follow-up 1 (🧊): multi-word search → TriePrefixSearch + DFS
- **Compositions**
  - **BacktrackingExploration + Memoization (DFS DP)** (string segmentation / repeated subproblems)
- **Real-world mappings**
  - configuration search with constraints (scheduling/placement)
  - generating candidate rules/expressions with pruning
  - test generation / combinatorial exploration under constraints

---

<!-- markmap: fold -->
## 7) BFS Wavefront (GridBFSMultiSource + Graph BFS) 🌊
- **API contract**
  - **Inputs**: unweighted grid/graph; one or multiple sources
  - **State**: queue; visited set/array or mutate grid; level counter
  - **Hooks**: `enqueue_sources()`, `pop()`, `for neighbor`, `mark_visited_on_enqueue()`, `process_level()`
  - **Complexities**: $O(V+E)$ or $O(R\cdot C)$; **failure modes**: marking visited on dequeue (duplicates), off-by-one in level/time
- **Invariant**: each node/cell is enqueued at most once (when it first becomes visited/active), and BFS layers correspond to shortest steps/time in an unweighted graph.
- **Grid BFS (multi-source)** (existing)
  - Anchor (🔥)
    - [LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/0994_rotting_oranges/)
  - Engineering checklist
    - queue init with all sources
    - count fresh/remaining targets
    - process BFS by levels to count minutes
  - Complexity
    - $O(R\cdot C)$ time, $O(R\cdot C)$ space (worst case)
- **Graph shortest path BFS (unweighted)**
  - Template note: same queue + visited; edges from adjacency list; layers = shortest path length
  - Weighted counterpoint: if edges have weights → Dijkstra (priority queue); 0/1 weights → 0/1 BFS (deque) 🧊
- **Visited representation trade-offs**
  - mutate grid to mark visited: memory-light, but changes input
  - separate visited: clearer, keeps input intact, costs memory
- **Real-world mappings**
  - network propagation / contagion simulation
  - shortest time-to-reach in grids / multi-origin distance transforms
  - broadcast radius / level-by-level processing of unweighted graphs

---

## 8) Heap / Selection (HeapTopK + Quickselect) ⛰️
- **API contract**
  - **Inputs**: array/stream; comparator; `k`
  - **State**: heap (size ≤ k) or in-place partition for quickselect
  - **Hooks**: `push/pop/peek` (heap), `partition(pivot)` (quickselect)
  - **Complexities**: heap $O(n\log k)$; quickselect expected $O(n)$; **failure modes**: wrong heap direction; mutating input unexpectedly
- **Invariant**: heap size ≤ k and contains the best-so-far elements under the chosen comparator (or for quickselect, partition invariant around pivot).
- **Kth element**
  - Anchor (🔥): [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/0215_kth_largest_element_in_an_array/)
  - Quickselect / partition: [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/0215_kth_largest_element_in_an_array/)
  - Heap alternative (especially streaming / stability): [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/0215_kth_largest_element_in_an_array/)
- **Mini decision guide**
  - Quickselect: expected $O(n)$, but **worst-case $O(n^2)$** unless using median-of-medians (worst-case $O(n)$); mutates array
  - Heap: $O(n\log k)$ time, $O(k)$ extra space; works for streaming; predictable worst-case
  - Alternative: heapify all + pop k times = $O(n + k\log n)$
- **Mutate/stability/edge cases (engineering)**
  - **Mutates input?** Quickselect: yes; heap approach: no (unless you heapify in place)
  - **Stable?** Not applicable for selection; for top-k listing, stability requires extra handling
  - **Typical time/space**: see above; hidden constants: heap ops are small but frequent
  - **Edge cases**: duplicates; k=1/n; k out of range; comparator overflow
- **Real-world mappings**
  - top-k queries / leaderboards
  - alerting thresholds (top offenders)
  - streaming analytics (heavy hitters, rolling percentiles)

---

## 9) Linked List Manipulation (pointer surgery) 🔧
- **Invariant**: after each operation, list connectivity is preserved (no lost nodes, no cycles introduced unintentionally), and all next pointers are consistent with the intended segment structure.
- **Sub-kernels (micro-templates)**
  - `DummyHeadSplice` (stable insertion/removal)
    - Template
      - ```text
        dummy.next = head
        prev = dummy
        while prev.next:
          if should_remove(prev.next):
            prev.next = prev.next.next
          else:
            prev = prev.next
        return dummy.next
        ```
  - `ReverseSegment(l, r)` (local reversal primitive)
    - Template (reverse exactly k nodes starting at `l`, return new head/tail)
      - ```text
        prev = None
        cur = l
        while cur != r:          # or for k steps
          nxt = cur.next
          cur.next = prev
          prev = cur
          cur = nxt
        # prev is new head of reversed segment
        ```
  - `KGroupReverse` built from `ReverseSegment`
    - Anchor (🔥): [LeetCode 25 - Reverse Nodes in k-Group](https://leetcode.com/problems/0025_reverse_nodes_in_k_group/)
  - `CarryPropagateAddition` for arithmetic lists
    - Anchor (⭐): [LeetCode 2 - Add Two Numbers](https://leetcode.com/problems/0002_add_two_numbers/)
- **Mutate/stability/edge cases (engineering)**
  - **Mutates input?** Yes (rewires pointers)
  - **Stable?** Relative node order is preserved unless intentionally reversed/spliced
  - **Typical time/space**: $O(n)$ time, $O(1)$ extra space
  - **Edge cases**: null head; single node; k > length; leftover group (<k) unchanged; carry at end; potential overflow in digit sums
- **Real-world mappings**
  - in-place list transforms in memory-constrained systems
  - streaming pipelines represented as linked nodes (rewiring stages)
  - undo/redo chains and segment reversals

---

<!-- markmap: fold -->
## 10) Binary Search Boundary / Answer Space (BinarySearchBoundary) 🔎
- **API contract**
  - **Inputs**: monotone predicate `P(x)` over index space or answer space
  - **State**: `lo, hi, mid`; boundary answer
  - **Hooks**: `P(mid)`, `tighten_range()`, `return_boundary(lo/hi)`
  - **Complexities**: $O(\log n)$ predicate checks; **failure modes**: predicate not monotone; wrong mid/bounds updates
- **Invariant**: maintain `P(lo)=false` and `P(hi)=true` (or the chosen variant) so the boundary remains within `[lo,hi]` until convergence.
- **Templates**
  - **First true** (`lower_bound`)
    - ```text
      lo = -1 (false), hi = n (true)
      while hi - lo > 1:
        mid = (lo + hi) // 2
        if P(mid): hi = mid
        else: lo = mid
      return hi
      ```
  - **Last true** (`upper_bound - 1`)
    - ```text
      lo = -1 (true), hi = n (false)   # inverted sentinel variant
      while hi - lo > 1:
        mid = (lo + hi) // 2
        if P(mid): lo = mid
        else: hi = mid
      return lo
      ```
  - **Binary search on answer space** (minimize feasible)
    - ```text
      lo, hi = min_answer, max_answer
      while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid): hi = mid
        else: lo = mid + 1
      return lo
      ```
- **Partition-by-count (Median of two sorted arrays)**
  - Anchor (🔥): [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/0004_median_of_two_sorted_arrays/)
  - Invariant: choose cut `i` in A and `j` in B so that `i + j = (m+n+1)/2` and `max(left parts) ≤ min(right parts)`.
- **Compositions**
  - **BinarySearchBoundary + FeasibilityCheck** (answer-space search)
- **Real-world mappings**
  - capacity planning: “minimum capacity that passes SLA” (feasible(mid))
  - tuning thresholds: smallest limit that avoids errors
  - boundary detection in monotone metrics (first time a system becomes unhealthy)

---

<!-- markmap: fold -->
## 11) Monotonic Stack (MonotonicStack) 📉
- **Invariant**: stack maintains a monotone order of values/indices, so each index is pushed and popped at most once ⇒ $O(n)$ amortized.
- **Problems (representative)**
  - 🧊 Next greater family (e.g., Next Greater Element)
  - ⭐ Daily temperatures family
  - 🔥 Largest rectangle in histogram family
  - 🔥 Trapping rain water family
- **Real-world mappings**
  - computing spans (stock span / temperature span)
  - skyline/histogram area computations
  - “next event with higher priority” over time series

---

<!-- markmap: fold -->
## 12) Prefix Sum / Range Query (PrefixSumRangeQuery) ➕
- **Invariant**: prefix sums let any range sum be expressed as `pref[r]-pref[l-1]`; for target-sum counts, map stores counts of previously seen prefix sums.
- **Problems (representative)**
  - 🔥 Subarray sum equals k family
  - 🔥 Product of array except self family
  - ⭐ Range sum query family
- **Real-world mappings**
  - analytics over time series (range totals)
  - balancing ledgers (net change over interval)
  - counting occurrences of cumulative states

---

<!-- markmap: fold -->
## 13) Union-Find Connectivity (UnionFindConnectivity) 🔗
- **Invariant**: `find(x)` returns canonical representative; union merges sets; with path compression + union by rank, operations are near-constant amortized.
- **Problems (representative)**
  - 🔥 Accounts merge family
  - ⭐ Redundant connection / cycle detection (undirected)
  - ⭐ Connected components counting
- **Real-world mappings**
  - grouping identities/entities by shared keys
  - dynamic connectivity in networks
  - clustering via merge operations

---

<!-- markmap: fold -->
## 14) Tree Traversal DFS/BFS (TreeTraversalDFS/BFS) 🌳
- **Invariant**: each node is visited exactly once (tree), work per node is $O(1)$ aside from recursion/stack overhead.
- **Problems (representative)**
  - 🔥 Level order traversal family (BFS)
  - 🔥 Diameter of binary tree family (DFS)
  - 🔥 Validate BST family (inorder / bounds)
  - ⭐ LCA family (DFS)
- **Real-world mappings**
  - traversing hierarchical org/product catalogs
  - evaluating expression trees
  - aggregations over hierarchical data

---

<!-- markmap: fold -->
## 15) Topological Sort (TopologicalSort) 🧾
- **Invariant**: nodes with indegree 0 are safe to output next; removing them decreases indegrees; if output size < V then a cycle exists.
- **Problems (representative)**
  - 🔥 Course schedule family (I/II)
  - ⭐ Build order / dependency resolution
- **Real-world mappings**
  - build systems and compilation ordering
  - scheduling jobs with prerequisites
  - package dependency resolution

---

<!-- markmap: fold -->
## 16) Trie Prefix Search (TriePrefixSearch) 🌲
- **Invariant**: trie path corresponds to prefix; terminal flags distinguish full words from prefixes.
- **Problems (representative)**
  - 🔥 Implement Trie family
  - ⭐ Word Search II family
  - ⭐ autocomplete/prefix queries family
- **Real-world mappings**
  - autocomplete / search suggestions
  - prefix routing / URL matching
  - dictionary-based filtering

---

<!-- markmap: fold -->
## 17) DP Sequence / DP Interval (DPSequence/DPInterval) 🧮
- **Invariant**: dp state captures optimal substructure; transitions only depend on smaller subproblems (respect iteration order).
- **Problems (representative)**
  - 🔥 House Robber family (DPSequence)
  - 🔥 LIS family (DPSequence)
  - 🔥 Coin Change family (DPSequence)
  - ⭐ Palindrome DP family (DPInterval)
- **Real-world mappings**
  - cost optimization over sequences (budgets, schedules)
  - edit/transform costs (strings)
  - interval planning and partition costs

---

## Suggested Learning Paths (roadmap-style) 🚀
- **Sliding Window Mastery**
  - [ ] 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/0003_longest_substring_without_repeating_characters/)
  - [ ] ⭐ [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/0340_longest_substring_with_at_most_k_distinct/)
  - [ ] 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/0076_minimum_window_substring/)
  - [ ] ⭐ [LeetCode 567 - Permutation in String](https://leetcode.com/problems/0567_permutation_in_string/)
  - [ ] ⭐ [LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/0438_find_all_anagrams_in_a_string/)
  - [ ] ⭐ [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/0209_minimum_size_subarray_sum/)
- **Two Pointers Mastery**
  - [ ] 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/0011_container_with_most_water/)
  - [ ] 🔥 [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/0125_valid_palindrome/)
  - [ ] ⭐ [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/0026_remove_duplicates_from_sorted_array/)
  - [ ] 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/0015_3sum/)
- **Backtracking Mastery**
  - [ ] 🔥 [LeetCode 78 - Subsets](https://leetcode.com/problems/0078_subsets/)
  - [ ] 🔥 [LeetCode 46 - Permutations](https://leetcode.com/problems/0046_permutations/)
  - [ ] 🔥 [LeetCode 39 - Combination Sum](https://leetcode.com/problems/0039_combination_sum/)
  - [ ] 🔥 [LeetCode 51 - N-Queens](https://leetcode.com/problems/0051_n_queens/)
  - [ ] ⭐ [LeetCode 79 - Word Search](https://leetcode.com/problems/0079_word_search/)

---