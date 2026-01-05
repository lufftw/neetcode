## Base Template: Kth Largest Element (LeetCode 215)

> **Problem**: Find the kth largest element in an unsorted array.
> **Invariant**: Min-heap of size k contains the k largest elements; root is the kth largest.
> **Role**: BASE TEMPLATE for `HeapTopK` API Kernel.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "kth largest/smallest" | → Heap of size k |
| "without sorting" | → Quickselect or heap |
| "stream of numbers" | → Online algorithm with heap |

### Implementation

```python
# Pattern: heap_kth_element
# See: docs/patterns/heap/templates.md Section 1 (Base Template)

class SolutionHeap:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        Find kth largest using min-heap of size k.

        Key Insight:
        - Maintain k largest elements seen so far in a min-heap
        - Root of min-heap = smallest of the k largest = kth largest

        Why min-heap for max problem?
        - When new element > root, it belongs in top-k
        - Replace root (smallest of k largest) with new element
        - After n elements, root is exactly the kth largest
        """
        import heapq

        # Min-heap stores k largest elements
        min_heap: list[int] = []

        for num in nums:
            if len(min_heap) < k:
                # Phase 1: Fill heap until size k
                heapq.heappush(min_heap, num)
            elif num > min_heap[0]:
                # Phase 2: New element larger than kth largest
                # Replace the current kth largest
                heapq.heapreplace(min_heap, num)

        # Root is the kth largest element
        return min_heap[0]
```

### Trace Example

```
Input: nums = [3, 2, 1, 5, 6, 4], k = 2

Step-by-step heap evolution:
num=3: heap=[3]          (fill phase, size < k)
num=2: heap=[2, 3]       (fill phase, size = k)
num=1: heap=[2, 3]       (1 < 2, skip)
num=5: heap=[3, 5]       (5 > 2, replace root)
num=6: heap=[5, 6]       (6 > 3, replace root)
num=4: heap=[5, 6]       (4 < 5, skip)

Result: heap[0] = 5 (2nd largest)

Visual verification:
Sorted descending: [6, 5, 4, 3, 2, 1]
                       ↑
                   2nd largest = 5 ✓
```

### Alternative: Quickselect

```python
class SolutionQuickselect:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        Quickselect algorithm: O(n) average, O(n²) worst.

        Partition-based selection without full sorting.
        Use random pivot to avoid worst-case on sorted input.
        """
        import random

        target_idx = k - 1  # kth largest at index k-1 in descending order

        def partition(left: int, right: int) -> int:
            # Random pivot to avoid O(n²) on sorted arrays
            pivot_idx = random.randint(left, right)
            pivot_val = nums[pivot_idx]
            nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

            store_idx = left
            for i in range(left, right):
                if nums[i] >= pivot_val:  # >= for descending order
                    nums[store_idx], nums[i] = nums[i], nums[store_idx]
                    store_idx += 1

            nums[store_idx], nums[right] = nums[right], nums[store_idx]
            return store_idx

        left, right = 0, len(nums) - 1
        while left <= right:
            pivot_idx = partition(left, right)
            if pivot_idx == target_idx:
                return nums[pivot_idx]
            elif pivot_idx < target_idx:
                left = pivot_idx + 1
            else:
                right = pivot_idx - 1

        return nums[left]
```

### Complexity Comparison

| Approach | Time (Average) | Time (Worst) | Space |
|----------|----------------|--------------|-------|
| Min-heap size k | O(n log k) | O(n log k) | O(k) |
| Quickselect | O(n) | O(n²) | O(1) |
| Sorting | O(n log n) | O(n log n) | O(n) |

### When to Use Each

| Scenario | Best Approach |
|----------|---------------|
| k is small (k << n) | Min-heap O(n log k) ≈ O(n) |
| k ≈ n/2 | Quickselect O(n) |
| Need top-k elements, not just kth | Min-heap |
| Streaming data | Min-heap (online algorithm) |
| Memory constrained | Quickselect (in-place) |


