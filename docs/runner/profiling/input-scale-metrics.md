> **Purpose**
> Define how problem scale (e.g. n, m, V, E) is estimated from method signatures, and how the system behaves when such estimation is not possible.

---

## 1. Conceptual Separation

This project treats **problem scale** and **memory size** as distinct concepts.

| Concept                  | Meaning                           |
| ------------------------ | --------------------------------- |
| Input Scale (n, m, V, E) | Structural size of the problem    |
| Signature Payload (MB)   | Memory footprint of input objects |
| Input Bytes (MB)         | Raw size of stdin data            |

No conversion is performed between these values.

---

## 1.1 Display Format (PyTorch-style)

Input Scale uses a **PyTorch-inspired shape notation**:

| Type | Notation | Example | Description |
|------|----------|---------|-------------|
| 1D array | `[a]` | `s:[8]` | Length 8 |
| 2D matrix | `[a,b]` | `matrix:[3,4]` | 3 rows × 4 cols |
| 3D tensor | `[a,b,c]` | `tensor:[2,3,4]` | 3D shape |
| k-lists | `[k] n=N` | `lists:[3] n=8` | 3 lists, 8 total elements |
| Scalar | (skipped) | — | Not displayed |

**Legend (displayed once at end of output):**
```
Input Scale Legend:
  [a]     = 1D length
  [a,b]   = 2D shape (rows×cols)
  [a,b,c] = 3D shape
  n       = total elements
```

### Implementation

Shape is inferred from actual parameter values in the subprocess using:
1. `inspect.signature()` to get method parameter names
2. `inspect.currentframe().f_locals` to get actual values
3. `_compute_shape()` to derive PyTorch-style shape

This approach leverages Python's introspection rather than text parsing.

---

## 2. Input Scale Metrics

**Definition**

Input Scale Metrics describe the **cardinality or structure** of the input, such as:

* number of elements,
* number of nodes or edges,
* dimensionality.

They are derived from **structured signature objects** only.

---

## 3. Availability Rules & Fallbacks

### 3.1 Signature Available (In-process)

When method signature objects are available:

* Input Scale is computed from object structure.
* Signature Payload may be computed.
* Input Bytes are still reported for completeness.

Example:

```
Input Scale: n = 100000
Signature Payload: 6.8 MB
Input Bytes: 0.9 MB
```

---

### 3.2 Signature Unavailable (Subprocess / stdin-only)

When signature objects cannot be inspected:

* Input Scale is reported as `N/A`.
* Signature Payload is reported as `N/A`.
* Input Bytes are used as the sole size indicator.

Example:

```
Input Scale: N/A (signature unavailable)
Signature Payload: N/A
Input Bytes: 0.9 MB
```

This guarantees **graceful degradation** without inference or guessing.

---

## 4. Standard Input Scale Cases

Below are canonical mappings from common problem signatures to scale metrics.

### 4.1 One-dimensional Array / String

* `nums: List[int]`, `s: str`
* Scale: `n = len(...)`

---

### 4.2 Two Arrays

* `a: List[int], b: List[int]`
* Scale: `n = len(a)`, `m = len(b)`

---

### 4.3 List of Lists (k arrays)

* `lists: List[List[int]]`
* Scale:

  * `k = len(lists)`
  * `n = sum(len(x) for x in lists)`

---

### 4.4 Matrix / Grid

* `grid: List[List[int]]`
* Scale:

  * `rows = len(grid)`
  * `cols = len(grid[0])`
  * `n = rows * cols`

---

### 4.5 Linked List

* `head: ListNode`
* Scale:

  * `nodes = number of nodes`

---

### 4.6 Tree (Binary / N-ary)

* `root: TreeNode`
* Scale:

  * `nodes`
  * (optional) `height`, `leaves`

---

### 4.7 Graph — Edge List

* `edges: List[Tuple[int, int]]`
* Scale:

  * `E = len(edges)`
  * `V = number of unique vertices`

---

### 4.8 Graph — Adjacency List

* `graph: Dict[node, List[node]]`
* Scale:

  * `V = len(graph)`
  * `E = sum(len(adj))`

---

### 4.9 Intervals

* `intervals: List[List[int]]`
* Scale:

  * `n = len(intervals)`

---

### 4.10 Points / Coordinates

* `points: List[List[int]]`
* Scale:

  * `n = len(points)`
  * `d = dimension`

---

### 4.11 Dictionary / Frequency Map

* `counts: Dict[Any, int]`
* Scale:

  * `u = number of unique keys`
  * (optional) `n = sum(values)`

---

## 5. Scalars and Non-scale Parameters

Scalar parameters (`k`, `target`, `threshold`, etc.):

* Are **skipped** in Input Scale display (shape = `[]` in PyTorch terms).
* Do not contribute to the "scale" of the problem.
* Only array-like inputs (lists, matrices, trees, graphs) are displayed.

Example:

```
Input Scale: nums:[100] n=100
```

Note: Scalar parameters like `target=5` are not shown because they don't
represent the computational scale of the problem.

---

## 6. Display Order (Consistent Across CLI)

Always display in the following order:

1. Input Scale (or N/A)
2. Signature Payload (or N/A)
3. Input Bytes

---

## 7. Design Guarantee

> Input Scale metrics are derived only from explicit structure and never inferred from memory size or byte counts.

---