## Algorithm Comparison

| Aspect | Stone Game (877) | Predict Winner (486) | Can I Win (464) | Stone Game II (1140) | Stone Game III (1406) |
|--------|------------------|----------------------|-----------------|----------------------|----------------------|
| State | (i, j) interval | (i, j) interval | bitmask | (start, M) | start index |
| Choices | Left or right | Left or right | Any unused | 1 to 2*M | 1, 2, or 3 |
| Values | Positive | Any | Fixed 1..n | Positive | Any |
| Win Condition | diff > 0 | diff >= 0 | reach target | max stones | diff comparison |
| Time | O(n²) | O(n²) | O(2^n * n) | O(n³) | O(n) |
| Space | O(n²) | O(n²) | O(2^n) | O(n²) | O(1) optimized |

## Pattern Selection Guide

```
Two-player game?
├── Taking from array ends?
│   ├── Even elements only → Stone Game (877) - always True
│   └── Any elements → Predict Winner (486)
├── Taking from array front?
│   ├── Variable amount based on M → Stone Game II (1140)
│   └── Fixed 1,2,3 choices → Stone Game III (1406)
└── Selecting from pool (no reuse)?
    └── Can I Win (464) - bitmask DP
```

## Key Technique Comparison

| Technique | When to Use |
|-----------|-------------|
| Interval DP (i, j) | Taking from either end |
| Linear DP (start) | Taking from one end only |
| Bitmask DP | Selecting items without reuse |
| Math solution | Special structure (even piles) |

## Score Tracking Methods

1. **Score Difference**: `dp = my_gain - dp(next_state)`
   - Used in: 877, 486, 1406
   - Positive = current player wins

2. **Direct Score**: `my_score = suffix_sum - opponent_score`
   - Used in: 1140
   - Track actual stones, not difference

3. **Win/Lose Boolean**: `can_win = any move leads to opponent losing`
   - Used in: 464
   - True = current player can force win
