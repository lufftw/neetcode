```markdown
---
title: LeetCode Knowledge Graph Mind Map (Core Patterns → API Kernels → Problems) 🎯
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## How to use this map 📚
- **Goal**: learn *transferable kernels* (APIs) → recognize *patterns* → solve *problems*
- **Legend / tags**
  - 🔥 anchor / must-know
  - ⭐ common
  - ➕ optional / reinforcement
  - 🧩 hybrid (composition of kernels)
- **Progress tracker**
  - [ ] Do 1 problem per kernel (breadth)
  - [ ] Do 3 problems per kernel (depth)
  - [ ] Re-solve “anchor” problems from scratch under 20 minutes ⚡

## Kernel Index (the “APIs” you should internalize) 🔥
- **Core Platform Kernels (primitives)**
  - **HashMapLookup** 🔥
  - **PrefixSumRangeQuery** 🔥
  - **BinarySearchBoundary** 🔥
  - **MonotonicStack** 🔥
  - **TreeTraversalDFS / TreeTraversalBFS** 🔥
  - **GraphTraversalBFS / GraphTraversalDFS + TopologicalSort** 🔥
  - **UnionFindConnectivity** ⭐
  - **DPSequence / DPInterval** 🔥
  - **TriePrefixSearch** ⭐
- **This Map’s Implemented Kernels (expanded below)**
  - **HashMapLookup** 🔥
  - **PrefixSumRangeQuery** 🔥
  - **TwoPointersTraversal** ⭐ → read-only traversal (search/validation; shrink search space)
  - **SubstringSlidingWindow** 🔥 → contiguous substring state machine
  - **BinarySearchBoundary** 🔥 → boundary + answer-space search
  - **TreeTraversalDFS / TreeTraversalBFS** 🔥
  - **GraphTraversalBFS / GraphTraversalDFS + TopologicalSort** 🔥
  - **HeapTopK** ⭐ → top-k / kth / streaming median
  - **MergeSortedSequences** + **KWayMerge** ⭐ → merging sorted streams
  - **TwoPointerPartition (InPlaceCompaction)** ⭐ → mutation kernel (partition/compaction)
  - **MonotonicStack** ⭐
  - **UnionFindConnectivity** ⭐
  - **BacktrackingExploration** ⭐ → choose → explore → unchoose
  - **GridBFSMultiSource** ⭐ → wavefront BFS on grid
  - **FastSlowPointers** ⭐ → cycle / midpoint
  - **DPSequence / DPInterval** 🔥
  - **TriePrefixSearch** ⭐
- **Canonical compositions (combinators)**
  - **BinarySearchBoundary + FeasibilityCheck** (answer-space search) 🧩
  - **Partition + Quickselect** (selection) 🧩
  - **HeapTopK + Streaming aggregation** (running kth/median) 🧩
  - **Backtracking + Memoization/DP** (search with caching) 🧩
  - **BFS + Multi-source init** (wavefront) 🧩
  - **MergeSortedSequences + TwoPointersTraversal** (merge-like scans) 🧩
- **Planned / Backlog**
  - *(keep extending with more representative problems as you add sections)*

---

## Router (pick the kernel fast) 🧭
- | Problem signal | Route to |
  |---|---|
  | Unsorted array/string, need complement / count / frequency | **HashMapLookup** |
  | Range sum, subarray sum = K, “count of subarrays …” | **PrefixSumRangeQuery** (+ hash map) |
  | Contiguous + optimize over window (max/min/exists) | **SubstringSlidingWindow** |
  | Sorted + monotone move proves exclusion | **TwoPointersTraversal (Opposite)** |
  | In-place classify/compact/rewrite | **TwoPointerPartition (InPlaceCompaction)** |
  | “first/last”, boundary, rotated, answer feasible monotone | **BinarySearchBoundary** |
  | Tree traversal / LCA / validate BST | **TreeTraversalDFS/BFS** |
  | Graph components / shortest hops / DAG ordering | **GraphTraversalBFS/DFS + TopologicalSort** |
  | Kth/top-k/streaming median | **HeapTopK** / **Partition+Quickselect** |
  | Merge sorted streams / k lists | **MergeSortedSequences / KWayMerge** |
  | Wavefront propagation on grid | **GridBFSMultiSource** |
  | Choose/explore/unchoose; generate combinations | **BacktrackingExploration** |
  | Next greater/smaller; histogram/water trapping | **MonotonicStack** |
  | Connectivity under unions | **UnionFindConnectivity** |
  | Optimal substructure / overlapping subproblems | **DPSequence/DPInterval** |
  | Prefix search / word dictionary | **TriePrefixSearch** |

---

## Reverse Index (problems → kernels) 🔎
- | Problem | Primary kernel | Secondary kernel |
  |---|---|---|
  | [LeetCode 1](https://leetcode.com/problems/two-sum/description/)(only if sorted / after sort) |
  | [LeetCode 2](https://leetcode.com/problems/add-two-numbers/description/)
  | [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/)
  | [LeetCode 4](https://leetcode.com/problems/median-of-two-sorted-arrays/description/)(context only) |
  | [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/)
  | [LeetCode 15](https://leetcode.com/problems/3sum/description/)
  | [LeetCode 16](https://leetcode.com/problems/3sum-closest/description/)
  | [LeetCode 21](https://leetcode.com/problems/merge-two-sorted-lists/description/)
  | [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/)
  | [LeetCode 25](https://leetcode.com/problems/reverse-nodes-in-k-group/description/)
  | [LeetCode 26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/)(InPlaceCompaction) | writer |
  | [LeetCode 27](https://leetcode.com/problems/remove-element/description/)(InPlaceCompaction) | writer |
  | [LeetCode 39](https://leetcode.com/problems/combination-sum/description/)
  | [LeetCode 40](https://leetcode.com/problems/combination-sum-ii/description/)
  | [LeetCode 46](https://leetcode.com/problems/permutations/description/)[] |
  | [LeetCode 47](https://leetcode.com/problems/permutations-ii/description/)
  | [LeetCode 51](https://leetcode.com/problems/n-queens/description/)
  | [LeetCode 52](https://leetcode.com/problems/n-queens-ii/description/)
  | [LeetCode 75](https://leetcode.com/problems/sort-colors/description/)(InPlaceCompaction) | dutch flag |
  | [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/)
  | [LeetCode 77](https://leetcode.com/problems/combinations/description/)
  | [LeetCode 78](https://leetcode.com/problems/subsets/description/)
  | [LeetCode 79](https://leetcode.com/problems/word-search/description/)
  | [LeetCode 80](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/)(InPlaceCompaction) | writer |
  | [LeetCode 88](https://leetcode.com/problems/merge-sorted-array/description/)
  | [LeetCode 90](https://leetcode.com/problems/subsets-ii/description/)
  | [LeetCode 93](https://leetcode.com/problems/restore-ip-addresses/description/)
  | [LeetCode 125](https://leetcode.com/problems/valid-palindrome/description/)
  | [LeetCode 131](https://leetcode.com/problems/palindrome-partitioning/description/)
  | [LeetCode 141](https://leetcode.com/problems/linked-list-cycle/description/)
  | [LeetCode 142](https://leetcode.com/problems/linked-list-cycle-ii/description/)
  | [LeetCode 202](https://leetcode.com/problems/happy-number/description/)
  | [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/)
  | [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/)
  | [LeetCode 216](https://leetcode.com/problems/combination-sum-iii/description/)
  | [LeetCode 283](https://leetcode.com/problems/move-zeroes/description/)(InPlaceCompaction) | stable compaction |
  | [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/)
  | [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/)
  | [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/)
  | [LeetCode 680](https://leetcode.com/problems/valid-palindrome-ii/description/)
  | [LeetCode 876](https://leetcode.com/problems/hand-of-straights/description/)
  | [LeetCode 905](https://leetcode.com/problems/length-of-longest-fibonacci-subsequence/description/)(InPlaceCompaction) | two-way |
  | [LeetCode 922](https://leetcode.com/problems/possible-bipartition/description/)(InPlaceCompaction) | two-way |
  | [LeetCode 977](https://leetcode.com/problems/distinct-subsequences-ii/description/)
  | [LeetCode 994](https://leetcode.com/problems/prison-cells-after-n-days/description/)

---

## 1) Hash Map Lookup (HashMapLookup) 🔥
- **Contract (standard)**
  - **Inputs**: sequence/stream of items; key extraction; optional target/complement rule
  - **State**: `seen` (hash map / hash set), counts, last index
  - **Invariant**: `seen` reflects exactly the processed prefix; lookups query the prefix only
  - **Progress rule**: scan once; update `seen` after using it (avoid self-pair bugs)
  - **Complexity knobs**: key size / hashing; collision behavior; memory = distinct keys
  - **Common failure modes**
    - updating `seen` before checking complement (self-match)
    - forgetting duplicates semantics (store first vs last index)
- **Pseudo-signature (API surface)**
  - `hash_lookup(seq, key(x), on_hit(key)->answer, on_miss(update))`
  - Extension points: `key`, duplicate policy, value stored (count/index/list)
- **Problems**
  - 🔥 [LeetCode 1](https://leetcode.com/problems/two-sum/description/)
    - Note: Target $O(n)$; store index; check complement before insert.
- **Where this shows up at work**
  - dedupe IDs/events; frequency counting; join-like lookups in pipelines

---

## 2) Prefix Sums (PrefixSumRangeQuery) 🔥
- **Contract (standard)**
  - **Inputs**: numeric sequence; range queries or target-sum constraints
  - **State**: `prefix[i]`, or running `pref`; hash map `count[pref]`
  - **Invariant**: `pref = sum(seq[0..i])`; range sum `sum(l..r)=pref[r]-pref[l-1]`
  - **Progress rule**: accumulate once; answer queries in $O(1)$ or count via hash map
  - **Complexity knobs**: memory for prefix array vs streaming; hash map size
  - **Common failure modes**
    - off-by-one in range endpoints
    - using sliding window when negatives exist (should use prefix techniques)
- **Pseudo-signature (API surface)**
  - `prefix_sum(seq) -> prefix[]`
  - `count_subarrays(seq, target) using pref_count: count += pref_count[pref-target]`
  - Extension points: store earliest index (for longest), store counts (for number)
- **Representative problems**
  - [LeetCode 560](https://leetcode.com/problems/subarray-sum-equals-k/description/)
  - [LeetCode 525](https://leetcode.com/problems/contiguous-array/description/)
  - [LeetCode 238](https://leetcode.com/problems/product-of-array-except-self/description/)
  - [LeetCode 304](https://leetcode.com/problems/range-sum-query-2d-immutable/description/)
- **Where this shows up at work**
  - time-series rollups; cumulative metrics; anomaly detection with deltas

---

## 3) Two Pointers Traversal (TwoPointersTraversal) 👯 ⭐
- **Contract (standard)**
  - **Inputs**: read-only array/string; comparator/predicate; (often sorted or symmetric structure)
  - **State**: `L`, `R`, best answer so far; optional skipping rules
  - **Invariant**: answer lies within current search space; pointer moves never re-expand it
  - **Progress rule**: move one pointer per step based on rule ⇒ shrinks search space ⇒ terminates
  - **Complexity knobs**: sort precondition (may add $O(n \log n)$); skipping duplicates
  - **Common failure modes**
    - moving wrong pointer (breaks exclusion proof)
    - missing dedup skip loops (duplicates in output)
- **Pseudo-signatures (API surface)**
  - `two_pointers_opposite(arr, L=0, R=n-1, move_rule(state, L, R) -> (L', R'), on_answer)`
  - `two_pointer_sorted_enum(arr_sorted, i_loop, L/R inner, skip_duplicates=True)`
  - Extension points: move rule, stop condition, dedup policy, objective update

- **Mental model**: every move *proves* an excluded region can’t contain the answer

- **Subfamilies**
  - **Opposite pointers** (sorted/symmetric optimization)
    - Maximize objective
      - 🔥 [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/)(move shorter side)*
        - Each step guarantees one boundary index can be discarded because area is limited by the shorter height and width only shrinks.
        - Note: Target $O(n)$; correctness hinges on “shorter side is bottleneck”.
    - Palindrome validation
      - ⭐ [LeetCode 125](https://leetcode.com/problems/valid-palindrome/description/)
        - Each step guarantees discarded outer characters can’t affect validity because they are either matched or skipped by predicate.
      - ⭐ [LeetCode 680](https://leetcode.com/problems/valid-palindrome-ii/description/)(one skip branch)*
        - Each step guarantees at most one mismatch needs branching because only one deletion is allowed.
    - “Two Sum family”
      - Primary (unsorted): 🔥 [LeetCode 1](https://leetcode.com/problems/two-sum/description/)
      - Sorted variant: ⭐ [LeetCode 167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/)
        - Each step guarantees either `L` or `R` can be discarded because sum is monotone in each pointer on sorted input.
  - **Dedup + enumeration on sorted array**
    - 🔥 [LeetCode 15](https://leetcode.com/problems/3sum/description/)(outer i + inner L/R + skip duplicates)*
      - Each step guarantees duplicates are discarded because sorted order enables same-value skip without missing new tuples.
      - Note: Target $O(n^2)$ after sort; be precise about duplicate skipping at `i`, `L`, `R`.
    - ⭐ [LeetCode 16](https://leetcode.com/problems/3sum-closest/description/)
      - Each step guarantees a pointer move discards sums that only move farther in the monotone direction for that fixed `i`.

- **Quick invariant table**
  - | Pattern | Invariant | Typical problems |
    |---------|-----------|------------------|
    | Opposite | answer in `[L..R]` | [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/)
    | Sorted enumeration | no duplicate tuples emitted | [LeetCode 15](https://leetcode.com/problems/3sum/description/)

- **Where this shows up at work**
  - scanning sorted logs; reconciling two ordered feeds; symmetric validation in parsers

---

## 4) Sliding Window (SubstringSlidingWindow) 🪟 🔥
- **Contract (standard)**
  - **Inputs**: contiguous sequence (string/array); invariant predicate `Valid(state)`; add/remove update rules
  - **State**: counts/frequencies, `distinct_count`, `need/have`, sums, last-seen indices
  - **Invariant**: `Valid(L,R)` is maintained (or restored) by shrinking `L` after expanding `R`
  - **Progress rule**: advance `R` monotonically; advance `L` monotonically only as needed to restore `Valid` ⇒ termination
  - **Complexity knobs**: update cost of map/array; alphabet size `σ`; memory $O(σ)$ or $O(k)$
  - **Common failure modes**
    - not shrinking in a `while` loop when minimizing
    - applying sum-window with negatives (breaks monotonicity)

- **Core invariant**: maintain an invariant `Valid(L,R)`; advance `R` monotonically, and advance `L` monotonically only as needed to restore `Valid`. This monotonicity implies at most `n` increments of each pointer, hence $O(n)$ updates *assuming $O(1)$ amortized map updates*.

- **Pseudo-signature (API surface)**
  - `sliding_window(seq, on_add(x), on_remove(x), is_valid(state), on_answer(L,R,state))`
  - Extension points: validity predicate (≤K distinct / cover / sum), fixed vs variable window, answer aggregation (max/min/all)

- **State choices**
  - `last_seen_index` map (jump-L optimization)
  - `freq` map + `distinct_count`
  - `need/have` maps + `satisfied/required`
  - numeric `window_sum`

- **Pattern comparison table**
  - | Problem | Invariant | State | Window Size | Goal |
    |---------|-----------|-------|-------------|------|
    | 🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/)
    | ⭐ [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/)
    | 🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/)[c] >= need[c]` | need/have + satisfied | variable | minimize |
    | ⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/)(fixed)**: `len==|p|` and ∀c, `have[c]==need[c]` (or `matched==required` with defined criterion) | freq + matched | fixed | exists |
    | ⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/)(fixed)**: `len==|p|` and ∀c, `have[c]==need[c]` (or `matched==required`) | freq + matched | fixed | all positions |
    | 🔥 [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/)(requires all numbers non-negative; if negatives exist use prefix sums + monotone structure / binary search variants)* | sum ≥ target | integer sum | variable | minimize |

- **Patterns**
  - **Unique window** (`sliding_window_unique`)
    - Pseudo-signature: `unique_window(s) -> max_len` (extend: store indices to reconstruct substring)
    - Anchor: 🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/)(learn jump-left)==
      - Note: Target $O(n)$; ASCII vs Unicode trade-off (array[128/256] vs hashmap).
      - Each step guarantees `L..(newL-1)` is discarded because any window starting before `newL` would still contain a duplicate of `s[R]`.
  - **At most K distinct** (`sliding_window_at_most_k_distinct`)
    - Pseudo-signature: `at_most_k_distinct(s, k) -> max_len` (extend: “exactly K” via at_most(K)-at_most(K-1))
    - Anchor: 🔥 [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/)
      - Each step guarantees when invalid, advancing `L` discards prefixes that cannot become valid without removing elements (monotone distinct-count under removals).
  - **Frequency cover / exact match** (`sliding_window_freq_cover`)
    - Pseudo-signature: `min_cover(s, need) -> (L,R)` (extend: track satisfied counts)
    - Minimize cover: 🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/)
      - Note: Target $O(n)$; memory $O(σ)$; use array when alphabet bounded.
      - Each step guarantees when window covers `need`, shrinking `L` discards left chars because any larger window with same `R` is never better for “minimize”.
    - Fixed-size exact match (exists): ⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/)
      - Each step guarantees any window not of length `|p|` is discarded because exact-match predicate depends on fixed length.
    - Fixed-size exact match (collect all): ⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/)
      - Each step guarantees shifting by one discards previous start because only the current fixed window can match at that start.
  - **Cost bounded / sum constraint** (`sliding_window_cost_bounded`)
    - Pseudo-signature: `min_len_sum_at_least(nums_nonneg, target) -> min_len`
    - Anchor: 🔥 [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/)
      - Note: Requires all numbers **positive or non-negative** for correctness; if negatives exist, use **PrefixSumRangeQuery** (+ monotone deque / hashmap). Canonical “window fails” example: [LeetCode 862](https://leetcode.com/problems/find-and-replace-in-string/description/)
      - Each step guarantees once `sum >= target`, advancing `L` discards starts that only make the window longer for the same `R`.

- **Common interview pitfalls**
  - “minimize window” needs: **while valid → shrink** (not just one shrink)
  - “exact match” works best with: **fixed window** + `matched` counter

- **Where this shows up at work**
  - rate limiting (rolling windows); log/session analytics; dedupe within recent horizon

---

## 5) Binary Search Boundary (BinarySearchBoundary) 🔥
- **Contract (standard)**
  - **Inputs**: sorted array / implicit monotone predicate over index or answer-space
  - **State**: `lo`, `hi` bounds; predicate `P(mid)`; best-so-far boundary
  - **Invariant**: true region and false region remain separated by maintained bounds
  - **Progress rule**: shrink `[lo, hi]` each iteration ⇒ terminates in $O(\log n)$
  - **Complexity knobs**: predicate cost; integer overflow in mid; inclusive/exclusive boundaries
  - **Common failure modes**
    - off-by-one (wrong loop condition / return)
    - predicate not monotone (binary search invalid)

- **Templates (boundary)**
  - `first_true(lo, hi):` find smallest `i` s.t. `P(i)=true`
  - `last_true(lo, hi):` find largest `i` s.t. `P(i)=true`
  - `lower_bound(x):` first index with `A[i] >= x`
  - `upper_bound(x):` first index with `A[i] > x`

- **Templates (answer-space search)**
  - `min_x_s.t._feasible(x)` where `feasible(x)` is monotone (false...false,true...true)
  - Composition: **BinarySearchBoundary + FeasibilityCheck** 🧩

- **Representative problems**
  - [LeetCode 33](https://leetcode.com/problems/search-in-rotated-sorted-array/description/)
  - [LeetCode 34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/description/)
  - [LeetCode 153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/)
  - [LeetCode 162](https://leetcode.com/problems/find-peak-element/description/)
  - [LeetCode 875](https://leetcode.com/problems/longest-mountain-in-array/description/)
  - [LeetCode 1011](https://leetcode.com/problems/flip-binary-tree-to-match-preorder-traversal/description/)
  - 🧩 🔥 [LeetCode 4](https://leetcode.com/problems/median-of-two-sorted-arrays/description/)(partition-by-count invariant; binary search on partition index, not a merge)*
    - Note: Target $O(\log \min(m,n))$; define invariant “left partition has k elements and all left ≤ all right”.

- **Where this shows up at work**
  - tuning thresholds (SLA/SLO); capacity planning via feasibility; “first failure point” diagnostics

---

## 6) Tree Traversal (TreeTraversalDFS/BFS) 🌳 🔥
- **Contract (standard)**
  - **Inputs**: tree root; neighbor access (children)
  - **State**: recursion stack / explicit stack; (BFS) queue + level markers
  - **Invariant**: DFS: stack represents current path; BFS: queue contains frontier
  - **Progress rule**: visit each node once; push children; terminate when structure exhausted
  - **Complexity knobs**: recursion depth vs iterative; memory = height (DFS) or width (BFS)
  - **Common failure modes**
    - recursion depth overflow on skewed trees
    - missing base cases / null checks

- **Pseudo-signatures (API surface)**
  - `dfs(node, enter, exit)` / `dfs_iterative(stack, on_pop)`
  - `bfs(root, on_level(level_nodes))`
  - Extension points: preorder/inorder/postorder; accumulate path; parent pointers

- **Representative problems**
  - [LeetCode 102](https://leetcode.com/problems/binary-tree-level-order-traversal/description/)
  - [LeetCode 104](https://leetcode.com/problems/maximum-depth-of-binary-tree/description/)
  - [LeetCode 236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/description/)
  - [LeetCode 199](https://leetcode.com/problems/binary-tree-right-side-view/description/)
  - [LeetCode 98](https://leetcode.com/problems/validate-binary-search-tree/description/)

- **Where this shows up at work**
  - traversing ASTs/config trees; dependency trees; hierarchical aggregations

---

## 7) Graph Traversal + Topological Sort (GraphTraversalBFS/DFS + TopologicalSort) 🌐 🔥
- **Contract (standard)**
  - **Inputs**: graph neighbors function; start nodes; (Topo) indegree counts
  - **State**: visited set; queue/stack; (Topo) queue of indegree-0
  - **Invariant**: visited prevents reprocessing; BFS layers give shortest hops (unweighted)
  - **Progress rule**: pop frontier, push unvisited neighbors; topo removes indegree-0 nodes
  - **Complexity knobs**: adjacency representation; recursion vs stack
  - **Common failure modes**
    - forgetting visited (infinite loops)
    - topo: not decrementing indegree correctly; not checking processed count

- **Pseudo-signatures (API surface)**
  - `graph_bfs(starts, neighbors, on_visit)`
  - `graph_dfs(starts, neighbors, on_enter, on_exit)`
  - `toposort(nodes, edges) -> order or fail`
  - Extension points: multi-source init; parent tracking; component counting

- **Representative problems**
  - [LeetCode 133](https://leetcode.com/problems/clone-graph/description/)
  - [LeetCode 200](https://leetcode.com/problems/number-of-islands/description/)
  - [LeetCode 207](https://leetcode.com/problems/course-schedule/description/)
  - [LeetCode 417](https://leetcode.com/problems/pacific-atlantic-water-flow/description/)

- **Where this shows up at work**
  - dependency graphs; scheduling; reachability/impact analysis

---

## 8) Heap / Selection (HeapTopK + Quickselect) ⛰️ ⭐
- **Contract (standard)**
  - **Inputs**: iterable; comparator/key; target `k`
  - **State**: heap of size `k` (min-heap for top-k largest); or partition indices for quickselect
  - **Invariant**: heap contains current best `k` candidates; quickselect partition places pivot correctly
  - **Progress rule**: heap: push/pop maintains size `k`; quickselect: partition shrinks search side
  - **Complexity knobs**: `k`; stream vs batch; stability requirements
  - **Common failure modes**
    - wrong heap polarity (min vs max)
    - quickselect pivot choice causing worst-case

- **Pseudo-signatures (API surface)**
  - `heap_top_k(stream, k, key=None) -> items`
  - `quickselect(arr, k, key=None, randomized=True) -> kth`
  - Extension points: stable output, streaming updates, two-heaps median

- **Kth element**
  - 🧩 Quickselect / partition: 🔥 [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/)
    - Quickselect: **expected** $O(n)$ with randomization, **worst-case** $O(n^2)$; space $O(1)$ iterative (or $O(\log n)$ recursion).
    - Each step guarantees one side of the partition can be discarded because pivot is placed in its final rank position.
  - Heap alternative (especially streaming / stability): ⭐ [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/)
    - Heap: $O(n \log k)$ time; space $O(k)$.
    - Each step guarantees elements outside the size-`k` heap can be discarded because they cannot enter the top-k given current heap minimum.

- **Choose X when…**
  - **Quickselect**: batch array, in-place, expected linear; OK with worst-case risk.
  - **Heap**: streaming data or need incremental updates; simpler correctness; predictable $O(n \log k)$.

- **Where this shows up at work**
  - top-N dashboards; percentile approximations (exact kth for small data); priority scheduling queues

---

## 9) Merging Sorted Sequences (MergeSortedSequences + KWayMerge) 🔗 ⭐
- **Contract (standard)**
  - **Inputs**: sorted sequences/iterators; comparator/key; output mode (stream vs materialize)
  - **State**: two pointers (`i`,`j`) for 2-way; heap of heads for k-way; output buffer
  - **Invariant**: output prefix is globally sorted; next chosen item is smallest available head
  - **Progress rule**: advance the pointer/iterator of the chosen head; terminates after consuming all items
  - **Complexity knobs**: `k`; stability requirement; memory for output
  - **Common failure modes**
    - forgetting to advance pointer after output
    - mishandling empty lists / null heads

- **Pseudo-signatures (API surface)**
  - `merge_two(a, b, key=None) -> merged`
  - `kway_merge(iterators, key=None, stable=True, mode="stream|list")`
  - Extension points: stable tie-breaking, lazy iteration, dedup merges

- **Two sorted streams (two pointers)**
  - Linked list merge: ⭐ [LeetCode 21](https://leetcode.com/problems/merge-two-sorted-lists/description/)
    - Each step guarantees the smaller head node can be emitted because all remaining nodes in that list are ≥ its head.
  - Array merge (often from ends): ⭐ [LeetCode 88](https://leetcode.com/problems/merge-sorted-array/description/)
    - Each step guarantees placing the current max at the end is safe because it will never need to move again.
  - Merge-from-ends trick: ⭐ [LeetCode 977](https://leetcode.com/problems/distinct-subsequences-ii/description/)
    - Each step guarantees one end index can be discarded because the maximum absolute value must be at an end of a sorted array.

- **K-way merge**
  - Heap-based $O(N \log k)$: 🔥 [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/)
    - Each step guarantees the heap-min head can be output because it is the smallest among all list heads.
  - Divide-and-conquer $O(N \log k)$: 🔥 [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/)
    - Each merge step guarantees sortedness is preserved because it composes correct 2-way merges.

- **Choose X when… (Merge k lists)**
  - **Heap**: streaming incremental output; simpler implementation; stable incremental merge.
  - **Divide-and-conquer**: often better constants in batch; no heap overhead; clean recursion/iteration over pairs.

- **Where this shows up at work**
  - merging sorted event streams; index segment merges (LSM/IR systems); external sort pipelines

---

## 10) Partitioning / In-Place Compaction (TwoPointerPartition) 🚧 ⭐
- **Contract (standard)**
  - **Inputs**: mutable array; classification predicate(s); desired region order
  - **State**: region pointers (`low/mid/high` or `write/read`); optional counts
  - **Invariant**: array is divided into labeled regions with precise meanings
  - **Progress rule**: each step shrinks the unknown region; terminates when unknown is empty
  - **Complexity knobs**: stable vs unstable; number of partitions; swap cost
  - **Common failure modes**
    - wrong pointer updates after swap (especially `mid/high`)
    - assuming stability when using swaps

- **Pseudo-signatures (API surface)**
  - `writer_compact(arr, keep(x)) -> new_len` (stable)
  - `partition_2way(arr, pred) -> boundary`
  - `dutch_flag(arr, classify={0,1,2})`
  - Extension points: stability requirement; k-way generalization; in-place vs extra buffer

- **Patterns**
  - **Dutch flag (3-way partition)** (`dutch_flag_partition`)
    - Pseudo-signature: `dutch_flag(A, values={0,1,2}) -> A`
    - Region invariant:
      - `A[0..low-1] = 0`, `A[low..mid-1] = 1`, `A[mid..high] = unknown`, `A[high+1..n-1] = 2`
      - Loop: while `mid <= high`, maintain regions after each swap/update
    - Anchor: 🔥 [LeetCode 75](https://leetcode.com/problems/sort-colors/description/)
  - **Two-way partition** (`two_way_partition`)
    - ⭐ [LeetCode 905](https://leetcode.com/problems/length-of-longest-fibonacci-subsequence/description/)
    - ⭐ [LeetCode 922](https://leetcode.com/problems/possible-bipartition/description/)
  - **Writer compaction (same-direction reader/writer)**
    - Deduplicate
      - ⭐ [LeetCode 26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/)
      - ⭐ [LeetCode 80](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/)
    - Remove elements
      - ⭐ [LeetCode 27](https://leetcode.com/problems/remove-element/description/)
    - Compact / stable filtering
      - ⭐ [LeetCode 283](https://leetcode.com/problems/move-zeroes/description/)

- **Where this shows up at work**
  - compaction in ETL; stable filtering; bucketing/routing partitions

---

## 11) Fast–Slow Pointers (FastSlowPointers) 🐢🐇 ⭐
- **Contract (standard)**
  - **Inputs**: linked structure or function `f(x)` defining next; head/start
  - **State**: `slow`, `fast` pointers
  - **Invariant**: after `t` iterations, `slow` moved `t` steps, `fast` moved `2t`
  - **Progress rule**: advance slow by 1 and fast by 2; if cycle exists they must meet; else fast hits null
  - **Complexity knobs**: step function cost; loop termination conditions
  - **Common failure modes**
    - null checks for `fast` / `fast.next`
    - mixing up phase-2 reset logic

- **Two phases (Floyd)**
  - Phase 1: detect cycle
    - Correctness hook: after `t` iterations, slow moved `t`, fast moved `2t`; if a cycle exists, relative speed 1 ensures they meet inside the cycle.
  - Phase 2: find cycle start
    - Correctness hook: reset one pointer to head and move both 1 step; equal distance-to-entry modulo cycle length ⇒ meet at entry.

- **Problems**
  - Detect cycle: ⭐ [LeetCode 141](https://leetcode.com/problems/linked-list-cycle/description/)
  - Find cycle start: ⭐ [LeetCode 142](https://leetcode.com/problems/linked-list-cycle-ii/description/)
  - Implicit cycle (function iteration): ⭐ [LeetCode 202](https://leetcode.com/problems/happy-number/description/)
  - Midpoint: ⭐ [LeetCode 876](https://leetcode.com/problems/hand-of-straights/description/)

- **Where this shows up at work**
  - detecting cycles in references; iterative function systems; stream dedupe with cycle checks

---

## 12) Backtracking Exploration (BacktrackingExploration) 🧠 ⭐
- **Contract (standard)**
  - **Inputs**: choice set; constraints; goal predicate; pruning rules
  - **State**: current path; auxiliary sets (used/cols/diags); recursion depth
  - **Invariant**: state exactly matches current path (no “ghost marks”)
  - **Progress rule**: choose one option, recurse, unchoose; terminates by depth/choices exhaustion
  - **Complexity knobs**: branching factor; pruning strength; output size lower bound
  - **Common failure modes**
    - forgetting to unchoose (state leak)
    - insufficient pruning / wrong duplicate-skip level

- **Pseudo-signature (API surface)**
  - `backtrack(state, choices(state), choose, unchoose, is_solution, prune) -> outputs`
  - Extension points: duplicate handling (sort + same-level skip), memoization cache key, iterative stack

- **Core rhythm**: **Choose → Explore → Unchoose**

- **Decision-tree shapes**
  - **Permutation** (used[])
    - Time: `O(n * n!)` to output all permutations; stack `O(n)`
    - ⭐ [LeetCode 46](https://leetcode.com/problems/permutations/description/)
    - With duplicates (sort + same-level skip): ⭐ [LeetCode 47](https://leetcode.com/problems/permutations-ii/description/)
  - **Subset** (start index)
    - Time: `O(n * 2^n)`; stack `O(n)`
    - ⭐ [LeetCode 78](https://leetcode.com/problems/subsets/description/)
    - With duplicates (sort + same-level skip): ⭐ [LeetCode 90](https://leetcode.com/problems/subsets-ii/description/)
  - **Combination / fixed size** (start index + length bound)
    - ⭐ [LeetCode 77](https://leetcode.com/problems/combinations/description/)
  - **Target sum search**
    - Reuse allowed: ⭐ [LeetCode 39](https://leetcode.com/problems/combination-sum/description/)
    - No reuse + duplicates: ⭐ [LeetCode 40](https://leetcode.com/problems/combination-sum-ii/description/)
    - Fixed count + bounded domain: ⭐ [LeetCode 216](https://leetcode.com/problems/combination-sum-iii/description/)
  - **Constraint satisfaction**
    - N-Queens: exponential with strong pruning; state via `cols`, `diag1`, `diag2`
    - 🔥 [LeetCode 51](https://leetcode.com/problems/n-queens/description/)
    - ⭐ [LeetCode 52](https://leetcode.com/problems/n-queens-ii/description/)
  - **String segmentation**
    - ⭐ [LeetCode 93](https://leetcode.com/problems/restore-ip-addresses/description/)(4 segments + length bounds prune)*
    - ⭐ [LeetCode 131](https://leetcode.com/problems/palindrome-partitioning/description/)(optional DP precompute for palindrome checks)*
  - **Grid path search**
    - ⭐ [LeetCode 79](https://leetcode.com/problems/word-search/description/)(visited mark/unmark)*

- **Choose X when…**
  - recursion: simplest expression of choose/explore/unchoose
  - iterative stack: avoid recursion depth limits in some languages / huge depth constraints

- **Where this shows up at work**
  - constraint solvers; generating configurations; search with pruning in schedulers

<!-- markmap: fold -->
## 13) BFS Wavefront on Grid (GridBFSMultiSource) 🌊 ⭐
- **Contract (standard)**
  - **Inputs**: grid; neighbor function (4-neighbor or 8-neighbor as specified); multiple sources
  - **State**: queue; visited/state grid; remaining targets; time/levels counter
  - **Invariant**: queue contains current frontier; each cell is enqueued at most once
  - **Progress rule**: process BFS by levels; push valid neighbors; terminate when queue empty or goals met
  - **Complexity knobs**: neighbor degree (4 vs 8); visited representation; grid mutation vs separate visited
  - **Common failure modes**
    - not marking visited at enqueue-time (duplicate enqueues)
    - mixing level counting with per-node processing

- **Core idea**: push all sources, expand layer by layer (time = levels)
- **Model**: grid cells are vertices; edges connect 4-neighbors (or 8 if specified).
- **Complexity**: $O(R \* C)$ time and $O(R \* C)$ space in worst case (queue + visited/state); each cell is enqueued at most once.

- **Anchor**
  - 🔥 [LeetCode 994](https://leetcode.com/problems/prison-cells-after-n-days/description/)
    - Each step guarantees processed cells at minute `t` cannot be reached earlier because BFS explores in nondecreasing distance layers.
- **Engineering checklist**
  - queue init with all sources
  - count fresh/remaining targets
  - process BFS by levels to count minutes

- **Where this shows up at work**
  - multi-origin propagation (blast radius); distance-to-nearest facility; shortest hops on maps

---

## 14) Monotonic Stack (MonotonicStack) 📚 🔥
- **Contract (standard)**
  - **Inputs**: array; comparator defining monotonicity; query type (next greater/smaller)
  - **State**: stack of indices maintaining monotone property
  - **Invariant**: stack values are monotone; unresolved indices remain on stack
  - **Progress rule**: each index pushed once and popped once ⇒ $O(n)$
  - **Complexity knobs**: strict vs non-strict comparisons; direction (left/right)
  - **Common failure modes**
    - wrong comparison (>= vs >) causing duplicates bugs
    - forgetting to store indices (need distances)

- **Pseudo-signature (API surface)**
  - `mono_stack(arr, cmp, on_pop(pop_i, i), on_finish(i))`
  - Extension points: next greater, previous smaller, span/area computations

- **Representative problems**
  - [LeetCode 739](https://leetcode.com/problems/daily-temperatures/description/)
  - [LeetCode 853](https://leetcode.com/problems/most-profit-assigning-work/description/)
  - [LeetCode 84](https://leetcode.com/problems/largest-rectangle-in-histogram/description/)
  - [LeetCode 42](https://leetcode.com/problems/trapping-rain-water/description/)

- **Where this shows up at work**
  - time-to-next-event queries; envelope computations; stack-based single-pass analytics

---

## 15) Union-Find Connectivity (UnionFindConnectivity) 🧩 ⭐
- **Contract (standard)**
  - **Inputs**: elements; union operations; connectivity queries
  - **State**: `parent[]`, `rank/size[]`
  - **Invariant**: `find(x)` returns representative; union merges components
  - **Progress rule**: path compression + union by rank ⇒ near-constant amortized
  - **Complexity knobs**: number of unions/finds; mapping ids to indices
  - **Common failure modes**
    - not compressing paths; incorrect rank updates
    - forgetting to initialize all nodes

- **Pseudo-signature (API surface)**
  - `find(x)`, `union(x,y)`, `connected(x,y)`
  - Extension points: component counting, union by size, dynamic node add

- **Representative problems**
  - [LeetCode 323](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/description/)
  - [LeetCode 547](https://leetcode.com/problems/number-of-provinces/description/)
  - [LeetCode 684](https://leetcode.com/problems/redundant-connection/description/)
  - [LeetCode 721](https://leetcode.com/problems/accounts-merge/description/)

- **Where this shows up at work**
  - grouping/merging identities; network connectivity; clustering by relations

---

## 16) DP (Sequence / Interval) (DPSequence/DPInterval) 🧠 🔥
- **Contract (standard)**
  - **Inputs**: sequence/string; recurrence definition; base cases
  - **State**: `dp[i]` or `dp[i][j]`; transition rules
  - **Invariant**: dp state represents optimal/ways for a prefix/interval
  - **Progress rule**: fill in topological order of dependencies
  - **Complexity knobs**: state dimension; transition cost; memory optimization
  - **Common failure modes**
    - wrong dependency order; missing base cases
    - confusing “ways” vs “min cost” semantics

- **Pseudo-signature (API surface)**
  - `dp_sequence(n, transition(i, dp)->dp[i])`
  - `dp_interval(n, transition(l,r,dp)->dp[l][r])`
  - Extension points: reconstruct path; rolling arrays; memoization

- **Representative problems**
  - [LeetCode 70](https://leetcode.com/problems/climbing-stairs/description/)
  - [LeetCode 198](https://leetcode.com/problems/house-robber/description/)
  - [LeetCode 300](https://leetcode.com/problems/longest-increasing-subsequence/description/)
  - [LeetCode 322](https://leetcode.com/problems/coin-change/description/)
  - [LeetCode 1143](https://leetcode.com/problems/find-smallest-common-element-in-all-rows/description/)
  - [LeetCode 416](https://leetcode.com/problems/partition-equal-subset-sum/description/)

- **Where this shows up at work**
  - optimization under constraints; alignment/diff-like tasks; planning with overlapping subproblems

---

## 17) Trie / Prefix Search (TriePrefixSearch) 🔤 ⭐
- **Contract (standard)**
  - **Inputs**: strings; alphabet; operations insert/search/prefix; optional board neighbors for word search
  - **State**: trie nodes with children map/array; terminal markers
  - **Invariant**: path from root spells prefix; terminal indicates full word
  - **Progress rule**: traverse characters; create nodes as needed
  - **Complexity knobs**: alphabet size; memory; compressing nodes
  - **Common failure modes**
    - forgetting terminal flag
    - using hashmap children when alphabet small and fixed (constant factors)

- **Pseudo-signature (API surface)**
  - `insert(word)`, `search(word)`, `starts_with(prefix)`
  - Extension points: word count; delete; wildcard; compressed trie

- **Representative problems**
  - [LeetCode 208](https://leetcode.com/problems/implement-trie-prefix-tree/description/)(Prefix Tree)
  - [LeetCode 212](https://leetcode.com/problems/word-search-ii/description/)

- **Where this shows up at work**
  - autocomplete; routing by prefix; dictionary matching in parsers

---

## 18) Linked List Manipulation (pointer surgery) 🔧 ⭐
- **Contract (standard)**
  - **Inputs**: linked list head; group size / arithmetic rules
  - **State**: `prev/curr/next` pointers; dummy head; carry (for arithmetic)
  - **Invariant**: pointers maintain list connectivity; reversed segments are fully linked
  - **Progress rule**: move through nodes; reverse/connect segments; terminate at end
  - **Complexity knobs**: recursion vs iterative; extra dummy nodes
  - **Common failure modes**
    - losing next pointer (breaking list)
    - incorrect reconnection at segment boundaries

- **Pseudo-signature (API surface)**
  - `reverse_segment(head, k) -> (new_head, new_tail, next_start)`
  - Extension points: reverse between positions; reverse whole list; group reversal

- Arithmetic on lists
  - ⭐ [LeetCode 2](https://leetcode.com/problems/add-two-numbers/description/)
- In-place reversal in groups
  - 🔥 [LeetCode 25](https://leetcode.com/problems/reverse-nodes-in-k-group/description/)
    - Note: Target $O(n)$; be careful about reconnecting `prev_tail`, `new_head`, `new_tail`, `next_start`.

- **Where this shows up at work**
  - pointer-safe list transforms; streaming buffers (linked structures); in-place chunk operations

---

## Suggested Learning Paths (roadmap-style) 🚀
- **Sliding Window Mastery**
  - [ ] 🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/)
  - [ ] 🔥 [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/)
  - [ ] 🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/)
  - [ ] ⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/)
  - [ ] ⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/)
  - [ ] 🔥 [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/)
- **Two Pointers Mastery**
  - [ ] 🔥 [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/)
  - [ ] ⭐ [LeetCode 125](https://leetcode.com/problems/valid-palindrome/description/)
  - [ ] ⭐ [LeetCode 26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/)
  - [ ] 🔥 [LeetCode 15](https://leetcode.com/problems/3sum/description/)
- **Backtracking Mastery**
  - [ ] ⭐ [LeetCode 78](https://leetcode.com/problems/subsets/description/)
  - [ ] ⭐ [LeetCode 46](https://leetcode.com/problems/permutations/description/)
  - [ ] ⭐ [LeetCode 39](https://leetcode.com/problems/combination-sum/description/)
  - [ ] 🔥 [LeetCode 51](https://leetcode.com/problems/n-queens/description/)
  - [ ] ⭐ [LeetCode 79](https://leetcode.com/problems/word-search/description/)

---
```