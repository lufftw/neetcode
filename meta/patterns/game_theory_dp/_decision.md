## Decision Flowchart

```
START: Two-player optimal game
│
├── What are players choosing from?
│   │
│   ├── Array elements from ENDS
│   │   │
│   │   ├── Even length array?
│   │   │   └── Stone Game (877) - return True
│   │   │
│   │   └── Any length array?
│   │       └── Predict Winner (486)
│   │           ├── State: (left, right) interval
│   │           └── diff >= 0 means P1 wins
│   │
│   ├── Array elements from FRONT
│   │   │
│   │   ├── Variable choices (1 to 2*M)?
│   │   │   └── Stone Game II (1140)
│   │   │       ├── State: (start, M)
│   │   │       └── Use suffix sums
│   │   │
│   │   └── Fixed choices (1, 2, or 3)?
│   │       └── Stone Game III (1406)
│   │           ├── State: start index only
│   │           └── O(1) space possible
│   │
│   └── Pool of items (no reuse)?
│       └── Can I Win (464)
│           ├── State: bitmask of used items
│           └── Win if reach target first
│
└── How to track outcome?
    │
    ├── Score difference (most common)
    │   └── dp = gain - dp(next_state)
    │
    ├── Win/Lose boolean
    │   └── can_win = any(not opponent_can_win)
    │
    └── Direct score with suffix sum
        └── my_score = suffix[start] - opponent_score
```

## Quick Selection Table

| Clue in Problem | Pattern |
|-----------------|---------|
| "take from either end" | Interval DP (877, 486) |
| "take 1-3 from front" | Linear DP (1406) |
| "take 1 to 2M" | State (start, M) (1140) |
| "each number once" | Bitmask DP (464) |
| "even number of piles" | Math: always True (877) |
| "reach target first" | Win/Lose tracking (464) |
| "maximize score" | Score difference DP |
