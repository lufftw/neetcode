## Template Quick Reference

### Permutation Template

```python
def permute(nums):
    results = []
    used = [False] * len(nums)
    
    def backtrack(path):
        if len(path) == len(nums):
            results.append(path[:])
            return
        
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False
    
    backtrack([])
    return results
```

### Subset/Combination Template

```python
def subsets(nums):
    results = []
    
    def backtrack(start, path):
        results.append(path[:])  # Collect at every node
        
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)  # i+1 for no reuse
            path.pop()
    
    backtrack(0, [])
    return results
```

### Target Sum Template

```python
def combination_sum(candidates, target):
    results = []
    
    def backtrack(start, path, remaining):
        if remaining == 0:
            results.append(path[:])
            return
        if remaining < 0:
            return
        
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i for reuse
            path.pop()
    
    backtrack(0, [], target)
    return results
```

### Grid Search Template

```python
def grid_search(grid, word):
    rows, cols = len(grid), len(grid[0])
    
    def backtrack(r, c, index):
        if index == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if grid[r][c] != word[index]:
            return False
        
        temp = grid[r][c]
        grid[r][c] = '#'
        
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            if backtrack(r + dr, c + dc, index + 1):
                grid[r][c] = temp
                return True
        
        grid[r][c] = temp
        return False
    
    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False

```

