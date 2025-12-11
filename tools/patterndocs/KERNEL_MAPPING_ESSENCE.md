# The Essence of Kernel Mapping

## Core Question: What is `kernel_mapping` associating?

### Two Endpoints Being Associated

```
┌─────────────────────────────────┐
│  Document Organization Layer     │
│  meta/patterns/sliding_window/ │
│  (Physical location in FS)       │
└──────────────┬──────────────────┘
               │ kernel_mapping
               │ (Bridge)
               ▼
┌─────────────────────────────────┐
│  Knowledge Structure Layer       │
│  ontology/api_kernels.toml       │
│  SubstringSlidingWindow          │
│  (Logical identifier of algo)   │
└─────────────────────────────────┘
```

### Specific Association Content

#### 1. **Physical Location** ↔ **Logical Identifier**

| Endpoint A | Endpoint B | Association Type |
|------------|------------|-----------------|
| `meta/patterns/sliding_window/` | `SubstringSlidingWindow` | Document Directory → API Kernel ID |
| Directory name in file system | Algorithm core identifier in Ontology | Physical Organization → Knowledge Structure |

#### 2. **Document Content** ↔ **Algorithm Knowledge**

Through this association, the system can:

1. **Get Algorithm Metadata**
   ```python
   kernel_id = get_kernel_id_from_dir_name("sliding_window")
   # → "SubstringSlidingWindow"
   
   kernel = kernels.get(kernel_id)
   kernel_summary = kernel.summary
   # → "1D window state machine over sequences with dynamic invariants."
   ```

2. **Get Related Patterns**
   ```python
   patterns = patterns_by_kernel.get(kernel_id)
   # → All patterns belonging to SubstringSlidingWindow
   ```

3. **Generate Document Attribution**
   ```markdown
   > **API Kernel**: `SubstringSlidingWindow`
   > **Core Mechanism**: Maintain a dynamic window...
   ```

## Why Is This Association Needed?

### Problem: Two Independent Systems

1. **Document Organization System** (`meta/patterns/`)
   - Organized by teaching needs
   - User-friendly directory names
   - Physical locations in file system

2. **Knowledge Structure System** (`ontology/`)
   - Organized by algorithm essence
   - Technical precise identifiers
   - Logical knowledge graph

### Solution: Bridge Mapping

`kernel_mapping` is a **bridge** connecting two systems:

```
Document Generation Flow:
1. User specifies directory name: "sliding_window"
2. kernel_mapping lookup: "sliding_window" → "SubstringSlidingWindow"
3. Get from ontology: API Kernel info and related Patterns
4. Compose document: Includes correct attribution and knowledge structure info
```

## The Essence of Association

### This Is Not Simple "Renaming"

Not:
- ❌ Simple conversion from directory name → API Kernel ID
- ❌ String mapping

But:
- ✅ **Bridge between two abstraction layers**
- ✅ **Association of Physical Organization ↔ Logical Knowledge**
- ✅ **Connection of Document System ↔ Knowledge System**

### Understanding Through Analogy

Like:
- **Library bookshelf location** (physical organization) ↔ **Book classification number** (knowledge classification)
- **File path** (storage location) ↔ **Namespace** (logical organization)
- **Folder name** (organization method) ↔ **Concept identifier** (semantic identifier)

## Real-World Usage Scenarios

### Scenario 1: Generate Document

```python
# Input: Directory name
pattern_name = "sliding_window"

# Get API Kernel ID via kernel_mapping
kernel_id = get_kernel_id_from_dir_name(pattern_name)
# → "SubstringSlidingWindow"

# Get knowledge from ontology
kernel = kernels.get(kernel_id)
patterns = patterns_by_kernel.get(kernel_id)

# Generate document (includes correct attribution)
document = compose_document(config, ...)
# → Document includes: "API Kernel: SubstringSlidingWindow"
```

### Scenario 2: Verify Consistency

```python
# Check if directory has corresponding API Kernel
kernel_id = get_kernel_id_from_dir_name("sliding_window")
if kernel_id not in kernels:
    print(f"Warning: Kernel '{kernel_id}' not found")
```

### Scenario 3: Knowledge Graph Connection

```python
# Find knowledge structure via directory name
dir_name = "sliding_window"
kernel_id = kernel_mapping[dir_name]
# → "SubstringSlidingWindow"

# Can further query:
# - What Patterns does this Kernel have?
# - What problems do these Patterns correspond to?
# - What knowledge families do these problems belong to?
```

## Summary

`kernel_mapping` associates:

1. **Physical Layer** (directories in file system)
   ↓
2. **Logical Layer** (algorithm knowledge in Ontology)

**Essence**: A **bridge mapping** connecting two independent systems: document organization and knowledge structure.

**Purpose**: Enable document generation tools to:
- Find document source files from file system
- Find corresponding algorithm information from knowledge graph
- Combine both to generate complete documents

**Importance**: Without this association, document generation tools cannot know:
- Which algorithm core does this directory correspond to?
- What attribution should be displayed?
- Which related Patterns should be associated?
