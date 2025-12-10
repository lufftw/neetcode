## Template Quick Reference

### Maximize Window (Variable Size)

```python
def maximize_window(sequence):
    state = {}
    left = 0
    max_result = 0
    
    for right, elem in enumerate(sequence):
        # Expand
        add_to_state(state, elem)
        
        # Contract while invalid
        while not is_valid(state):
            remove_from_state(state, sequence[left])
            left += 1
        
        # Update answer
        max_result = max(max_result, right - left + 1)
    
    return max_result
```

### Minimize Window (Variable Size)

```python
def minimize_window(sequence):
    state = {}
    left = 0
    min_result = float('inf')
    
    for right, elem in enumerate(sequence):
        # Expand
        add_to_state(state, elem)
        
        # Contract while valid (to minimize)
        while is_valid(state):
            min_result = min(min_result, right - left + 1)
            remove_from_state(state, sequence[left])
            left += 1
    
    return min_result if min_result != float('inf') else 0
```

### Fixed Size Window

```python
def fixed_window(sequence, k):
    state = {}
    result = []
    
    for right, elem in enumerate(sequence):
        # Expand
        add_to_state(state, elem)
        
        # Contract when window exceeds k
        if right >= k:
            remove_from_state(state, sequence[right - k])
        
        # Check condition when window is exactly k
        if right >= k - 1 and is_valid(state):
            result.append(process(state))
    
    return result
```


