# Ontology Relationships vs kernel_mapping

## Key Differences

### Relationships in Ontology

#### ✅ Pattern → Kernel (Exists)

In `ontology/patterns.toml`:

```toml
[[patterns]]
id = "sliding_window_unique"
api_kernel = "SubstringSlidingWindow"  # ← Pattern links to Kernel
summary = "Window where all elements are unique."

[[patterns]]
id = "sliding_window_at_most_k_distinct"
api_kernel = "SubstringSlidingWindow"  # ← Pattern links to Kernel
summary = "Window with at most K distinct elements."
```

**Relationship**: `Pattern.api_kernel` → `APIKernel.id`

**Direction**: Pattern → Kernel (many-to-one)

**Purpose**: Describes which API Kernel each Pattern belongs to

---

### Relationship Made by kernel_mapping

#### ❌ Directory Name → Kernel (Not in Ontology)

In `tools/generate_pattern_docs.toml`:

```toml
[kernel_mapping]
sliding_window = "SubstringSlidingWindow"  # ← Directory name links to Kernel
two_pointers = "TwoPointersTraversal"      # ← Directory name links to Kernel
```

**Relationship**: `Directory Name` → `APIKernel.id`

**Direction**: Directory Name → Kernel (one-to-one)

**Purpose**: Connects document directory to knowledge structure

---

## Comparison Table

| Relationship Type | Endpoint A | Endpoint B | Location | Exists? |
|-------------------|------------|------------|----------|---------|
| **Pattern → Kernel** | Pattern ID | API Kernel ID | `ontology/patterns.toml` | ✅ Exists |
| **Directory Name → Kernel** | Directory Name | API Kernel ID | `tools/generate_pattern_docs.toml` | ❌ Not in Ontology |

---

## Why No Directory Name → Kernel in Ontology?

### Reason: Separation of Concerns

1. **Ontology Describes Algorithm Knowledge**
   - API Kernels: Algorithm core definitions
   - Patterns: Specific application patterns
   - Pattern → Kernel: Knowledge structure relationships

2. **Directory Name is Document Organization**
   - Not part of algorithm knowledge itself
   - Tool-level organization method
   - Should not be mixed into Ontology

### Analogy

Like:
- **Book Classification System** (Ontology): Describes knowledge classification of books
- **Bookshelf Location** (Directory Name): Describes physical storage location of books
- **Bookshelf Location → Classification Number** (kernel_mapping): Connects physical organization and knowledge classification

---

## Data Flow Example

### Scenario: Generate `sliding_window.md` Document

```
1. Input: Directory name "sliding_window"
   ↓
2. kernel_mapping lookup:
   "sliding_window" → "SubstringSlidingWindow"
   ↓
3. Get Kernel info from Ontology:
   api_kernels.toml: SubstringSlidingWindow
   → summary: "1D window state machine..."
   ↓
4. Get related Patterns from Ontology:
   patterns.toml: Find all with api_kernel = "SubstringSlidingWindow"
   → sliding_window_unique
   → sliding_window_at_most_k_distinct
   → sliding_window_freq_cover
   → ...
   ↓
5. Compose document
```

---

## Summary

### What's in Ontology?

✅ **Pattern → Kernel Relationship**
- Each Pattern links to Kernel via `api_kernel` field
- This is part of algorithm knowledge structure

### What does kernel_mapping do?

❌ **Not Pattern → Kernel** (that's already in Ontology)

✅ **Directory Name → Kernel**
- Connects document directory to knowledge structure
- This is a tool-level mapping, not part of Ontology

### Why is kernel_mapping needed?

Because Ontology doesn't record **document directory names**, only:
- API Kernel IDs (algorithm identifiers)
- Pattern IDs (application pattern identifiers)

But document generation needs:
- Find corresponding Kernel from directory name
- Then get Kernel details from Ontology
