---
title: LeetCode Knowledge Graph Mind Map (Core Patterns → Kernels → Problems)
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 How to use this map (free-form, interview-oriented)
- **Legend**: 🔥 must-know · ⭐ common · 🧪 nice-to-know
- **Kernel retrofit (5 steps)**
  1) identify kernel
  2) write pre/post conditions
  3) define state ops
  4) define repair rule
  5) write 3 assertions/tests
- **Rule of thumb**: pick a *pattern* → learn its *invariant* → practice 2–5 *problems* → generalize to *kernel template*
- [ ] Do 1 easy + 2 medium per kernel before moving on
- [ ] After each problem, write: `state`, `invariant`, `when to shrink/expand`, `time/space`
- **Constraint heuristics**
  - `n ≤ 2e5` → aim $O(n)$ / $O(n \log n)$
  - `n ≤ 2e3` → $O(n^2)$ may be ok
  - `n ≤ 200` → exponential + pruning / DP often ok
- **Stop conditions**
  - can implement the kernel template from memory
  - can explain invariant + correctness (why it works)
  - can handle 2 variants without peeking

## 🧠 API Kernels (the reusable “engines”)
<!-- markmap: fold -->
- **HashMapCounting** — *frequency map patterns*
  - Mini-spec
    - Inputs: sequence / multiset of keys
    - State: `freq: key -> count`
    - Invariants: counts match current scope; never negative
    - Advance rule: update `freq[x] += 1`
    - Repair rule: if enforcing constraint (e.g., unique), decrement until valid
    - Termination: end of scan / end of scope
    - Return value: counts / derived metrics
    - Complexity envelope: $O(n)$ expected-time hash ops
    - Common failure modes: forgetting to delete 0-count keys; off-by-one on scope boundaries
- **PrefixSumRangeQuery** — *prefix sums + hash map for subarray queries*
  - Mini-spec
    - Inputs: array `nums`
    - State: running `prefix`, `map` of counts or earliest index
    - Invariants: `prefix[i] = sum(nums[:i])`; map reflects prefixes seen so far
    - Advance rule: update `prefix += nums[i]`; query/update map
    - Termination: finish scan
    - Return value: count / longest length / existence
    - Complexity envelope: $O(n)$ expected-time hash ops; worst-case can degrade with adversarial hashing
    - Common failure modes: wrong init (`map[0]=1` for counting); mixing earliest vs latest index
- **SubstringSlidingWindow** — *1D window state machine with dynamic invariants*
  - Mini-spec
    - Inputs: sequence `s`, predicate/invariant over window
    - State: `L, R`, plus `hash_map/counter`, sometimes `sum`
    - Invariants: window `[L..R]` valid iff predicate holds; `R` increases monotonically
    - Advance rule: extend `R`, update state
    - Shrink/repair rule: while invalid, increment `L` and undo state
    - Termination: `R` reaches end
    - Return value: max/min length, existence, window endpoints
    - Complexity envelope: `R` increases monotonically from `0..n-1`; `L` also increases monotonically and never exceeds `n`; total increments of `L` across the run ≤ `n` ⇒ total work $O(n)$ given $O(1)$ average updates to state
    - Common failure modes: using sliding window when predicate is non-monotone; forgetting to update answer in minimize mode
  - Notes
    - Time assumes $O(1)$ expected-time hash operations; worst-case can degrade with adversarial hashing
- **GridBFSMultiSource** — *wavefront BFS from multiple sources*
  - Mini-spec
    - Inputs: grid/graph, list of sources, neighbor function
    - State: queue, visited/dist, time/levels
    - Invariants: queue holds the current frontier (equal distance); first time visited is shortest distance
    - Advance rule: pop frontier, push unvisited neighbors
    - Termination: queue empty or target condition met
    - Return value: min time / distance grid / reachability
    - Complexity envelope: $O(V+E)$ (grid: $O(R \cdot C)$)
    - Common failure modes: mixing levels/time with steps incorrectly; re-enqueue without visited guard
- **DFSGraphGeneric** — *DFS on adjacency list graphs (non-grid)*
  - Mini-spec
    - Inputs: adjacency list `g`
    - State: recursion/stack, `visited`, optional `parent/onpath`
    - Invariants: visited prevents reprocessing; onpath supports cycle detection in directed graphs
    - Advance rule: explore neighbors
    - Termination: all reachable nodes processed
    - Return value: components, topological feasibility, traversal order
    - Complexity envelope: $O(V+E)$
    - Common failure modes: not distinguishing undirected parent edge; recursion depth limits
- **TreeTraversalDFS / TreeTraversalBFS** — *tree traversals*
  - Mini-spec
    - Inputs: `root`
    - State: recursion/stack (DFS) or queue (BFS)
    - Invariants: DFS respects chosen order; BFS processes by levels
    - Termination: null nodes processed/skipped
    - Return value: aggregated value / path results / level arrays
    - Complexity envelope: $O(n)$ time; $O(h)$ stack (DFS) or $O(w)$ queue (BFS)
    - Common failure modes: mixing path accumulation with subtree aggregation
- **BinarySearchBoundary** — *index-space boundary in sorted array*
  - Mini-spec
    - Inputs: sorted array `a`, monotone predicate over index `i`
    - State: `lo, hi`
    - Invariants: boundary lies in `[lo, hi]`
    - Advance rule: shrink interval by midpoint test
    - Termination: `lo == hi` (or `lo > hi` depending on variant)
    - Return value: boundary index (first/last true etc.)
    - Complexity envelope: $O(\log n)$
    - Common failure modes: infinite loops from wrong mid; returning wrong side
- **BinarySearchOnAnswer** — *value-space feasibility predicate*
  - Mini-spec
    - Inputs: answer range `[lo..hi]`, `feasible(x)` monotone
    - State: `lo, hi`
    - Invariants: if minimizing: feasible region is suffix/prefix monotone; answer within bounds
    - Advance rule: test `mid` and shrink by feasibility
    - Termination: `lo == hi`
    - Return value: min/max feasible answer
    - Complexity envelope: $O(\log range \cdot T(feasible))$
    - Common failure modes: feasibility not monotone; wrong bounds initialization
- **HeapTopK** — *top-k / kth / stream median*
  - Mini-spec
    - Inputs: stream / array
    - State: heap(s), size constraint `k`
    - Invariants: heap contains current best candidates; size ≤ k
    - Advance rule: push/pop to restore size invariant
    - Termination: end of stream
    - Return value: kth, top-k list, median
    - Complexity envelope: $O(n \log k)$
    - Common failure modes: wrong heap polarity; forgetting to pop when size exceeds k
- **MonotonicStack** — *next greater/smaller, histogram*
  - Mini-spec
    - Inputs: array
    - State: stack of indices
    - Invariants: stack values monotone (increasing/decreasing per problem)
    - Advance rule: while invariant violated, pop and resolve answer for popped index
    - Termination: full scan; optional flush with sentinel
    - Return value: next greater/smaller indices, max area
    - Complexity envelope: $O(n)$ (each index pushed/popped ≤ 1)
    - Common failure modes: using values instead of indices; wrong strict vs non-strict comparisons
- **TwoPointersTraversal** — *two indices under invariant-preserving rules*
  - Mini-spec
    - Inputs: array/string; sometimes requires sorted input
    - State: two pointers (`l,r` or `read,write`)
    - Invariants: search space or kept prefix satisfies property
    - Advance rule: move one pointer per rule
    - Termination: pointers cross / scan ends
    - Return value: bool / length / modified array prefix
    - Complexity envelope: $O(n)$
    - Common failure modes: breaking invariants when skipping duplicates; not updating answer before moving pointers
- **TwoPointerPartition** — *partitioning (Dutch flag, quickselect partition)*
  - Mini-spec
    - Inputs: array; pivot/partition rule
    - State: region pointers delimiting partitions
    - Invariants: regions satisfy `< pivot`, `== pivot`, `> pivot` (or 2-region)
    - Advance rule: swap/move pointers to grow correct regions
    - Termination: scan pointer passes boundary
    - Return value: partitioned array / pivot final index / kth
    - Complexity envelope: $O(n)$ per partition pass
    - Common failure modes: incorrect region boundaries; not advancing after swap
- **FastSlowPointers**
  - **FloydCycleDetection** — *cycle existence + cycle start on functional graph*
  - **RunnerMidpoint** — *midpoint / kth-from-end style on linked list*
- **MergeSortedSequences** — *merge two sorted sequences*
  - Mini-spec
    - Inputs: two sorted sequences
    - State: `i,j` (and `k` for output)
    - Invariants: output prefix is sorted and equals smallest consumed elements
    - Advance rule: take smaller head, advance pointer
    - Termination: one sequence exhausted, append remainder
    - Return value: merged sequence or in-place merged array
    - Complexity envelope: $O(m+n)$
    - Common failure modes: wrong comparator; not handling tail correctly
- **KWayMerge** — *merge K sorted sequences (heap or divide-and-conquer)*
  - Mini-spec
    - Inputs: list of K sorted sequences
    - State: heap of current heads OR pairwise merge recursion
    - Invariants: heap top is smallest remaining head
    - Advance rule: pop smallest, push next from that sequence
    - Termination: heap empty / all sequences consumed
    - Return value: merged sorted output
    - Complexity envelope: $O(N \log K)$
    - Common failure modes: pushing nulls; incorrect tie handling
- **UnionFindConnectivity** — *components / cycle detection*
- **TopologicalSort** — *DAG ordering*
- **TriePrefixSearch** — *prefix matching*
- **DP1D/2D basic (knapsack-ish, LIS-ish, grid DP)**
- **Interval DP (advanced)**

### Common kernel compositions
- `BinarySearchOnAnswer` + `PrefixSumRangeQuery` (binary search on length/value + fast range checks)
- `TriePrefixSearch` + `BacktrackingExploration` (word search / autocomplete)
- `HeapTopK` + `KWayMerge` (stream merge + maintain top-k)

---

## 🪟 Sliding Window Family: `substring_window` (Kernel: SubstringSlidingWindow) 🎯
### Kernel mini-spec (standard)
- Inputs: `s` (string/array), constraint/predicate over window
- State: `L, R`, plus `freq` / counters / `sum`
- Invariants: window `[L..R]` valid iff predicate holds; `L` and `R` are monotone increasing
- Advance rule: move `R` right by 1, update state
- Shrink/repair rule: while invalid (or while still valid for minimize), move `L` right by 1 and update state
- Termination: `R == n`
- Return value: best window endpoints / length / boolean
- Complexity envelope: $O(n)$ expected-time; relies on monotone pointers + $O(1)$ average updates
- Common failure modes: using for non-monotone predicates (negatives), forgetting to update answer at correct time

### Deterministic chooser (when to use this kernel)
- Need **contiguous** subarray/substring? → if no, this is not sliding window
- Fixed length `k`? → use **fixed-size** window mode
- Predicate monotone with expanding `R`? → use variable window with shrink-on-invalid
- Need **minimum** window that satisfies predicate? → use minimize mode (shrink-while-valid)

### ==Invariant-first thinking==
- Window `[L..R]` is valid iff **invariant holds**
- Two modes:
  - **Maximize**: expand `R`, shrink while invalid
  - **Minimize**: expand until valid, shrink while still valid

### 3-step ladder (progressive)
- 1) **Unique** (local duplicates) → add `freq` + `while freq[x]>1` repair
- 2) **At most K distinct** → add `distinct` counter + `while distinct>K` repair
- 3) **Min cover / fixed anagram match** → add `need/have` + either minimize loop or fixed-size equality checks

### Pattern comparison (cheat table)
| Pattern | Invariant | State | Window | Typical goal | Repair rule | Practice |
|---|---|---|---|---|---|---|
| sliding_window_unique | all unique | last index / freq | variable | maximize | `while freq[s[R]]>1: remove(s[L])` | 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) |
| sliding_window_at_most_k_distinct | ≤ K distinct | freq map + `distinct` | variable | maximize | `while distinct>K: remove(s[L])` | ⭐ [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) |
| sliding_window_min_cover | covers required freq | need/have maps + `formed` | variable | minimize | `while formed==required: try minimize; remove(s[L])` | 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) |
| sliding_window_fixed_anagram_match | freq equals target | freq diff / matches | fixed | exists / all | `if R-L+1>k: remove(s[L]); if R-L+1==k: check()` | ⭐ [LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py), ⭐ [LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) |
| sliding_window_cost_bounded | sum/cost constraint | integer sum | variable | minimize | `while sum>target: sum-=nums[L]; L+=1` | ⭐ [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) |
| sliding_window_fixed_size | fixed length `k` | rolling state | fixed | aggregate/stat | `if R-L+1==k: update ans; slide L++` | *(template mode; no problem pinned here in this subset)* |

### Core problems (source of truth: table above)
- Use the **Practice** column in the cheat table.

### Boundary rule (Sliding Window vs Prefix Sum)
- Sliding window when predicate is monotone with window growth (often non-negative costs).
- Prefix sums when you need arbitrary sums / negatives / exact counts.

---

## 👉 Two Pointers Family (Kernel: TwoPointersTraversal) ⚡
### Kernel mini-spec (standard)
- Inputs: array/string; sometimes requires sorted input
- State: pointers `(l,r)` or `(read,write)`, optional invariants (kept prefix, remaining search space)
- Invariants: answer/search space remains within pointer-defined region; or `arr[:write]` is “kept/clean”
- Advance rule: move one pointer per local comparison / writer rule
- Termination: pointers cross or scan ends
- Return value: boolean / max metric / modified prefix length
- Complexity envelope: typically $O(n)$
- Common failure modes: forgetting sorted precondition; incorrect duplicate skipping; off-by-one when updating answer

### Pattern comparison
| Sub-pattern | Pointer init | Invariant | Time | Practice |
|---|---|---|---|---|
| Opposite pointers | `l=0, r=n-1` | answer lies within `[l,r]` | $O(n)$ | 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py), ⭐ [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py), ⭐ [LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py), 🔥 [LeetCode 167 - Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/) |
| Same-direction writer | `write=0`, `read` scans | `arr[:write]` is “kept/clean” | $O(n)$ | 🔥 [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py), ⭐ [LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py), ⭐ [LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py), ⭐ [LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py) |
| Dedup enumeration (k-sum core) | sort + fixed `i` + `(l,r)` | **Precondition**: input sorted. **Uniqueness contract**: skip duplicates deterministically so each tuple emitted once. | $O(n^2)$ | 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py), ⭐ [LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py), [LeetCode 18 - 4Sum](https://leetcode.com/problems/4sum/description/) |
| Merge (2 sorted) | `i,j` forward | output is sorted prefix | $O(m+n)$ | *(see `🔗 Merge Sorted Family` → `MergeSortedSequences` kernel)* |

### Chooser rubric: sliding window vs two pointers
- Sliding window: contiguous range + maintain a *window state* with shrink/expand.
- Two pointers: can *discard one side deterministically* based on local comparison (or compact in-place).
- Two pointers on sorted: pair search / dedup enumeration relies on sorted order invariants.
- If decision depends on a mid/global predicate → prefer binary search (boundary/answer).
- If array is circular, pointers often move with `i = (i+1) % n` (modular indexing); ensure termination by counting steps.

### Opposite pointers (search / maximize / palindrome)
- **two_pointer_opposite_maximize**
  - [ ] 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - [ ] ⭐ [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
  - [ ] ⭐ [LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
- **two_pointer_opposite_search (sorted pair search)**
  - [ ] 🔥 [LeetCode 167 - Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/) *(canonical “sorted pair search”)*

### Same-direction writer (in-place array modification)
- **two_pointer_writer_dedup**
  - [ ] 🔥 [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [ ] ⭐ [LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
- **two_pointer_writer_remove/compact**
  - [ ] ⭐ [LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - [ ] ⭐ [LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)

### Multi-sum enumeration (sort + two pointers)
- **two_pointer_three_sum**
  - [ ] 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
  - [ ] ⭐ [LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
  - [ ] [LeetCode 18 - 4Sum](https://leetcode.com/problems/4sum/description/) *(related; if in your full set)*

---

## 🐢🐇 Fast–Slow Pointers (Kernels: FloydCycleDetection, RunnerMidpoint) 🔥
### FloydCycleDetection: two-phase mental model
- Phase 1: detect cycle (tortoise/hare meet) in a **functional graph** (each node has out-degree ≤ 1)
- Phase 2: find cycle start (reset one pointer to head)
  - Let μ = distance head→cycle start, λ = cycle length. At meeting, moving one pointer to head and then advancing both by 1 keeps them synchronized to meet at cycle start after μ steps.

### RunnerMidpoint: mental model
- `slow` moves 1, `fast` moves 2 → when `fast` hits end, `slow` is at midpoint (or lower/upper mid by convention)

### Practice ladder
- [ ] 🔥 [LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py) *(cycle detect)*
- [ ] 🔥 [LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py) *(cycle start)*
- [ ] ⭐ [LeetCode 202 - Happy Number](https://leetcode.com/problems/happy-number/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py) *(implicit cycle)*
- [ ] ⭐ [LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py) *(midpoint)*

---

## 🧩 Backtracking (Kernel: BacktrackingExploration) 📚
### Kernel mini-spec (standard)
- Inputs: choices/candidates, constraints, goal condition
- State: `path`, `used[]` / `start_index`, plus constraint trackers
- Invariants: **State consistency** — after returning from recursion, state must be exactly restored
- Advance rule: `choose(option)` then recurse
- Repair/prune rule: `prune(state)` early
- Termination: `is_goal(state)` or no candidates
- Return value: all solutions / count / best
- Complexity envelope: typically exponential; depends on branching + depth
- Common failure modes: forgetting to unchoose; aliasing mutable state across branches
- Aux space: recursion depth $O(depth)$ plus state structures (`used[]`, `path`)

### Standard signature (pluggable engine)
- `candidates(state)`
- `choose(option)`
- `unchoose(option)`
- `is_goal(state)`
- `prune(state)`

### 5 decision-tree shapes (use the right “state handle”)
- **Permutation** → `used[]`
  - [ ] 🔥 [LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
  - [ ] ⭐ [LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py) *(dedup: sort + same-level skip via `used[i-1]==False`)*
- **Subset** → `start_index`
  - [ ] 🔥 [LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
  - [ ] ⭐ [LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py) *(dedup: sort + same-level skip `i>start && nums[i]==nums[i-1]`)*
- **Combination / fixed size** → `start_index` + `len(path)==k`
  - [ ] ⭐ [LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py) *(sorted early break)*
  - [ ] 🔥 [LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py) *(reuse allowed: recurse with `i`)*
  - [ ] ⭐ [LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py) *(no reuse: recurse with `i+1` + dedup)*
  - [ ] ⭐ [LeetCode 216 - Combination Sum III](https://leetcode.com/problems/combination-sum-iii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py) *(fixed count + bounded range)*
- **Constraint satisfaction / placement**
  - [ ] 🔥 [LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
  - [ ] ⭐ [LeetCode 52 - N-Queens II](https://leetcode.com/problems/n-queens-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)
  - [ ] ⭐ [LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)
  - [ ] ⭐ [LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)
  - [ ] ⭐ [LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)

### Backtracking “toolbelt”
- **Pruning**
  - feasibility bound (not enough remaining choices)
  - target bound (`remaining < 0`)
  - sorted early exit (`candidates[i] > remaining → break`)
- **Dedup strategies**
  - sort + same-level skip (subset/combination)
  - sort + `used`-based skip (permutation)
- If subproblems repeat with same parameters → add memo (top-down DP).

---

## 🌊 Graph Wavefront BFS (Kernel: GridBFSMultiSource) 🎯
### Kernel mini-spec (standard)
- Inputs: grid, sources, neighbor function
- State: `queue`, `visited/dist`, `time/levels`
- Invariants: queue stores the current frontier of equal distance (level); first visit is shortest
- Advance rule: pop a cell; push valid unvisited neighbors; when processing by levels, increment `time`
- Termination: queue empty (or all targets processed)
- Return value: min time, dist grid, reachability mask
- Complexity envelope: $O(R \cdot C)$ time, $O(R \cdot C)$ space
- Common failure modes: off-by-one in time; forgetting multi-source initialization

### Domain → graph checklist
- Identify **nodes** (cells/states), **edges** (legal moves), **sources**, and what a “minute/step” means (one BFS level).

### Real-world analogs
- cache warm-up / invalidation wavefront
- infection/alert propagation across a network
- rollout radius / TTL expansion by hops

### grid_bfs_propagation
- Multi-source BFS = enqueue all sources first, expand level by level

### Practice
- [ ] 🔥 [LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

## 🔗 Merge Sorted Family
### Merge 2 sorted (Kernel: MergeSortedSequences)
- [ ] 🔥 [LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
- [ ] ⭐ [LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
- [ ] ⭐ [LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

### Merge K sorted (Kernel: KWayMerge)
- **merge_k_sorted_heap**: $O(N \log K)$
- **merge_k_sorted_divide**: $O(N \log K)$
- Two implementations: heap-based or divide-and-conquer pairwise merge
- [ ] 🔥 [LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - [ ] ⭐ [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

## 🎛️ Partitioning & Selection (Kernel: TwoPointerPartition / HeapTopK)
### Partitioning
- **two_way_partition**
  - [ ] ⭐ [LeetCode 905 - Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
  - [ ] ⭐ [LeetCode 922 - Sort Array By Parity II](https://leetcode.com/problems/sort-array-by-parity-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
- **dutch_flag_partition**
  - [ ] 🔥 [LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
- **quickselect_partition**
  - [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

### Heap alternative for kth/top-k (Kernel: HeapTopK)
- **heap_kth_element**
  - [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) *(compare: quickselect avg $O(n)$ vs heap $O(n\log k)$)*

### Chooser (heap vs partition)
- need streaming / online → heap
- need in-place, average linear, single query → quickselect
- need worst-case guarantees → heap (or introselect note)

---

## 📚 Monotonic Stack Family (Kernel: MonotonicStack)
### Kernel mini-spec (standard)
- Inputs: array `a`
- State: stack of indices
- Invariants: stack indices represent a monotone sequence of values (increasing or decreasing)
- Advance rule: for each `i`, while invariant violated, pop `j` and finalize answer for `j`
- Termination: scan completes; optionally push sentinel to flush
- Return value: next greater/smaller arrays, or max area/width
- Complexity envelope: $O(n)$ time; $O(n)$ stack
- Common failure modes: wrong strictness (`<` vs `<=`), forgetting sentinel/flush, storing values not indices

### Sub-patterns
- **next_greater_element / next_smaller_element**
- **histogram_max_rectangle**

### Practice (representative)
- *(not pinned to this subset of auto-linked problems; add your own monotonic-stack staples as needed)*

---

## 🧮 Prefix Sum + Hash Map Family (Kernel: PrefixSumRangeQuery)
### Kernel mini-spec (standard)
- Inputs: `nums`
- State: `prefix`, `map` of counts or earliest index
- Invariants: map reflects prefixes before current index; `prefix` is running sum
- Advance rule: update `prefix`, query map for needed prior prefix, then update map
- Termination: end of array
- Return value: count / longest length / existence
- Complexity envelope: $O(n)$ expected-time hash ops
- Common failure modes: forgetting `map[0]` bootstrap; updating map before querying

### Template (two common modes)
- running prefix: `prefix += nums[i]`
- map:
  - counting: `count[prefix] += 1`
  - longest: store earliest index `first_idx[prefix]`
- when it beats sliding window: negatives present; exact sums/counts; non-monotone predicates

### Sub-patterns
- **prefix_sum_hash_count** (subarray sum equals k)
- **prefix_sum_hash_longest** (longest subarray with property)

---

## 🔎 Binary Search Family (Kernels: BinarySearchBoundary, BinarySearchOnAnswer)
### 5-line template (minimize first feasible)
```python
lo, hi = ...
while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid): hi = mid
    else: lo = mid + 1
return lo
```

### Rule boundary (two pointers vs binary search)
- If you can discard one side deterministically based on local comparison → two pointers.
- If decision depends on a mid/global predicate (feasible/threshold) → binary search.

---

## 🧭 Roadmap Anchors (from your graph)
- **NeetCode 150**: 🔥 [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), 2, 3, 4, 11, 15, 21, 23, 25, 26, 27, 39, 40, 46, 51, 75, 76, 78, 79, 80, 88, 90, 125, 131, 141, 142, 202, 209, 215, 283, 438, 567, 680, 876, 905, 922, 977, 994
- **Blind 75** (subset present): 🔥 [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), 3, 11, 15, 21, 23, 26, 39, 75, 76, 79, 125, 141, 142, 215, 994
- Note on **[LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)**: canonical kernel is **HashLookupComplement** (hash-based). Two pointers works only after sorting and changes output constraints.
- **High-frequency patterns not yet covered in this map**: monotonic stack (section added, but no pinned problems), prefix sum + hash (section added), binary search boundary/on-answer (template added), topological sort, union find, trie, DP basics.

---

## ✅ Quick “next 10 problems” playlist (balanced)
- [ ] 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
- [ ] 🔥 [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
- [ ] 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- [ ] 🔥 [LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
- [ ] 🔥 [LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
- [ ] 🔥 [LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
- [ ] 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
- [ ] 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- [ ] 🔥 [LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)