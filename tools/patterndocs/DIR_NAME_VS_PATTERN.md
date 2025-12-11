# Directory Name vs Pattern ID Naming Inconsistency Analysis

## Core Issue

**Yes, part of the reason is naming inconsistency between directory names and Pattern IDs.**

But there are deeper reasons as well.

---

## Category Analysis

### Category 1: Consistent Naming ✅ Can Auto-Infer

| Directory Name | Pattern ID Prefix | Status |
|----------------|-------------------|--------|
| `sliding_window` | `sliding_window_*` | ✅ Completely consistent, can auto-infer |

**Example**:
```toml
# ontology/patterns.toml
id = "sliding_window_unique"        # ← Prefix matches
id = "sliding_window_at_most_k"     # ← Prefix matches
```

**Result**: Can auto-infer Kernel through Pattern ID

---

### Category 2: Singular/Plural Inconsistency ⚠️ Needs Handling

| Directory Name | Pattern ID Prefix | Status |
|----------------|-------------------|--------|
| `two_pointers` | `two_pointer_*` | ⚠️ Singular/plural inconsistency |

**Example**:
```toml
# ontology/patterns.toml
id = "two_pointer_opposite"         # ← Singular
id = "two_pointer_same_direction"   # ← Singular
```

**Issue**: Directory name is plural `two_pointers`, Pattern ID is singular `two_pointer`

**Solution**: Singular/plural handling implemented (automatically matches `two_pointers` → `two_pointer`)

---

### Category 3: Word Order Inconsistency ❌ Needs Manual Configuration

| Directory Name | Pattern ID Prefix | Status |
|----------------|-------------------|--------|
| `bfs_grid` | `grid_bfs_*` | ❌ Reversed order |
| `k_way_merge` | `merge_k_*` | ❌ Different order |

**Example**:
```toml
# ontology/patterns.toml
id = "grid_bfs_propagation"         # ← Reversed order
id = "merge_k_sorted_heap"           # ← Different order
```

**Issue**: Directory name and Pattern ID have different word order

**Solution**: Requires manual configuration in `kernel_mapping`

---

### Category 4: Pattern ID Doesn't Contain Directory Name ❌ Needs Manual Configuration

| Directory Name | Pattern ID | Status |
|----------------|-----------|--------|
| `monotonic_stack` | `next_greater_element` | ❌ Completely missing |
| `monotonic_stack` | `next_smaller_element` | ❌ Completely missing |
| `monotonic_stack` | `histogram_max_rectangle` | ❌ Completely missing |

**Example**:
```toml
# ontology/patterns.toml
id = "next_greater_element"         # ← Doesn't contain "monotonic_stack"
api_kernel = "MonotonicStack"        # ← But belongs to MonotonicStack
```

**Issue**: Pattern ID describes problem scenarios, not technical names

**Solution**: Requires manual configuration in `kernel_mapping`

---

### Category 5: Prefix Conflict ❌ Needs Manual Configuration

| Directory Name | Pattern ID Prefix | Possible Kernels | Status |
|----------------|-------------------|------------------|--------|
| `dp_sequence` | `dp_*` | `DPSequence`, `DPInterval` | ❌ Ambiguous |
| `dp_interval` | `dp_*` | `DPSequence`, `DPInterval` | ❌ Ambiguous |

**Example**:
```toml
# ontology/patterns.toml
id = "dp_fibonacci_style"           # ← Belongs to DPSequence
api_kernel = "DPSequence"

id = "dp_palindrome"                 # ← Belongs to DPInterval
api_kernel = "DPInterval"
```

**Issue**: Both start with `dp_`, cannot distinguish by prefix

**Solution**: Requires manual configuration in `kernel_mapping` to resolve ambiguity

---

## Summary

### Why is kernel_mapping needed?

1. **Naming Inconsistency** (Categories 2-4)
   - Singular/plural: `two_pointers` vs `two_pointer_*`
   - Word order: `bfs_grid` vs `grid_bfs_*`
   - Completely missing: `monotonic_stack` vs `next_greater_element`

2. **Semantic Ambiguity** (Category 5)
   - Prefix conflict: `dp_sequence` vs `dp_interval` both match `dp_*`

3. **Design Choices**
   - Pattern ID describes problem scenarios (e.g., `next_greater_element`)
   - Directory name describes technical names (e.g., `monotonic_stack`)
   - They have different focus points

### What if naming were unified?

**Theoretically**, if:
- All Pattern IDs start with directory name
- Naming is completely consistent (including singular/plural, word order)
- No prefix conflicts

Then **most mappings can be auto-inferred**.

But **in practice**:
- Pattern ID design goal is to describe problem scenarios
- Directory name design goal is user-friendly organization
- They have different focus points, unified naming may reduce readability

### Current Solution

- ✅ **Simple cases auto-infer**: `sliding_window` → `sliding_window_*`
- ✅ **Singular/plural handling**: `two_pointers` → `two_pointer_*`
- ✅ **Complex cases manual config**: Other cases explicitly specified via `kernel_mapping`

This maintains flexibility while reducing manual configuration workload.
