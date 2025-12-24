---
title: LeetCode Knowledge Graph Mind Map (Core Patterns → Kernels → Problems)
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 How to use this map (free-form, interview-oriented)
- **Rule of thumb**: pick a *pattern* → learn its *invariant* → practice 2–5 *problems* → generalize to *kernel template*
- [ ] Do 1 easy + 2 medium per kernel before moving on
- [ ] After each problem, write: `state`, `invariant`, `when to shrink/expand`, `time/space`
- **Legend**: 🔥 must-know · ✅ should-know · 🧪 nice-to-know

### Decision guide (router)
- **Array/string scan**
  - need “best subarray/substring under constraint” → `SubstringSlidingWindow`
  - need “pair/tuple with structure” → `TwoPointersTraversal` (often after sort)
  - has **negatives** and needs subarray sum/count → `PrefixSumRangeQuery` (+ hash map)
- **Sorted / answer is a boundary / monotone predicate** → `BinarySearchBoundary` (incl. “binary search on answer space”)
- **kth / top-k / streaming** → `HeapTopK` (online) vs `TwoPointerPartition` / quickselect (offline, mutates)
- **Unweighted shortest steps / propagation / “minutes”** → `MultiSourceBFSWavefront`
- **Dynamic connectivity** (components, cycle in undirected graph) → `UnionFindConnectivity`
- **Enumerate / find one / optimize combinatorial choices** → `BacktrackingExploration`
- **Next greater/smaller / range boundaries** → `MonotonicStack`
- **DAG ordering / prerequisites** → `TopologicalSort`

---

## 🧠 API Kernels (the reusable “engines”)
<!-- markmap: fold -->
### Kernels (callable templates)
- **HashMapIndexing** — *O(1) avg lookup for “last seen / count / complement”*
  - Contract
    - Inputs: stream/array/string items; queries like `need = target - x`
    - State: `dict` mapping key → index/value/count
    - Invariant: map reflects processed prefix exactly
    - Progress rule: process next item, update/query map
    - Termination: end of input or early return when match found
    - Complexities: $O(n)$ time avg, $O(n)$ space
    - Common failure modes: overwrite order bugs (need before put); duplicate handling (Two Sum); key normalization (case/non-alnum)
  - Dependencies: `dict` / `Counter`
  - Bug sources & readability: name `seen`, `count`; update order explicit; avoid premature micro-opts
- **TwoPointersTraversal** — *two indices under invariant-preserving rules (search/scan/dedup)*
  - Contract
    - Inputs: array/string; often sorted for elimination arguments
    - State: indices `l,r` or `read,write`, plus optional accumulators
    - Invariant: depends on sub-pattern (search elimination, palindrome checked prefix/suffix, writer prefix valid)
    - Progress rule: move one pointer monotonically based on comparison/predicate
    - Termination: pointers cross / `read==n` / match found
    - Complexities: $O(n)$ typical; with sort pre-step total becomes $O(n\log n)$
    - Common failure modes: wrong move direction; duplicate skipping incorrect; off-by-one on crossing
  - Dependencies: sorting (optional), predicate/compare
  - Bug sources & readability: standardize `l,r,read,write`; isolate “advance past duplicates” helper; call out when to avoid (unsorted/no elimination)
- **SubstringSlidingWindow** — *1D window state machine with dynamic invariants*
  - Contract
    - Inputs: string/array; constraints on window validity
    - State: `L,R`, `Counter/map`, sometimes `sum`
    - Invariant: window validity predicate (pattern-specific)
    - Progress rule: advance `R`; while invalid, advance `L` and update state
    - Termination: `R` reaches end
    - Complexities: amortized $O(n)$: `L` and `R` advance monotonically; total increments ≤ $n$ each
    - Common failure modes: shrink condition inverted; forgetting to decrement/remove; wrong “record answer” timing; off-by-one window length
  - Dependencies: `Counter/map`; sometimes `PrefixSumRangeQuery`, `MonotonicDeque`
  - Bug sources & readability: helper hooks `add/remove/is_invalid/record`; name `L,R`; ensure multiplicity logic in freq-cover
- **PrefixSumRangeQuery** — *prefix sums + hash map for subarray queries*
  - Contract
    - Inputs: array; queries about subarray sum/count
    - State: `prefix`, `freq_map[prefix_value]`
    - Invariant: `freq_map` counts prefix sums of processed prefix
    - Progress rule: update `prefix += x`; query map for needed prior prefixes; then increment `freq_map[prefix]`
    - Termination: end of array
    - Complexities: $O(n)$ time avg, $O(n)$ space
    - Common failure modes: forgetting `freq_map[0]=1`; update order (count before insert); int overflow (non-Python)
  - Dependencies: `dict` / `defaultdict(int)`
  - Bug sources & readability: define `prefix`; comment “count prior prefixes then add current”
- **BinarySearchBoundary** — *first/last true, binary search on answer*
  - Contract
    - Inputs: monotone predicate over index or value space
    - State: `lo, hi, mid`
    - Invariant: search space maintained so boundary remains inside
    - Progress rule: update `lo/hi` based on `predicate(mid)`
    - Termination: `lo == hi` (or `lo+1==hi` variant)
    - Complexities: $O(\log n)$
    - Common failure modes: infinite loop (mid bias); wrong invariant on inclusive bounds; predicate not monotone
  - Dependencies: predicate function
  - Bug sources & readability: use “first true” / “last true” named template; choose `mid = (lo+hi)//2` vs upper-mid deliberately
- **HeapTopK** — *top-k / kth (single heap)*
  - Contract
    - Inputs: iterable/stream; need top-k or kth element
    - State: min-heap of size ≤ k (or max-heap via negation)
    - Invariant: heap holds current best k elements
    - Progress rule: push; if size > k pop
    - Termination: end of stream
    - Complexities: $O(n\log k)$ time, $O(k)$ space
    - Common failure modes: wrong heap polarity; k=0 edge; forgetting to cap size
  - Dependencies: heap/priority queue
  - Bug sources & readability: wrap push-pop; name `min_heap`; avoid quickselect if streaming needed
- **DualHeapMedian** — *stream median via two heaps with balance invariant*
  - Contract
    - Inputs: stream of numbers; need median after each insertion
    - State: `low` (max-heap), `high` (min-heap)
    - Invariant: `len(low)` == `len(high)` or +1; all `low` ≤ all `high`
    - Progress rule: insert then rebalance and fix ordering
    - Termination: stream ends / query anytime
    - Complexities: $O(\log n)$ per insert, $O(n)$ space
    - Common failure modes: rebalance order wrong; median definition (even count)
  - Dependencies: two heaps
  - Bug sources & readability: separate `add_num()` and `rebalance()`
- **MergeSortedSequences** — *merge two sorted sequences*
  - Contract
    - Inputs: two sorted sequences/iterators
    - State: indices `i,j` (or node pointers), output buffer
    - Invariant: output is sorted merge of consumed prefixes
    - Progress rule: advance pointer that provides next smallest
    - Termination: one exhausted; append remainder
    - Complexities: $O(m+n)$ time, $O(1)$ extra for linked list / $O(m+n)$ for new array
    - Common failure modes: forgetting tail append; stable ordering expectation
  - Dependencies: two-pointer compare
  - Bug sources & readability: unify “take smaller then advance” helper
- **KWayMerge** — *merge K sorted sequences (heap or divide-and-conquer)*
  - Contract
    - Inputs: list of sorted sequences/lists
    - State: min-heap of current heads (heap impl) OR recursion stack (divide-and-conquer)
    - Invariant: heap contains next candidate from each active list
    - Progress rule: pop smallest; push next from same list
    - Termination: heap empty / all lists exhausted
    - Complexities: $O(N\log K)$ time, $O(K)$ space (heap)
    - Common failure modes: forgetting list index; pushing null nodes; comparator mistakes
  - Dependencies: heap; MergeSortedSequences (for batching)
  - Bug sources & readability: store `(val, list_id, node/ref)` tuples
- **TwoPointerPartition** — *in-place rearrangement via partition invariants*
  - Contract
    - Inputs: array; predicate or pivot/categories
    - State: pointers (`low, mid, high`) or (`i,j`) and pivot
    - Invariant: partition regions already satisfy category constraints
    - Progress rule: swap into correct region; move pointers
    - Termination: pointers cross / mid > high
    - Complexities: $O(n)$ time, $O(1)$ space
    - Common failure modes: pointer increment order; swapping then advancing wrong pointer; pivot edge cases
  - Dependencies: swap, comparisons
  - Bug sources & readability: comment region boundaries explicitly; avoid if stability required
- **MonotonicStack** — *next greater/smaller, histogram*
  - Contract
    - Inputs: array of values; need nearest greater/smaller boundaries
    - State: stack of indices (monotone increasing/decreasing by value)
    - Invariant: stack indices are monotonic in value; unresolved positions remain on stack
    - Progress rule: while current breaks monotonicity, pop and resolve; then push current
    - Termination: end; pop remaining (resolve with sentinel)
    - Complexities: amortized $O(n)$ time, $O(n)$ space
    - Common failure modes: using values vs indices; wrong strictness (`<` vs `<=`); missing sentinel flush
  - Dependencies: stack
  - Bug sources & readability: name `st`; comment “st holds increasing indices”
- **FastSlowPointers** — *Floyd cycle + midpoint*
  - Contract
    - Inputs: functional graph `next = f(x)` (linked list is special case)
    - State: `slow`, `fast`
    - Invariant: once in cycle, distance(fast, slow) increases by 1 mod cycle length each step ⇒ eventual meeting
    - Progress rule: advance `slow=1`, `fast=2` (or variant)
    - Termination: meet (cycle) or `fast` hits null (no cycle)
    - Complexities: $O(n)$ time, $O(1)$ space
    - Common failure modes: null checks; resetting pointer wrong in phase 2
  - Dependencies: pointer/next function
  - Bug sources & readability: separate phase1/phase2; helper `advance(node, k)`
- **BacktrackingExploration** — *Choose → Explore → Unchoose decision tree*
  - Contract
    - Inputs: candidate set + constraints; optional target objective
    - State: `path`, `used[]/start_index`, constraint trackers
    - Invariant: state reflects exactly the current partial solution
    - Progress rule: iterate choices; `choose`; recurse; `unchoose`
    - Termination: leaf reached (emit) or early exit or bound prunes
    - Complexities: exponential worst-case; pruning changes effective branching
    - Common failure modes: not restoring state; shared mutable refs; wrong dedup level
  - Dependencies: recursion/stack; set/bitmask; pruning checks
  - Bug sources & readability: implement `choose/unchoose/is_valid/emit/prune` hooks; avoid premature micro-opts
- **MultiSourceBFSWavefront** — *wavefront BFS from multiple sources (grid is a specialization)*
  - Contract
    - Inputs: implicit/explicit unweighted graph; multiple start nodes
    - State: queue (frontier), visited, distance/time counter
    - Invariant: queue holds exactly the current frontier; nodes dequeued in nondecreasing distance
    - Progress rule: pop frontier; push unvisited neighbors; advance time per level
    - Termination: queue empty or target reached
    - Complexities: $O(V+E)$ (grid: $O(R\cdot C)$)
    - Common failure modes: marking visited too late; mixing levels; re-enqueue duplicates
  - Dependencies: queue/deque; visited representation
  - Bug sources & readability: process by `for _ in range(len(q))` for levels; encode coords consistently
- **UnionFindConnectivity** — *components / cycle detection*
  - Contract
    - Inputs: edges/unions over `n` items
    - State: `parent[]`, `rank[]/size[]`
    - Invariant: each set represented by root; `find(x)` returns root
    - Progress rule: `union(a,b)` merges roots; path compression on find
    - Termination: all unions processed / query anytime
    - Complexities: near $O(1)$ amortized (inverse Ackermann), $O(n)$ space
    - Common failure modes: forgetting path compression; union by rank wrong; 0/1-index mismatch
  - Dependencies: arrays
  - Bug sources & readability: keep `find` iterative/recursive clean; comment “union returns whether merged”
- **TopologicalSort** — *DAG ordering*
  - Contract
    - Inputs: directed graph; need order or cycle detection
    - State: indegree[] + queue (Kahn) OR color/visited + stack (DFS)
    - Invariant: Kahn queue holds zero-indegree nodes; DFS postorder emits reverse finishing times
    - Progress rule: remove node, decrement indegrees; or DFS neighbors then append
    - Termination: processed count == V (acyclic) else cycle exists
    - Complexities: $O(V+E)$ time, $O(V)$ space
    - Common failure modes: missing nodes with 0 outdegree; incorrect indegree init; recursion depth
  - Dependencies: adjacency list; queue/stack
  - Bug sources & readability: track processed count; explicit cycle check
- **TriePrefixSearch** — *prefix matching*
  - Contract
    - Inputs: words/strings
    - State: trie nodes with `children`, `is_end`
    - Invariant: path from root spells prefix
    - Progress rule: `insert`, `search`, `startsWith`; optional DFS enumerate
    - Termination: end of word/prefix; enumeration ends when children exhausted
    - Complexities: $O(L)$ per op (L=word length)
    - Common failure modes: forgetting end marker; memory blowup on large alphabets
  - Dependencies: node structure (dict/array children)
  - Bug sources & readability: define `Node(children,is_end)`; keep ops symmetric

### Domains / meta-techniques (topic umbrellas, not single engines)
- Tree traversal & tree DP (split below in kernels when expanded): `TreeDFSRecursion`, `TreeBFSLevelOrder`, `TreeDPPostorder`
- DP family: `DP1DLinear`, `DP2DGrid`, `DPInterval`, `DPKnapsackSubsetSum`

### Kernel composition examples
- `BacktrackingExploration + TriePrefixSearch` (Word Search II style)
- `BinarySearchBoundary + Greedy/HeapTopK` (min feasible capacity / scheduling feasibility)
- `PrefixSumRangeQuery + monotonic deque` (shortest subarray ≥ K)

---

## Hash Map Indexing Family (Kernel: HashMapIndexing)
### Dependencies
- `dict` / `Counter`

### Ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] 🔥 [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
- Core (medium)
  - [ ] ✅ [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) *(also Sliding Window)*
- Stretch (hard)
  - [ ] 🧪 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) *(also Sliding Window freq-cover)*

### Common failure modes (runbook)
- Using “two pointers” for [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py) without sorted input (default is hash map)
- Insert-before-check vs check-before-insert (duplicate handling)
- Forgetting to normalize keys (case/whitespace) when problem implies it

---

## Two Pointers Family (Kernel: TwoPointersTraversal)
### Dependencies
- optional sort (`$O(n\log n)$` pre-step), predicate/compare, constant extra state

### Pattern comparison
| Sub-pattern (pattern id) | Pointer init | Invariant | Time | Practice |
|---|---|---|---|---|
| Opposite pointers maximize (`two_pointer_opposite_maximize`) | `l=0, r=n-1` | **Elimination**: after moving the shorter side, no optimal solution using the discarded index exists | $O(n)$ | 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py) |
| Sorted pair search (`two_pointer_sorted_pair_search`) | `l=0, r=n-1` | If `nums[l]+nums[r] < t`, then any pair with this `l` is too small ⇒ `l++`; if `> t`, any pair with this `r` is too large ⇒ `r--` | $O(n)$ | ✅ [LeetCode 167 - Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/) |
| Palindrome check (`two_pointer_opposite_palindrome`) | `l=0, r=n-1` | `s[0:l)` and `s(r:n]` already validated; pointers converge | $O(n)$ | ✅ [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py), ✅ [LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py) |
| Same-direction writer (`two_pointer_same_direction`) | `write=0`, `read` scans | `[0:write)` satisfies predicate (“kept/clean”); `[write:read)` unprocessed | $O(n)$ | 🔥 [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py), ✅ [LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py), ✅ [LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py), ✅ [LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py) |
| Dedup enumeration (k-sum core) (`two_pointer_three_sum`) | sort + fixed `i` + `(l,r)` | skip duplicates deterministically at each level; inner pair-search is elimination-based | $O(n^2)$ (+ sort) | 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py), ✅ [LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py), [LeetCode 18 - 4Sum](https://leetcode.com/problems/4sum/description/) |
| Merge (2 sorted) | `i,j` forward | *See canonical “Merge Sorted Family” section (Kernel: MergeSortedSequences)* | $O(m+n)$ | *(canonical home below)* |

### Notes (constraints & architecture)
- Multi-sum enumeration **requires sorted input**; sorting cost `$O(n\log n)$` changes total complexity; sometimes hash-based alternatives exist.
- Writer-pointer variants: input often sorted or predicate-based; **stable vs unstable** compaction matters; reverse iteration sometimes needed (write from end to avoid overwrite).

### Ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - [ ] ✅ [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
- Core (medium)
  - [ ] 🔥 [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [ ] 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- Stretch (hard)
  - [ ] 🧪 [LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)

### Common failure modes (runbook)
- Opposite pointers: moving the wrong side breaks elimination proof
- Palindrome: skipping non-alnum must advance pointers correctly
- Writer: forgetting `read` always advances; `write` advances only when kept
- k-sum: dedup wrong level (same-level vs cross-level) ⇒ duplicates/missed tuples

---

## Sliding Window Family: `substring_window` (Kernel: SubstringSlidingWindow)
### Dependencies
- `Counter/map`; sometimes `PrefixSumRangeQuery`, `MonotonicDeque`

### ==Invariant-first thinking==
- Window `[L..R]` is valid iff **invariant holds**
- Modes:
  - **Maximize**: expand `R`, shrink while invalid
  - **Minimize**: expand until valid, shrink while still valid
  - **Enumerate**: expand `R`, shrink to restore validity, then **record for each `R`** (or **Exists**: early stop when first valid window found)

### Pattern comparison (cheat table)
| Pattern | Invariant | State | Window | Typical goal | Practice |
|---|---|---|---|---|---|
| sliding_window_unique | all unique | last index / freq | variable | maximize | 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) |
| sliding_window_at_most_k_distinct | ≤ K distinct | freq map | variable | maximize | ✅ [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) |
| sliding_window_freq_cover | For all `c` in `need`: `have[c] ≥ need[c]` (multiplicity matters) | need/have maps | variable/fixed | minimize / exists / all | 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py), ✅ [LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py), ✅ [LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) |
| sliding_window_cost_bounded | sum/cost constraint (**requires non-negative costs**) | integer sum | variable | minimize | ✅ [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) |
| sliding_window_fixed_size | `R-L+1 == k` | rolling sum / freq | fixed | maximize/minimize/enumerate | *(practice TBD in this subset)* |

### Template (hook-based pseudocode)
```text
L = 0
state = init()

for R in range(n):
  add(R, state)

  while is_invalid(L, R, state):
    remove(L, state)
    L += 1

  record_answer(L, R, state)   # maximize / enumerate
  # or: if is_valid(...) early return  # exists
```

### Important boundary note
- If array can contain **negatives**, “cost-bounded” sliding window generally breaks (monotonicity lost) → use `PrefixSumRangeQuery` (counts/equals) or `PrefixSum + monotonic deque` (shortest ≥ K) depending on goal.

### Ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
- Core (medium)
  - [ ] 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
  - [ ] ✅ [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
  - [ ] ✅ [LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - [ ] ✅ [LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
- Stretch (hard)
  - [ ] 🧪 [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)

### Common failure modes (runbook)
- Off-by-one window length: `R-L+1`
- Shrink condition wrong: `while invalid` vs `while still valid`
- Freq-cover: updating `have/need` inconsistently; forgetting multiplicity
- Recording answer at the wrong moment (before/after shrink)

---

## Prefix Sum Family (Kernel: PrefixSumRangeQuery)
### Dependencies
- `dict` / `defaultdict(int)`; sometimes `MonotonicDeque` for “shortest ≥ K” variants

### Template: prefix sum + hash map (count subarrays)
```text
freq = {0: 1}
prefix = 0
ans = 0

for x in nums:
  prefix += x
  ans += freq.get(prefix - k, 0)   # count subarrays sum == k
  freq[prefix] = freq.get(prefix, 0) + 1
```

### Ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] 🧪 [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py) *(hash-map cousin; warms up map discipline)*
- Core (medium)
  - [ ] ✅ [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) *(contrast: non-negative sliding window)*
- Stretch (hard)
  - [ ] 🧪 *(planned in this subset)* PrefixSum + MonotonicDeque (shortest subarray ≥ K)

### Common failure modes (runbook)
- Missing `freq[0]=1` causes off-by-one in subarrays starting at index 0
- Doing `freq[prefix]++` before querying changes semantics
- Using sliding window on data with negatives (should be prefix-based)

---

## Binary Search Boundary Family (Kernel: BinarySearchBoundary)
### Boundary templates
- **First true**
```text
lo, hi = 0, n  # hi is exclusive
while lo < hi:
  mid = (lo + hi) // 2
  if predicate(mid):
    hi = mid
  else:
    lo = mid + 1
return lo
```
- **Last true**
```text
lo, hi = -1, n-1
while lo < hi:
  mid = (lo + hi + 1) // 2  # upper mid
  if predicate(mid):
    lo = mid
  else:
    hi = mid - 1
return lo
```
- **Binary search on answer space**
  - predicate is feasibility/monotone constraint: `can(mid)`; find min feasible or max feasible

### Practice
- [ ] 🔥 [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py) *(boundary on partition; also relates to merge reasoning)*

### Ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] 🧪 *(planned in this subset)* first >= target boundary
- Core (medium)
  - [ ] 🔥 [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
- Stretch (hard)
  - [ ] 🧪 *(planned in this subset)* binary search on answer + greedy/heap feasibility

### Common failure modes (runbook)
- Non-monotone predicate ⇒ binary search invalid
- Wrong mid bias causes infinite loop
- Off-by-one on inclusive/exclusive `hi`

---

## Heap / Selection Family (Kernels: HeapTopK / DualHeapMedian / TwoPointerPartition)
### Heap vs quickselect (architectural)
- Heap supports **streaming/online** updates; quickselect is **batch/offline** and **mutates** the array.
- Complexity note: heap is $O(n\log k)$; quickselect average $O(n)$, worst $O(n^2)$.

### Practice
- [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) *(heap vs quickselect tradeoff)*

### Common failure modes (runbook)
- Picking heap for one-shot batch when quickselect is simpler (or vice versa for streaming)
- Wrong heap polarity; forgetting to cap heap size at k

---

## 🔗 Merge Sorted Family
### Merge 2 sorted (Kernel: MergeSortedSequences)
- [ ] 🔥 [LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
- [ ] ✅ [LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
- [ ] ✅ [LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

### Merge K sorted (Kernel: KWayMerge)
- **merge_k_sorted_heap**: $O(N \log K)$ (streaming)
- **merge_k_sorted_divide**: $O(N \log K)$ (batching)
- [ ] 🔥 [LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py) *(heap or divide-and-conquer merge; binary search not standard here.)*

### Ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] 🔥 [LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
- Core (medium)
  - [ ] ✅ [LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - [ ] ✅ [LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)
- Stretch (hard)
  - [ ] 🔥 [LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)

### Common failure modes (runbook)
- Losing tail when one side exhausts
- Wrong pointer increments causing infinite loop
- For in-place merges: overwriting unread data (need write-from-end)

---

## Monotonic Stack Family (Kernel: MonotonicStack)
### Canonical patterns
- `next_greater_element`: pop while `nums[st[-1]] <= nums[i]`, resolve “next greater”
- `stock_span`: stack stores decreasing prices; span computed by popping smaller/equal
- `histogram_max_rectangle`: stack stores increasing heights; pop to compute area with width by boundaries

### Ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] 🧪 *(planned in this subset)* next greater element
- Core (medium)
  - [ ] 🧪 *(planned in this subset)* stock span
- Stretch (hard)
  - [ ] 🧪 *(planned in this subset)* largest rectangle in histogram

### Common failure modes (runbook)
- Using values instead of indices (can’t compute widths)
- Wrong strictness (`<` vs `<=`) changes “next greater” semantics
- Forgetting final flush with sentinel

---

## Graph Wavefront BFS (Kernel: MultiSourceBFSWavefront)
### Dependencies
- queue/deque, visited representation, coordinate encoding

### Contract (explicit)
- Queue holds the **frontier**.
- Each outer-loop iteration processes **one step/minute** (level-order): process exactly `len(queue)` nodes, then increment time.
- `visited` prevents re-enqueue; mark visited **when enqueued**, not when dequeued.

### Implementation adapters
- Encode coordinates as `(r,c)` or `id = r*C + c`.
- visited representation: `bool grid`, `set`, or bitset (space-optimized).

### Practice ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] 🔥 [LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- Core (medium)
  - [ ] 🧪 *(planned in this subset)* multi-source shortest distance to nearest facility
- Stretch (hard)
  - [ ] 🧪 *(planned in this subset)* BFS with state compression (bitmask)

### Common failure modes (runbook)
- Marking visited on pop ⇒ duplicates balloon queue
- Not separating levels ⇒ wrong time/minutes count
- Missing boundary checks / wrong neighbor deltas

---

## Union-Find Family (Kernel: UnionFindConnectivity)
### DSU API (when to use)
- Use DSU when edges are added and you need **dynamic connectivity** queries (components, cycle detection in undirected graphs).
- Prefer BFS/DFS when you need traversal order/path or graph is static and you need explicit reachability paths.

```text
find(x):
  if parent[x] != x: parent[x] = find(parent[x])
  return parent[x]

union(a,b):
  ra, rb = find(a), find(b)
  if ra == rb: return False
  attach smaller-rank under larger-rank
  return True
```

### Ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] 🧪 *(planned in this subset)* connected components
- Core (medium)
  - [ ] 🧪 *(planned in this subset)* cycle detection (undirected)
- Stretch (hard)
  - [ ] 🧪 *(planned in this subset)* DSU on grid (islands union)

### Common failure modes (runbook)
- Not compressing paths ⇒ timeouts on large inputs
- Rank/size update wrong ⇒ deep trees
- Mixing 0/1 indexing

---

## 🐢🐇 Fast–Slow Pointers (Kernel: FastSlowPointers)
### Two-phase Floyd mental model
- Phase 1: detect cycle
  - Invariant: once both pointers are in the cycle, the distance between fast and slow increases by 1 mod cycle length each step ⇒ eventual meeting.
- Phase 2: find cycle start (reset one pointer to head)
  - From meeting point, moving both at speed 1 meets at entry.

### Works beyond linked lists
- Works on **functional graphs** where `f(x)` defines next state; linked list is a special case.

### Practice ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] 🔥 [LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py) *(cycle detect)*
- Core (medium)
  - [ ] 🔥 [LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py) *(cycle start)*
  - [ ] ✅ [LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py) *(midpoint)*
- Stretch (hard)
  - [ ] ✅ [LeetCode 202 - Happy Number](https://leetcode.com/problems/happy-number/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py) *(implicit cycle)*

### Common failure modes (runbook)
- Missing `fast` null checks (especially in Python/Java)
- Reset logic wrong in phase 2 (must move both 1 step)
- Using fast=fast.next (not 2 steps) breaks meeting guarantee

---

## 🧩 Backtracking (Kernel: BacktrackingExploration)
### Dependencies
- recursion/stack; `used[]` or bitmask; constraint trackers (sets/arrays)

### ==The invariant==
- **State consistency**: after returning from recursion, state must be exactly restored

### Backtracking supports (control-flow policies)
- enumerate all solutions
- find one solution (early exit)
- optimize best solution (track global best)

### Backtracking interface (hooks)
| Hook | Purpose |
|---|---|
| `choose(choice)` | apply choice to state |
| `unchoose(choice)` | restore state |
| `is_valid()` | local constraint check |
| `emit()` | record solution |
| `prune()` | bounding / feasibility checks |
| `next_choices()` | ordering heuristic |

### 5 decision-tree shapes (use the right “state handle”)
- **Permutation** → `used[]`
  - [ ] 🔥 [LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
  - [ ] ✅ [LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py) *(dedup: sort + same-level skip via `used[i-1]==False`)*
- **Subset** → `start_index`
  - [ ] 🔥 [LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
  - [ ] ✅ [LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py) *(dedup: sort + same-level skip `i>start && nums[i]==nums[i-1]`)*
- **Combination / fixed size** → `start_index` + `len(path)==k`
  - [ ] ✅ [LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py) *(sorted early break)*
  - [ ] 🔥 [LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py) *(reuse allowed: recurse with `i`)*
  - [ ] ✅ [LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py) *(no reuse: recurse with `i+1` + dedup)*
  - [ ] ✅ [LeetCode 216 - Combination Sum III](https://leetcode.com/problems/combination-sum-iii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py) *(fixed count + bounded range)*
- **Constraint satisfaction / placement**
  - [ ] 🔥 [LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
  - [ ] ✅ [LeetCode 52 - N-Queens II](https://leetcode.com/problems/n-queens-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)
  - [ ] ✅ [LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)
  - [ ] ✅ [LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)
  - [ ] ✅ [LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)

### Backtracking “toolbelt”
- **Pruning**
  - feasibility bound (not enough remaining choices)
  - target bound (`remaining < 0`)
  - sorted early exit (`candidates[i] > remaining → break`)
- **Dedup strategies**
  - sort + same-level skip (subset/combination)
  - sort + `used`-based skip (permutation)
- **Mitigation knobs**
  - ordering choices (most-constrained-first)
  - constraint propagation (maintain availability sets)
  - memoization (when state repeats)
  - bitmasks for compact state

### Ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] 🔥 [LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
- Core (medium)
  - [ ] 🔥 [LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
  - [ ] ✅ [LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
- Stretch (hard)
  - [ ] 🔥 [LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)

### Common failure modes (runbook)
- Not restoring state (missing `unchoose`)
- Mutating shared list without copying on `emit`
- Dedup done at wrong recursion level
- Missing early-exit wiring when “find one solution” is desired

---

## 🎛️ Partitioning & Selection (Kernel: TwoPointerPartition / HeapTopK)
### Partitioning invariants (Dutch flag)
- Maintain regions:
  - `[0..low)` are 0s
  - `[low..mid)` are 1s
  - `[mid..high]` unknown
  - `(high..end]` are 2s

### Practice ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] ✅ [LeetCode 905 - Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
  - [ ] ✅ [LeetCode 922 - Sort Array By Parity II](https://leetcode.com/problems/sort-array-by-parity-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
- Core (medium)
  - [ ] 🔥 [LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
- Stretch (hard)
  - [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) *(quickselect partition)*

### Heap alternative for kth/top-k (Kernel: HeapTopK)
- [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) *(compare: quickselect avg $O(n)$ vs heap $O(n\log k)$; heap is online, quickselect is offline & mutating)*

### Common failure modes (runbook)
- Partition: swapping then advancing the wrong pointer
- Assuming stability (partition is typically unstable)
- Forgetting quickselect worst-case $O(n^2)$

---

## Trie Family (Kernel: TriePrefixSearch)
### Trie operations (API)
- `insert(word)`
- `search(word)` (full word)
- `startsWith(prefix)`
- traversal/DFS enumeration (autocomplete)

### Ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] 🧪 *(planned in this subset)* basic trie insert/search
- Core (medium)
  - [ ] 🧪 *(planned in this subset)* prefix autocomplete enumeration
- Stretch (hard)
  - [ ] 🧪 *(planned in this subset)* Trie + backtracking (Word Search II style)

### Common failure modes (runbook)
- Confusing `startsWith` with `search` (end marker)
- Not handling empty string edge cases
- Memory blowups with large alphabets (use dict children)

---

## Topological Sort Family (Kernel: TopologicalSort)
### Two templates
- **Kahn’s algorithm (BFS on indegrees)**: queue zero-indegree nodes; pop, decrement neighbors
- **DFS postorder**: detect cycle via colors; append on exit; reverse postorder is topo

### Ladder (Intro → Core → Stretch)
- Intro (easy)
  - [ ] 🧪 *(planned in this subset)* simple DAG order
- Core (medium)
  - [ ] 🧪 *(planned in this subset)* prerequisites / course schedule
- Stretch (hard)
  - [ ] 🧪 *(planned in this subset)* topo + DP on DAG

### Common failure modes (runbook)
- Not counting all nodes (isolated nodes missing)
- Failing to detect cycles (processed count < V)
- DFS recursion depth in Python without iteration

---

## Real-world analogs (kernel → systems)
- Sliding window → log processing / rate limiting windows
- TopK/Heap → trending items, streaming leaderboards
- Multi-source BFS wavefront → propagation/contagion simulation, nearest facility
- Union-Find → clustering, network connectivity

---

## 🧭 Roadmap Anchors (from your graph)
### Curriculum (ordered)
- HashMapIndexing → Two Pointers → Sliding Window → Prefix Sum → Binary Search → Heap/TopK → Merge → Monotonic Stack → BFS/DFS → UnionFind → Backtracking → Trie → DP → Toposort

### Coverage list (unordered)
- **NeetCode 150** *(Use map sections above to find each problem’s kernel/pattern)*: [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), 2, 3, 4, 11, 15, 21, 23, 25, 26, 27, 39, 40, 46, 51, 75, 76, 78, 79, 80, 88, 90, 125, 131, 141, 142, 202, 209, 215, 283, 438, 567, 680, 876, 905, 922, 977, 994
- **Blind 75** *(Use map sections above to find each problem’s kernel/pattern)*: [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), 3, 11, 15, 21, 23, 26, 39, 75, 76, 79, 125, 141, 142, 215, 994
- **Specialty paths**
  - Sliding Window Mastery: 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py), 76, 209, 340, 438, 567
  - BFS Mastery: 🔥 [LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

### Problem → kernel(s) mapping (compact)
| LeetCode | Kernel(s) |
|---:|---|
| 1 | HashMapIndexing |
| 3 | SubstringSlidingWindow; HashMapIndexing |
| 4 | BinarySearchBoundary |
| 11 | TwoPointersTraversal |
| 15 | TwoPointersTraversal |
| 16 | TwoPointersTraversal |
| 21 | MergeSortedSequences |
| 23 | KWayMerge |
| 26 | TwoPointersTraversal |
| 27 | TwoPointersTraversal |
| 39 | BacktrackingExploration |
| 40 | BacktrackingExploration |
| 46 | BacktrackingExploration |
| 47 | BacktrackingExploration |
| 51 | BacktrackingExploration |
| 52 | BacktrackingExploration |
| 75 | TwoPointerPartition |
| 76 | SubstringSlidingWindow |
| 77 | BacktrackingExploration |
| 78 | BacktrackingExploration |
| 79 | BacktrackingExploration |
| 80 | TwoPointersTraversal |
| 88 | MergeSortedSequences |
| 90 | BacktrackingExploration |
| 93 | BacktrackingExploration |
| 125 | TwoPointersTraversal |
| 131 | BacktrackingExploration |
| 141 | FastSlowPointers |
| 142 | FastSlowPointers |
| 202 | FastSlowPointers |
| 209 | SubstringSlidingWindow |
| 215 | HeapTopK; TwoPointerPartition |
| 283 | TwoPointersTraversal |
| 340 | SubstringSlidingWindow |
| 438 | SubstringSlidingWindow |
| 567 | SubstringSlidingWindow |
| 680 | TwoPointersTraversal |
| 876 | FastSlowPointers |
| 905 | TwoPointerPartition |
| 922 | TwoPointerPartition |
| 977 | MergeSortedSequences |
| 994 | MultiSourceBFSWavefront |

---

## ✅ Quick “next 10 problems” playlist (balanced)
- Covers **7 kernels**: HashMapIndexing, TwoPointersTraversal, SubstringSlidingWindow, BinarySearchBoundary, HeapTopK, BacktrackingExploration, MultiSourceBFSWavefront
- [ ] 🔥 [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
- [ ] 🔥 [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
- [ ] 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- [ ] 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
- [ ] 🔥 [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
- [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
- [ ] 🔥 [LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
- [ ] 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
- [ ] 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- [ ] 🔥 [LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)[Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)