# Kernel Mapping Explanation

## Why Manual Configuration is Needed

### Core Issue: Different Conceptual Layers

This is not a problem of missing records in the ontology, but rather **three different conceptual layers**:

1. **Directory Name** (`meta/patterns/<dir_name>/`) - **Document Organization**
   - User-friendly naming
   - Used to organize documentation and teaching materials
   - Examples: `two_pointers`, `sliding_window`

2. **API Kernel ID** (`ontology/api_kernels.toml`) - **Formal Identifier of Algorithm Core**
   - Technical, precise naming
   - Defines the essence of algorithmic mechanisms
   - Examples: `TwoPointersTraversal`, `SubstringSlidingWindow`

3. **Pattern ID** (`ontology/patterns.toml`) - **Specific Application Patterns**
   - Problem-oriented naming
   - Describes specific application scenarios
   - Examples: `two_pointer_opposite`, `sliding_window_unique`

### Mapping Relationships Involve Logical Semantics

The mapping from directory name to API Kernel is a **human-made, semantically-based decision**:

- The `two_pointers` directory may contain various two-pointer variants
- But it primarily corresponds to `TwoPointersTraversal` (not `TwoPointerPartition` or `FastSlowPointers`)
- This choice reflects **teaching and documentation organization intent**, not a technical necessity

### Why Automatic Matching is Unreliable?

1. **Naming inconsistency is a design choice**, not an error
   - `bfs_grid` vs `grid_bfs_propagation` - Different word order is normal
   - `monotonic_stack` vs `next_greater_element` - Pattern ID describes problems, not techniques

2. **Semantic Ambiguity**
   - `dp_sequence` vs `dp_interval` - Both need `dp_` prefix, but have different semantics
   - Automatic matching cannot understand this semantic difference

3. **High Maintenance Cost**
   - Complex matching rules are difficult to maintain
   - Many edge cases, prone to errors
   - Explicit configuration is clearer

## Why Some Mappings Cannot Be Auto-Inferred?

### Problem Categories

#### 1. **Word Order Mismatch**
**Issue**: Directory name and Pattern ID have different word order

| Directory Name | Pattern ID | Reason |
|----------------|-----------|--------|
| `bfs_grid` | `grid_bfs_propagation` | Reversed order |
| `k_way_merge` | `merge_k_sorted_heap` | Different order |

**Solution**: Word-order independent matching (Strategy 3) has been implemented, but requires all keywords to match.

#### 2. **Pattern ID Doesn't Contain Directory Name**
**Issue**: Pattern ID uses completely different naming

| Directory Name | Pattern ID | API Kernel |
|----------------|-----------|------------|
| `monotonic_stack` | `next_greater_element` | `MonotonicStack` |
| `monotonic_stack` | `next_smaller_element` | `MonotonicStack` |
| `monotonic_stack` | `histogram_max_rectangle` | `MonotonicStack` |

**Solution**: API Kernel fallback matching (`_match_by_api_kernel_name`) has been implemented, matching directly by API Kernel name.

#### 3. **Prefix Ambiguity**
**Issue**: Multiple directories share the same prefix, cannot be distinguished

| Directory Name | Pattern ID | API Kernel |
|----------------|-----------|------------|
| `dp_sequence` | `dp_fibonacci_style` | `DPSequence` |
| `dp_sequence` | `dp_longest_increasing` | `DPSequence` |
| `dp_interval` | `dp_palindrome` | `DPInterval` |

**Issue**: Both start with `dp_`, cannot be distinguished by prefix.

**Solution**: 
- Requires more precise pattern matching (check specific pattern types)
- Or resolve through explicit mapping in config file

#### 4. **Missing Patterns in Ontology**
**Issue**: API Kernel exists, but no Patterns are defined

| Directory Name | API Kernel | Patterns |
|----------------|-----------|----------|
| `trie` | `TriePrefixSearch` | (none) |
| `topological_sort` | `TopologicalSort` | (none) |

**Solution**: 
- Add corresponding patterns in `ontology/patterns.toml`
- Or manually map through config file

#### 5. **Naming Inconsistency**
**Issue**: Directory name and Pattern ID use different terms

| Directory Name | Pattern ID | Reason |
|----------------|-----------|--------|
| `tree_bfs` | `bfs_level_order` | Uses `bfs` instead of `tree_bfs` |
| `linked_list_reversal` | `linked_list_k_group_reversal` | Should match, but may be interfered by other strategies |

## Current Solution

### Implemented Strategies

1. **Exact Prefix Matching** (Strategy 1)
   - `sliding_window` → `sliding_window_*`

2. **Singular/Plural Variations** (Strategy 2)
   - `two_pointers` → `two_pointer_*`

3. **Word-Order Independent Matching** (Strategy 3)
   - `bfs_grid` → `grid_bfs_*` (partially implemented)

4. **API Kernel Fallback** (`_match_by_api_kernel_name`)
   - `monotonic_stack` → Find all patterns with `api_kernel = "MonotonicStack"`

### Mappings in Config File

The following mappings require manual configuration (cannot be fully auto-inferred):

```toml
[kernel_mapping]
bfs_grid = "GridBFSMultiSource"           # Word order issue
k_way_merge = "KWayMerge"                 # Word order issue
linked_list_reversal = "LinkedListInPlaceReversal"  # Should match, but kept as fallback
monotonic_stack = "MonotonicStack"         # Pattern ID doesn't contain dir name (solved via API Kernel matching)
tree_bfs = "TreeTraversalBFS"              # Naming inconsistency (solved via API Kernel matching)
dp_sequence = "DPSequence"                 # Prefix conflict
dp_interval = "DPInterval"                 # Prefix conflict
trie = "TriePrefixSearch"                  # Missing Patterns
topological_sort = "TopologicalSort"      # Missing Patterns
```

## Improvement Suggestions

### Short-term Improvements (Implemented)

1. ✅ **API Kernel Fallback Matching**: When Pattern ID doesn't match, match directly by API Kernel name
2. ✅ **Word-Order Independent Matching**: Check keyword sets instead of order

### Long-term Improvements (Optional)

1. **Smarter Prefix Disambiguation**
   - For `dp_sequence` vs `dp_interval`, check specific pattern characteristics
   - Or require pattern IDs to include clearer identifiers (e.g., `dp_sequence_*` vs `dp_interval_*`)

2. **Complete Ontology**
   - Add patterns for `trie` and `topological_sort`
   - Unify pattern ID naming conventions

3. **Configuration Priority**
   - Config file mappings take precedence over auto-inference
   - Allow overriding auto-inferred results

## Summary

**Auto-inferrable Mappings** (8):
- `sliding_window`, `backtracking`, `binary_search`, `two_pointers`, 
- `prefix_sum`, `tree_dfs`, `union_find`, `heap_top_k`

**Manually Configured Mappings** (9):
- Word order issues: `bfs_grid`, `k_way_merge`
- Prefix conflicts: `dp_sequence`, `dp_interval`
- Missing Patterns: `trie`, `topological_sort`
- Others: `linked_list_reversal`, `monotonic_stack`, `tree_bfs`

**Note**: Through API Kernel fallback matching, `monotonic_stack` and `tree_bfs` can actually be auto-inferred, but for clarity and maintainability, it's recommended to keep them in the config file.
