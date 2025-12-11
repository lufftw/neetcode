# Pattern → Kernel Mapping in Ontology

## ✅ Yes, This Relationship Exists in Ontology!

### Relationship Definition Location

In `ontology/patterns.toml`, each Pattern has an `api_kernel` field:

```toml
# ontology/patterns.toml

[[patterns]]
id = "sliding_window_unique"
api_kernel = "SubstringSlidingWindow"  # ← Pattern → Kernel mapping
summary = "Window where all elements are unique."

[[patterns]]
id = "sliding_window_at_most_k_distinct"
api_kernel = "SubstringSlidingWindow"  # ← Pattern → Kernel mapping
summary = "Window with at most K distinct elements."

[[patterns]]
id = "grid_bfs_propagation"
api_kernel = "GridBFSMultiSource"  # ← Pattern → Kernel mapping
summary = "Layered BFS expansion from multiple sources on a grid."
```

---

## Relationship Structure

### Data Model

```python
# tools/patterndocs/data.py

@dataclass
class Pattern:
    """Represents a Pattern from ontology."""
    id: str                    # Pattern ID
    api_kernel: str            # ← This is the Pattern → Kernel mapping!
    summary: str
```

### Relationship Direction

```
Pattern (Many)  →  API Kernel (One)
     ↓
api_kernel field
```

**Relationship Type**: Many-to-One
- Multiple Patterns can belong to the same Kernel
- One Pattern belongs to only one Kernel

---

## How to Use This Relationship

### 1. Load Relationship

```python
# tools/patterndocs/loader.py

def load_patterns() -> dict[str, list[Pattern]]:
    """Load patterns grouped by API kernel."""
    # ...
    patterns_by_kernel: dict[str, list[Pattern]] = {}
    
    for item in data.get("patterns", []):
        pattern = Pattern(
            id=item.get("id", ""),
            api_kernel=item.get("api_kernel", ""),  # ← Read mapping relationship
            summary=item.get("summary", ""),
        )
        patterns_by_kernel.setdefault(pattern.api_kernel, []).append(pattern)
    
    return patterns_by_kernel
```

### 2. Query Relationship

```python
# Get all Patterns for a Kernel
patterns = patterns_by_kernel.get("SubstringSlidingWindow")
# → [
#     Pattern(id="sliding_window_unique", api_kernel="SubstringSlidingWindow", ...),
#     Pattern(id="sliding_window_at_most_k_distinct", api_kernel="SubstringSlidingWindow", ...),
#     ...
#   ]

# Get Kernel for a Pattern
pattern = patterns[0]
kernel_id = pattern.api_kernel
# → "SubstringSlidingWindow"
```

---

## Relationship Examples

### Example 1: SubstringSlidingWindow

```toml
# 5 Patterns all map to the same Kernel
[[patterns]]
id = "sliding_window_unique"
api_kernel = "SubstringSlidingWindow"

[[patterns]]
id = "sliding_window_at_most_k_distinct"
api_kernel = "SubstringSlidingWindow"

[[patterns]]
id = "sliding_window_freq_cover"
api_kernel = "SubstringSlidingWindow"

[[patterns]]
id = "sliding_window_cost_bounded"
api_kernel = "SubstringSlidingWindow"

[[patterns]]
id = "sliding_window_fixed_size"
api_kernel = "SubstringSlidingWindow"
```

**Relationship**: 5 Patterns → 1 Kernel (`SubstringSlidingWindow`)

### Example 2: GridBFSMultiSource

```toml
# 2 Patterns map to the same Kernel
[[patterns]]
id = "grid_bfs_propagation"
api_kernel = "GridBFSMultiSource"

[[patterns]]
id = "bfs_shortest_path"
api_kernel = "GridBFSMultiSource"
```

**Relationship**: 2 Patterns → 1 Kernel (`GridBFSMultiSource`)

---

## Difference from kernel_mapping

### Two Different Mappings

| Mapping Type | Endpoint A | Endpoint B | Location | Purpose |
|--------------|------------|------------|----------|---------|
| **Pattern → Kernel** | Pattern ID | API Kernel ID | `ontology/patterns.toml` | Describes algorithm knowledge structure |
| **Directory Name → Kernel** | Directory Name | API Kernel ID | `tools/generate_pattern_docs.toml` | Connects document organization and knowledge structure |

### Why Two Mappings?

1. **Pattern → Kernel** (in Ontology)
   - Describes: Which Patterns belong to which Kernel
   - Purpose: Build knowledge graph
   - Direction: Pattern → Kernel (many-to-one)

2. **Directory Name → Kernel** (in config file)
   - Describes: Which document directory corresponds to which Kernel
   - Purpose: Document generation tool
   - Direction: Directory Name → Kernel (one-to-one)

### Data Flow

```
1. Directory name "sliding_window"
   ↓ kernel_mapping (Directory Name → Kernel)
2. Kernel ID "SubstringSlidingWindow"
   ↓ load_patterns (Find via Pattern.api_kernel)
3. All Patterns belonging to this Kernel
   → sliding_window_unique
   → sliding_window_at_most_k_distinct
   → ...
```

---

## Summary

### ✅ Ontology Does Have Pattern → Kernel Mapping

- **Location**: `ontology/patterns.toml`
- **Field**: Each Pattern's `api_kernel` field
- **Relationship**: Many-to-one (multiple Patterns → one Kernel)
- **Purpose**: Describes algorithm knowledge structure

### ❌ But Ontology Doesn't Have Directory Name → Kernel Mapping

- **Reason**: Directory name is document organization, not algorithm knowledge
- **Solution**: `kernel_mapping` provides this mapping in config file

### 🔗 Relationship Between Two Mappings

- `kernel_mapping` connects directory name to Kernel
- Then through Pattern → Kernel relationship in Ontology, find all related Patterns
- Finally generate complete documentation
