---
title: LeetCode Patterns Knowledge Graph (33 Problems) — API Kernels → Patterns → Problems 🎯
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 How to use this mind map (fast)
- **Read top-down**: *API Kernel* → *Pattern* → *Problems* (linked)
- **Practice loop**: implement template → solve 2–3 problems → refactor into reusable `solve(pattern_state_machine)` mental model
- **Progress tracking**
  - [ ] Do all **Easy** first
  - [ ] Then **Medium** variants
  - [ ] Finally **Hard** “edge-case amplifiers”
- **Problem tags (3-tier)**
  - 🔥 Must-know
  - ⭐ Common
  - 🧊 Nice-to-know

---

## 🧠 API Kernels (the “engines”)
### 🧭 Routing guide (pick the right kernel)
- **Need pair lookup under target (no sorted guarantee)?** → **HashMapComplement**
- **Need contiguous subarray/substring optimum under constraint?** → **SubstringSlidingWindow**
  - Gotcha: correct when **validity is monotone under shrinking** (or the window is **fixed-size**).
- **Sorted + pair/triple constraints / symmetric checks / in-place edits?** → **TwoPointersTraversal**
- **In-place grouping by predicate?** → **TwoPointerPartition**
  - Gotcha: maintain swap-safe region invariants (don’t “lose” unknown region).
- **Boundary in sorted/rotated array or “first true / last true”?** → **BinarySearchBoundary**
- **Next greater/smaller / span / histogram area?** → **MonotonicStack**
- **Merge sorted streams (2-way / k-way)?** → **MergeSortedSequences / KWayMerge**
- **Need level/min steps propagation on grid/graph?** → **GridBFSMultiSource**

---

### HashMapComplement — *one-pass complement lookup*
- ==Core invariant==: when processing index `i`, the hash map contains all needed complements from indices `< i`
- **Kernel Contract**
  - **Inputs**: array of values; no sorted requirement
  - **State**: `seen[value] = index`
  - **Transitions**: `process(x)`, `insert(x)`
  - **Validity predicate**: `target - x in seen`
  - **Objective**: **exist** (return indices)
- System mapping: fast joins / de-dup / “have I seen this key?” lookup
- Patterns
  - **hash_map_complement**
    - 🎯 Problems
      - [ ] 🔥 [LeetCode Two Sum](https://leetcode.com/problems/0001_two_sum/)
    - Guardrails: if input is sorted (or you sort), you can also do an opposite-pointer variant, but it changes constraints/complexity.
- Related patterns: prefix sum + hashmap for subarray sums; sorted variant → `two_pointer_opposite_search`

---

### SubstringSlidingWindow — *1D window state machine*
- ==Core invariant==: window `[L,R]` stays valid by **expand right** + **contract left**
- **Time**: $O(n)$ *amortized* when each index enters/leaves the window at most once (monotone `L`,`R`) and validity updates are $O(1)$  
- **Space**: $O(\min(n,\Sigma))$ for frequency/last-seen maps; $O(\Sigma)$ only if you maintain counts for the whole alphabet
- **Kernel Contract**
  - **Inputs**: sequence (string/array); constraint type decides **variable** vs **fixed** window; cost-bounded variant often requires **non-negative** costs
  - **State**: counts/last-seen + auxiliary counters (`distinct`, `formed/required`, `matches`, running `sum`)
  - **Transitions**: `expand(R)`, `shrink(L)` (while invalid), `record_answer()`
  - **Validity predicate**: `valid(state)` maintained in $O(1)$ (avoid rescanning maps)
  - **Objective**: max / min / exist / all
- System mapping: rate limiting (moving time window counters), log scanning, “last N minutes” metrics, stream de-dup

<!-- markmap: fold -->
#### Pattern cheat sheet (from docs)
| Problem | Invariant (explicit predicate) | State | Window Size | Goal |
|---------|--------------------------------|-------|-------------|------|
| [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | `∀c: windowCount[c] <= 1` | last index map | Variable | Max |
| [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) | `distinct <= k` | freq map + distinct | Variable | Max |
| [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | `∀c: windowCount[c] >= needCount[c]` (tracked via `formed == required`) | need/have + formed/required | Variable | Min |
| [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) | fixed `len(window)==len(s1)` and `∀c: windowCount[c] == needCount[c]` (or `diffCount==0`) | freq + matches/diff | Fixed | Exists |
| [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) | fixed `len(window)==len(p)` and `∀c: windowCount[c] == needCount[c]` (or `diffCount==0`) | freq + matches/diff | Fixed | All |
| [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | `windowSum >= target` | running sum | Variable | Min |

#### Patterns (grouped by objective)
- **Maximize (variable window)**
  - **sliding_window_unique** *(maximize, “jump left” optimization)*
    - 🎯 Problems
      - [ ] 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
    - Key state: `last_seen[char]` → `L = max(L, last_seen[c]+1)`
    - Guardrails: update answer after each `R` expansion; `L` only moves forward (monotone).
  - **sliding_window_at_most_k_distinct** *(maximize, shrink while invalid)*
    - 🎯 Problems
      - [ ] ⭐ [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
    - Key invariant: `distinct <= k` (track `distinct` in $O(1)$)
    - Guardrails: decrement `distinct` only when a count drops to 0.
- **Minimize (variable window)**
  - **sliding_window_freq_cover** *(cover `t`, minimize while valid)*
    - 🎯 Problems
      - [ ] 🔥 [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) — *minimize while valid*
    - Key predicate: maintain `formed == required` where `formed` increments only when `windowCount[c] == needCount[c]`
    - Guardrails: update answer inside the “while valid: shrink” loop (not only after expanding).
  - **sliding_window_cost_bounded** *(numeric constraint, minimize while valid)*
    - 🎯 Problems
      - [ ] 🔥 [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
    - Preconditions / gotchas:
      - Monotone-shrink is correct when all numbers are **positive** (or non-negative): expanding `R` never decreases sum; shrinking `L` never increases sum.
      - If negatives exist → use prefix sums + monotonic deque / other techniques.
    - Guardrails: requires **non-negative** numbers for monotone shrink; otherwise switch kernels.
- **Exist (fixed window)**
  - **sliding_window_fixed_size** *(fixed length, boolean existence)*
    - 🎯 Problems
      - [ ] ⭐ [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
    - Key predicate: fixed `k = len(s1)` and `diffCount == 0` (or all counts match)
    - Guardrails: do not shrink with a while-loop; slide by one each step.
- **Enumerate all (fixed window)**
  - **sliding_window_fixed_size** *(fixed length, collect all matches)*
    - 🎯 Problems
      - [ ] ⭐ [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
    - Key predicate: fixed `k = len(p)` and `diffCount == 0` (or all counts match)
    - Guardrails: record answer at each `R` once window size reaches `k`.

- Related patterns:
  - `sliding_window_freq_cover` ↔ `sliding_window_fixed_size` (anagram/permutation) via the same counter bookkeeping (formed/matches/diff)

---

### TwoPointersTraversal — *pointer choreography on sequences*
- ==Core invariant==: pattern-parameterized invariant
  - Opposite pointers: maintain that all candidate solutions requiring indices outside `[L,R]` have been ruled out by a dominance argument.
  - Writer/read pointers: maintain that `arr[:write]` equals the desired transformation of `arr[:read]`.
- **Kernel boundary**: primarily **array/string scanning** (optionally sorted); pointers are indices over a sequence, not structural edges.
- Complexity: often $O(n)$ time, $O(1)$ space (except sorting step)
- **Kernel Contract**
  - **Inputs**: array/string; some patterns require sorted order (or a preprocessing sort)
  - **State**: pointer positions + optional running best + dedup rules
  - **Transitions**: `advance_left()`, `advance_right()`, `advance_both()`, `write()`
  - **Validity predicate**: local predicate on `arr[L], arr[R]` (and/or `arr[i]` for enumeration) that decides movement
  - **Objective**: max / exist / all / in-place transform
- System mapping: two-ended scanning, in-place compaction, “stream filter” style transformations

#### Pattern comparison (from docs)
| Pattern | Pointer Init | Movement | Termination | Time | Space | Key Use Case |
|---------|--------------|----------|-------------|------|-------|--------------|
| Opposite | `0, n-1` | toward center | `L>=R` | $O(n)$ | $O(1)$ | sorted pairs / palindrome / maximize |
| Same-direction | `write, read` | forward | `read==n` | $O(n)$ | $O(1)$ | in-place modify |
| Fast–Slow | `slow, fast` | 1× / 2× | meet or null | $O(n)$ | $O(1)$ | cycle / midpoint |
| Dedup enum | `i` + `L,R` | nested | done | $O(n^2)$ | $O(1)$ | 3Sum/4Sum |

#### Patterns
- **two_pointer_opposite_maximize**
  - 🎯 Problems
    - [ ] 🔥 [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - Insight: move the pointer at the **shorter** height
  - Guardrails: requires dominance argument (moving taller side cannot improve area if shorter side unchanged).
- **two_pointer_three_sum** *(dedup enumeration)*
  - 🎯 Problems
    - [ ] 🔥 [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
    - [ ] ⭐ [LeetCode 16 - 3Sum Closest](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
  - Requires: sort first ($O(n\log n)$), then scan with dedup
  - Guardrails: requires sort; watch dedup and overflow edges.
- **two_pointer_opposite_palindrome**
  - 🎯 Problems
    - [ ] ⭐ [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
    - [ ] ⭐ [LeetCode 680 - Valid Palindrome II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
  - Guardrails: define skip/normalize rules precisely (alnum vs punctuation; at most one deletion).
- **two_pointer_writer_dedup**
  - 🎯 Problems
    - [ ] ⭐ [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
    - [ ] ⭐ [LeetCode 80 - Remove Duplicates from Sorted Array II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
  - Guardrails: invariant is `arr[:write]` is the deduped prefix of `arr[:read]` (maintain write rules).
- **two_pointer_writer_remove**
  - 🎯 Problems
    - [ ] ⭐ [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - Guardrails: ensure every `read` step advances; `write` only advances on kept elements.
- **two_pointer_writer_compact**
  - 🎯 Problems
    - [ ] ⭐ [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
  - Guardrails: preserve relative order of non-zeros by writing in read order.

- Related patterns:
  - sort + two pointers ↔ `two_pointer_three_sum`
  - writer pointers ↔ stable compaction problems

---

### FastSlowPointers — *Floyd + midpoints + implicit sequences*
- ==Core invariant==: if a cycle exists, `fast` meets `slow`
- **Kernel boundary**: pointers traverse **linked structure or function iteration** (implicit graph), primarily for **cycle/midpoint** properties.
- Cross-link: fast–slow is a specialization of two-pointer movement on *iterators* rather than indexes.
- **Kernel Contract**
  - **Inputs**: linked list node pointers or function iteration `x_{t+1}=f(x_t)`
  - **State**: `slow`, `fast` (and optionally phase-2 pointer)
  - **Transitions**: `slow = next(slow)`, `fast = next(next(fast))`
  - **Validity predicate**: `fast is None` (no cycle) or `slow == fast` (cycle detected)
  - **Objective**: exist (cycle), locate (cycle start), find midpoint
- System mapping: loop detection in iterators/state machines; detecting periodicity in generated sequences
- Patterns
  - **fast_slow_cycle_detect**
    - [ ] 🔥 [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - **fast_slow_cycle_start**
    - [ ] 🔥 [LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
  - **fast_slow_midpoint**
    - [ ] ⭐ [LeetCode 876 - Middle of the Linked List](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)
  - **fast_slow_implicit_cycle**
    - [ ] ⭐ [LeetCode 202 - Happy Number](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)

---

### BinarySearchBoundary — *first/last true + rotated boundaries*
- **Kernel Contract**
  - **Inputs**: sorted/monotone predicate space; sometimes rotated sorted arrays
  - **State**: `lo, hi, mid` + invariant on predicate region
  - **Transitions**: shrink search space by half based on predicate
  - **Validity predicate**: monotone predicate `P(i)` (false→true) or sorted order property
  - **Objective**: first true / last true / find target / boundary index
- System mapping: version rollouts (“first bad build”), threshold tuning, capacity boundary search
- Patterns
  - **binary_search_rotated**
    - 🎯 Problems
      - [ ] 🔥 [LeetCode Search in Rotated Sorted Array](https://leetcode.com/problems/0033_search_in_rotated_sorted_array/)
    - Guardrails: compare against `nums[mid]` and one side boundary to decide which half is sorted.
  - **binary_search_first_true**
    - 🎯 Problems
      - [ ] ⭐ [LeetCode Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/0034_find_first_and_last_position_of_element_in_sorted_array/)
    - Guardrails: use half-open intervals or consistent `lo/hi` updates to avoid infinite loops.
  - **binary_search_last_true**
    - 🎯 Problems
      - [ ] ⭐ [LeetCode Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/0034_find_first_and_last_position_of_element_in_sorted_array/)
    - Guardrails: implement as `first_true(> target) - 1` or a symmetric boundary search.
  - **binary_search_on_answer**
    - 🎯 Problems
      - [ ] ⭐ [LeetCode Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/0153_find_minimum_in_rotated_sorted_array/)
      - [ ] 🧊 [LeetCode Find Peak Element](https://leetcode.com/problems/0162_find_peak_element/)
    - Guardrails: must define feasibility predicate `feasible(x)` that is monotone in `x`.

---

### MonotonicStack — *next greater/smaller + area/span*
- **Kernel Contract**
  - **Inputs**: array where we need nearest greater/smaller or span/area contributions
  - **State**: stack of indices with monotone values (increasing or decreasing)
  - **Transitions**: while stack violates monotonicity, pop and resolve contributions; then push current index
  - **Validity predicate**: stack is monotone (by value) after each step
  - **Objective**: next greater/smaller index/value; aggregate area/span
- System mapping: “next higher price”, latency spike spans, skyline/area aggregation
- Patterns
  - **next_greater_element**
    - 🎯 Problems
      - [ ] 🔥 [LeetCode Daily Temperatures](https://leetcode.com/problems/0739_daily_temperatures/)
      - [ ] ⭐ [LeetCode Next Greater Element I](https://leetcode.com/problems/0496_next_greater_element_i/)
    - Guardrails: store indices; answer resolved on pop when current value is the “next greater”.
  - **histogram_max_rectangle**
    - 🎯 Problems
      - [ ] 🔥 [LeetCode Largest Rectangle in Histogram](https://leetcode.com/problems/0084_largest_rectangle_in_histogram/)
    - Guardrails: append sentinel 0 to flush stack; compute width via previous smaller index.

---

### TwoPointerPartition — *in-place partitioning “mini quicksort”*
- ==Core invariant==: regions are partitioned by property
- **Kernel Contract**
  - **Inputs**: array; predicate/classification function; in-place allowed
  - **State**: region boundaries (`low/mid/high` or `i/j`)
  - **Transitions**: `swap()` + move boundary pointers according to element class
  - **Validity predicate**: region invariants remain true after each swap
  - **Objective**: in-place grouping / selection
- System mapping: partitioning logs by severity, bucketing items by type, in-place stable/unstable compaction
- Patterns
  - **dutch_flag_partition**
    - [ ] ⭐ [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
    - Invariant (3 regions):
      - `arr[0:low] == 0`
      - `arr[low:mid] == 1`
      - `arr[high+1:n] == 2`
      - `mid` scans the unknown region `arr[mid:high+1]`
    - Guardrails: when swapping with `high`, do not increment `mid` until the swapped-in element is processed.
  - **two_way_partition**
    - [ ] 🧊 [LeetCode 905 - Sort Array By Parity](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
    - [ ] 🧊 [LeetCode 922 - Sort Array By Parity II](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
    - Guardrails: define which side consumes equal elements; avoid infinite swaps.
  - **quickselect_partition** *(selection via partition)*
    - 🎯 Problems
      - See **Selection**: [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
    - Guardrails: expected $O(n)$ but worst-case $O(n^2)$; randomize pivot / introselect-style defenses.
    - Complexity note: expected $O(n)$, worst-case $O(n^2)$ unless randomized pivot / median-of-medians; space $O(1)$ iterative or $O(\log n)$ recursion.

- Related patterns:
  - partition ↔ quickselect ↔ heap top-k (same selection problem, different constraints)

---

### MergeSortedSequences — *merge two sorted sequences*
- ==Core invariant==: output prefix is fully sorted
- **Kernel Contract**
  - **Inputs**: two sorted sequences (lists/arrays); comparator
  - **State**: two read pointers + output pointer
  - **Transitions**: take smaller head, advance that pointer
  - **Validity predicate**: output prefix is sorted and contains exactly consumed items
  - **Objective**: construct merged sorted sequence
- System mapping: merging two sorted streams/shards, two-way join-like operations
- Patterns
  - **merge_two_sorted_lists**
    - [ ] ⭐ [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - **merge_two_sorted_arrays**
    - [ ] ⭐ [LeetCode 88 - Merge Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - **merge_sorted_from_ends**
    - [ ] ⭐ [LeetCode 977 - Squares of a Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

- Related patterns:
  - merge-two ↔ k-way merge ↔ “boundary + merge thinking” (median of two sorted arrays)

---

### KWayMerge — *merge K sorted sequences*
- Two main implementations
  - **merge_k_sorted_heap** → $O(N\log k)$ time, $O(k)$ heap
  - **merge_k_sorted_divide** → $O(N\log k)$ time, smaller constants sometimes
- **Kernel Contract**
  - **Inputs**: K sorted sequences / iterators; may be streaming
  - **State**: heap of current heads (or pairwise merge recursion)
  - **Transitions**: pop smallest head, push next from that sequence
  - **Validity predicate**: heap contains current minimum candidate from each non-empty sequence
  - **Objective**: produce globally sorted stream
- System mapping: merging sorted shards, log compaction, search index segment merge (LSM-style)

<!-- markmap: fold -->
#### Trade-offs (k-way merge)
- Heap: best for **streaming** / iterators; $O(k)$ memory; simple; good when you can’t random-access lists.
- Divide & conquer: same asymptotic $O(N\log k)$; often fewer heap ops; good when lists are in memory.
- Flatten + sort: $O(N\log N)$; simplest but usually slower for large k or large N.

- 🎯 Problems
  - [ ] 🔥 [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - Related “hybrid thinking”: [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

---

### HeapTopK — *keep best K under streaming updates*
- **Kernel Contract**
  - **Inputs**: stream/array; comparator; `k`
  - **State**: heap of size ≤ `k`
  - **Transitions**: push; if size>k pop; peek kth
  - **Validity predicate**: heap contains the best `k` seen so far (by ordering)
  - **Objective**: keep top-k / kth element
- System mapping: trending topics, leaderboard maintenance, top error codes; extension: Count-Min Sketch for approximate heavy hitters
- Patterns
  - **heap_kth_element**
    - 🎯 Problems
      - See **Selection**: [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
    - Guardrails: $O(n\log k)$ time, $O(k)$ space; streaming-friendly and stable.

---

### GridBFSMultiSource — *wavefront propagation on grids*
- Pattern
  - **grid_bfs_propagation**
    - [ ] 🔥 [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- **Kernel Contract**
  - **Inputs**: grid as implicit graph; multiple sources
  - **State**: queue (frontier), visited/updated grid, minutes/levels
  - **Transitions**: `process_level()`, expand to 4/8-neighbors, enqueue newly-activated nodes
  - **Validity predicate**: each cell is processed at most once (or with monotone distance)
  - **Objective**: min time/steps to propagate (or detect impossibility)
- Implementation invariant: queue holds frontier of current “minute/level”
- System mapping: multi-source shortest-time propagation (network outage spread, contagion simulation, dependency propagation)

<!-- markmap: fold -->
#### Trade-offs (grid BFS)
- Multi-source BFS: one pass; gives shortest time from nearest source in unweighted grid.
- Repeated single-source BFS: typically redundant and slower (often $k$ times more work).
- Memory: queue + visited can be large; consider in-place marking when allowed.

- Related patterns:
  - BFS wavefront ↔ shortest path in unweighted graphs; multi-source init is the “preprocess” step.

---

### LinkedListInPlaceReversal — *pointer surgery*
- **Kernel Contract**
  - **Inputs**: linked list head; segment size `k` (optional)
  - **State**: `prev/curr/next` pointers; group boundaries
  - **Transitions**: reverse pointers within segment; stitch segments
  - **Validity predicate**: reversed segment remains connected; outside segment preserved
  - **Objective**: transform list structure in-place
- Pattern
  - **linked_list_k_group_reversal**
    - [ ] 🔥 [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
- Also core linked list arithmetic
  - [ ] ⭐ [LeetCode 2 - Add Two Numbers](https://github.com/lufftw/neetcode/blob/main/solutions/0002_add_two_numbers.py)

---

### BacktrackingExploration — *search tree with pruning*
- **Kernel Contract**
  - **Inputs**: decision space; constraints
  - **State**: partial assignment + constraint bookkeeping
  - **Transitions**: choose → recurse → undo (backtrack)
  - **Validity predicate**: partial assignment is consistent (prune early)
  - **Objective**: enumerate all solutions / find one
- Pattern
  - **backtracking_n_queens**
    - [ ] 🧊 [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)

---

## 🧭 Roadmap slices (what to do next)
### Sliding Window Mastery 📚
- [ ] Complete `sliding_window_unique` cluster (see `SubstringSlidingWindow → Maximize (variable window)`)
- [ ] Complete `sliding_window_at_most_k_distinct` cluster (see `SubstringSlidingWindow → Maximize (variable window)`)
- [ ] Complete `sliding_window_freq_cover` cluster (see `SubstringSlidingWindow → Minimize (variable window)`)
- [ ] Complete `sliding_window_cost_bounded` cluster (see `SubstringSlidingWindow → Minimize (variable window)`)
- [ ] Complete `sliding_window_fixed_size` cluster (see `SubstringSlidingWindow → fixed window`)

### Two Pointers Mastery ⚡
- [ ] Complete `two_pointer_opposite_maximize` (see `TwoPointersTraversal`)
- [ ] Complete `two_pointer_three_sum` (see `TwoPointersTraversal`)
- [ ] Complete `two_pointer_opposite_palindrome` (see `TwoPointersTraversal`)
- [ ] Complete writer-pointer clusters: `two_pointer_writer_dedup`, `two_pointer_writer_remove`, `two_pointer_writer_compact` (see `TwoPointersTraversal`)
- [ ] Complete `FastSlowPointers` clusters (see `FastSlowPointers` kernel)

---

## 🧩 “Same problem, different lens” (transfer learning)
- **Selection**: [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
  - Option A: `quickselect_partition` — expected $O(n)$, worst-case $O(n^2)$ unless randomized pivot / median-of-medians; space $O(1)$ iterative or $O(\log n)$ recursion
  - Option B: `heap_kth_element` — $O(n\log k)$ time, $O(k)$ space; streaming-friendly
- **Merging**:
  - 2-way: [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py), [LeetCode 88 - Merge Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - K-way: [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - “boundary + merge thinking”: [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

<!-- markmap: fold -->
### Composition matrix (pipelines)
- **Sort + Two Pointers** (3Sum)
  - Preprocess: sort ($O(n\log n)$)
  - Kernel: `two_pointer_three_sum` (scan + dedup)
  - Postprocess: collect unique tuples
- **Heap + Merge** (k-way merge)
  - Preprocess: push each list head into heap
  - Kernel: pop/push to produce sorted stream
  - Postprocess: rebuild list/array from stream
- **Partition + TopK** (Kth largest)
  - Preprocess: choose/randomize pivot
  - Kernel: partition + recurse/iterate on one side
  - Postprocess: return kth element
- **BFS + Multi-source initialization** (grid wavefront)
  - Preprocess: enqueue all sources with distance 0
  - Kernel: level-order BFS expansion
  - Postprocess: compute max distance / detect unreachable

---

## 🧱 Minimal reusable templates (mental API)
```python
# Sliding Window micro-templates
# NOTE: Maintain enough auxiliary counters so that validity checks are O(1)
# (e.g., distinct_count, formed/required, matches/diffCount). Avoid scanning maps each step.

# 1) Unique window (LeetCode 3): last_seen + jump L
def longest_unique(s: str) -> int:
    last = {}
    L = 0
    ans = 0
    for R, ch in enumerate(s):
        if ch in last:
            L = max(L, last[ch] + 1)
        last[ch] = R
        ans = max(ans, R - L + 1)  # record on each R
    return ans
# Common bug: forgetting L = max(L, last[ch]+1) (can move L backwards).

# 2) At most K distinct (LeetCode 340): freq + distinct_count
def longest_at_most_k_distinct(s: str, k: int) -> int:
    freq = {}
    distinct = 0
    L = 0
    ans = 0
    for R, ch in enumerate(s):
        if freq.get(ch, 0) == 0:
            distinct += 1
        freq[ch] = freq.get(ch, 0) + 1

        while distinct > k:
            left = s[L]
            freq[left] -= 1
            if freq[left] == 0:
                distinct -= 1
            L += 1

        ans = max(ans, R - L + 1)  # record after shrink restores validity
    return ans
# Common bug: not decrementing distinct when a count hits 0.

# 3) Cover t (LeetCode 76): need/have + formed/required
def min_window_cover(s: str, t: str) -> str:
    need = {}
    for ch in t:
        need[ch] = need.get(ch, 0) + 1
    required = len(need)

    have = {}
    formed = 0
    L = 0
    best = (10**18, None, None)

    for R, ch in enumerate(s):
        have[ch] = have.get(ch, 0) + 1
        if ch in need and have[ch] == need[ch]:
            formed += 1

        while formed == required:
            if R - L + 1 < best[0]:
                best = (R - L + 1, L, R)

            left = s[L]
            have[left] -= 1
            if left in need and have[left] < need[left]:
                formed -= 1
            L += 1

    _, i, j = best
    return "" if i is None else s[i:j+1]
# Common bug: updating formed on >= instead of ==, or forgetting to decrement when dropping below need.

# Two pointers (opposite)
def opposite(arr):
    L, R = 0, len(arr) - 1
    while L < R:
        if should_move_left(arr, L, R):
            L += 1
        else:
            R -= 1
```

---