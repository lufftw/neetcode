# Ontology Solution Analysis

## Problem Review

Mapping from directory name (`meta/patterns/<dir_name>/`) to API Kernel ID requires manual configuration.

## Possible Ontology Improvement Solutions

### Solution 1: Add `doc_directory` Field to `api_kernels.toml`

```toml
[[api_kernels]]
id = "SubstringSlidingWindow"
summary = "1D window state machine over sequences with dynamic invariants."
doc_directory = "sliding_window"  # New field

[[api_kernels]]
id = "TwoPointersTraversal"
summary = "Traverse sequence with two coordinated pointers..."
doc_directory = "two_pointers"  # New field
```

**Advantages**:
- ✅ Clear: Each API Kernel directly specifies corresponding document directory
- ✅ Centralized: Mapping relationship in ontology, maintained with knowledge structure
- ✅ Verifiable: Can check if directory exists

**Disadvantages**:
- ❌ Mixed concerns: API Kernel is algorithm core, `doc_directory` is document organization
- ❌ One-to-many issue: One API Kernel may correspond to multiple document directories (though not currently)
- ❌ Reverse dependency: API Kernel definition shouldn't depend on document structure

**Assessment**: ⚠️ Feasible, but mixes different levels of concerns

---

### Solution 2: Add `doc_directory` Field to `patterns.toml`

```toml
[[patterns]]
id = "sliding_window_unique"
api_kernel = "SubstringSlidingWindow"
summary = "Window where all elements are unique."
doc_directory = "sliding_window"  # New field
```

**Advantages**:
- ✅ Finer granularity: Each pattern can specify document directory
- ✅ Flexibility: Different patterns can go to different directories

**Disadvantages**:
- ❌ Redundancy: Multiple patterns of same API Kernel need repeated specification
- ❌ Inconsistency risk: Patterns of same Kernel may specify different directories
- ❌ More complex: Need to aggregate patterns to determine directory's Kernel

**Assessment**: ⚠️ Feasible, but may cause inconsistency

---

### Solution 3: Create New Mapping File `ontology/doc_mapping.toml`

```toml
# Documentation Directory Mapping
# Maps documentation directory names to API Kernel IDs

[directory_to_kernel]
sliding_window = "SubstringSlidingWindow"
two_pointers = "TwoPointersTraversal"
bfs_grid = "GridBFSMultiSource"
# ...
```

**Advantages**:
- ✅ Separation of concerns: Mapping relationship independent of algorithm definitions
- ✅ Clear: Specifically for document organization mapping
- ✅ Maintainable: Centralized management of all mapping relationships

**Disadvantages**:
- ❌ Still manual configuration (but this is necessary)
- ❌ Requires additional file

**Assessment**: ✅ Best solution, maintains separation of concerns

---

### Solution 4: Add `aliases` Field to `api_kernels.toml`

```toml
[[api_kernels]]
id = "SubstringSlidingWindow"
summary = "1D window state machine over sequences with dynamic invariants."
aliases = ["sliding_window", "sliding-window"]  # New field
```

**Advantages**:
- ✅ Semantically clear: aliases are API Kernel aliases
- ✅ Flexible: Supports multiple aliases

**Disadvantages**:
- ❌ Still needs reverse lookup: From directory name to Kernel
- ❌ One-to-many issue: Multiple Kernels may have same alias

**Assessment**: ⚠️ Feasible, but requires additional lookup logic

---

## Recommended Solution: Solution 3 + Current Config Approach

### Why Recommend Solution 3?

1. **Separation of Concerns**
   - Ontology describes algorithm knowledge structure
   - Mapping file describes document organization
   - They are different levels of concerns

2. **Maintainability**
   - Mapping relationships centralized in one file
   - Doesn't affect ontology core structure
   - Easy to understand and modify

3. **Flexibility**
   - Can support one-to-many mappings (future)
   - Can add metadata (e.g., priority, description)

### But Current Solution Is Already Good Enough

Current `tools/generate_pattern_docs.toml` already achieves Solution 3's effect:

```toml
[kernel_mapping]
sliding_window = "SubstringSlidingWindow"
two_pointers = "TwoPointersTraversal"
```

**Advantages**:
- ✅ Already in use, no refactoring needed
- ✅ Together with tool config, fits tool usage scenario
- ✅ Can include other configs (paths, file ordering)

---

## Conclusion

### Should It Be Added to Ontology?

**Not Recommended**, reasons:

1. **Different Conceptual Levels**
   - Ontology describes "what algorithms are" (knowledge structure)
   - Mapping relationships describe "how documents are organized" (organization method)
   - Mixing them reduces ontology purity

2. **Not Ontology's Responsibility**
   - Ontology should focus on algorithm knowledge itself
   - Document organization is tool-level concern
   - Maintaining separation of concerns is clearer

3. **Current Solution Is Sufficient**
   - `generate_pattern_docs.toml` already provides clear mapping
   - No additional abstraction layer needed
   - Manual configuration is necessary as it involves semantic decisions

### If Must Add to Ontology

If tighter integration is needed in the future, consider:

1. **Add `doc_directory` to `api_kernels.toml`** (Solution 1)
   - As optional field
   - Tool uses it first, falls back to config file if missing

2. **Create `ontology/doc_mapping.toml`** (Solution 3)
   - As part of ontology
   - But clearly labeled as "document organization mapping", not core knowledge

### Final Recommendation

**Keep Current Solution**:
- ✅ Manual configuration in `generate_pattern_docs.toml`
- ✅ Simple auto-inference as supplement (exact matching)
- ✅ Maintain ontology purity
- ✅ Clear separation of concerns

Mapping relationships involve **semantic decisions** and should be explicitly specified by humans, not auto-inferred.
