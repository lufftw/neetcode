# 1125. Smallest Sufficient Team

## Problem Link
https://leetcode.com/problems/smallest-sufficient-team/

## Difficulty
Hard

## Tags
- Bitmask DP
- Set Cover
- Dynamic Programming

## Pattern
Bitmask DP - Set Cover

## API Kernel
`BitmaskDP`

## Problem Summary
Given a list of required skills and people with their skills, find the smallest team such that all required skills are covered.

## Key Insight

Represent skill coverage as bitmask:
- `dp[mask]` = minimum team to cover skills in mask
- For each person, their skills form a bitmask
- Transition: `dp[mask | person_skills] = min(dp[mask | person_skills], dp[mask] + person)`

## Template Mapping

```python
def smallestSufficientTeam(req_skills, people):
    n = len(req_skills)
    skill_to_idx = {s: i for i, s in enumerate(req_skills)}

    # Encode each person's skills as bitmask
    person_masks = []
    for skills in people:
        mask = 0
        for skill in skills:
            if skill in skill_to_idx:
                mask |= (1 << skill_to_idx[skill])
        person_masks.append(mask)

    full_mask = (1 << n) - 1

    # dp[mask] = smallest team to achieve skill mask
    dp = {0: []}

    for i, person_mask in enumerate(person_masks):
        # Iterate over copy of current states
        for mask, team in list(dp.items()):
            new_mask = mask | person_mask

            # Only update if this gives a smaller team
            if new_mask not in dp or len(dp[new_mask]) > len(team) + 1:
                dp[new_mask] = team + [i]

    return dp[full_mask]
```

## Complexity
- Time: O(2^m × n) where m = number of skills, n = number of people
- Space: O(2^m) - storing teams for each skill mask

## Why This Problem Third?

1. **Classic set cover** - NP-hard problem made tractable with bitmask DP
2. **Optimization DP** - Track minimum, not just reachability
3. **Team reconstruction** - Return actual indices, not just count

## Key Observations

1. **Skill encoding** - Map skill names to bit positions
2. **Monotonic improvement** - Only update if strictly better team found
3. **State explosion control** - m ≤ 16 constraint makes bitmask feasible

## Optimization: Prune Dominated People

```python
# Remove people whose skills are subset of another person
def prune_dominated(person_masks):
    n = len(person_masks)
    keep = [True] * n
    for i in range(n):
        for j in range(n):
            if i != j and (person_masks[i] | person_masks[j]) == person_masks[j]:
                # Person i is dominated by person j
                keep[i] = False
                break
    return [i for i in range(n) if keep[i]]
```

## Common Mistakes

1. **Mutating dict during iteration** - Use `list(dp.items())`
2. **Wrong optimization direction** - Minimize team size, not maximize skills
3. **Forgetting skill mapping** - Skills are strings, need index mapping

## Related Problems
- LC 1494: Parallel Courses II
- LC 1723: Find Minimum Time to Finish All Jobs
- LC 1986: Minimum Number of Work Sessions
