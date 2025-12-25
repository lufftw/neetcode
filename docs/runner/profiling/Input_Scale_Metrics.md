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

* Are displayed as parameters.
* Are **not** treated as scale metrics.

Example:

```
Input Scale: n = 100000
Parameters: k = 50
```

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