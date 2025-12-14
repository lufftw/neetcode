## Pattern Comparison Table

| Problem | Sub-Pattern | State | Dedup Strategy | Pruning |
|---------|-------------|-------|----------------|---------|
| Permutations (46) | Permutation | used[] | None (distinct) | None |
| Permutations II (47) | Permutation | used[] | Sort + level skip | Same-level |
| Subsets (78) | Subset | start_idx | Index ordering | None |
| Subsets II (90) | Subset | start_idx | Sort + level skip | Same-level |
| Combinations (77) | Combination | start_idx | Index ordering | Count bound |
| Combination Sum (39) | Target Search | start_idx | None (distinct) | Target bound |
| Combination Sum II (40) | Target Search | start_idx | Sort + level skip | Target + level |
| Combination Sum III (216) | Target Search | start_idx | None (1-9 distinct) | Count + target |
| N-Queens (51) | Constraint | constraint sets | Row-by-row | Constraints |
| Palindrome Part. (131) | Segmentation | start_idx | None | Validity check |
| IP Addresses (93) | Segmentation | start_idx, count | None | Length bounds |
| Word Search (79) | Grid Path | visited | Path uniqueness | Boundary + char |

