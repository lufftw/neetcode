# Sliding Window Patterns: Complete Reference

> **API Kernel**: `SubstringSlidingWindow`  
> **Core Mechanism**: Maintain a dynamic window `[left, right]` over a sequence while preserving an invariant.

This document presents the **canonical sliding window template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Core Concepts

### The Sliding Window Invariant

Every sliding window algorithm maintains an **invariant** — a condition that must always be true for the current window `[left, right]`.

```
Window State:
┌─────────────────────────────────────────┐
│  ... [ left ─────── window ─────── right ] ...  │
│       └─────── invariant holds ───────┘         │
└─────────────────────────────────────────┘
```

### Universal Template Structure

```python
def sliding_window_template(sequence):
    """
    Generic sliding window template.
    
    Key components:
    1. State: Data structure tracking window contents
    2. Invariant: Condition that must hold for valid window
    3. Expand: Always move right pointer forward
    4. Contract: Move left pointer to restore invariant
    5. Update: Record answer when window is valid
    """
    state = initialize_state()
    left = 0
    answer = initial_answer()
    
    for right, element in enumerate(sequence):
        # EXPAND: Add element at right to window state
        update_state_add(state, element)
        
        # CONTRACT: Shrink window until invariant is restored
        while invariant_violated(state):
            update_state_remove(state, sequence[left])
            left += 1
        
        # UPDATE: Record answer for current valid window
        answer = update_answer(answer, left, right)
    
    return answer
```

### Two Window Strategies

| Strategy | When to Use | Example Problems |
|----------|-------------|------------------|
| **Maximize Window** | Find longest/largest valid window | LeetCode 3, 340, 424 |
| **Minimize Window** | Find shortest valid window | LeetCode 76, 209 |


