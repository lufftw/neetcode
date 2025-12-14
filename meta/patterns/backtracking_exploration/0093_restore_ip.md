## Variation: Restore IP Addresses (LeetCode 93)

> **Problem**: Return all valid IP addresses that can be formed from a digit string.  
> **Sub-Pattern**: String segmentation with multi-constraint validity.  
> **Key Insight**: Fixed 4 segments, each 1-3 digits, value 0-255, no leading zeros.

### Implementation

```python
def restore_ip_addresses(s: str) -> list[str]:
    """
    Generate all valid IP addresses from a digit string.
    
    Constraints per segment:
    1. Length: 1-3 characters
    2. Value: 0-255
    3. No leading zeros (except "0" itself)
    
    Algorithm:
    - Exactly 4 segments required
    - Try 1, 2, or 3 characters for each segment
    - Validate each segment before proceeding
    
    Pruning:
    - Early termination if remaining chars can't form remaining segments
    - Min remaining = segments_left × 1
    - Max remaining = segments_left × 3
    
    Time Complexity: O(3^4 × n) = O(81 × n) = O(n)
        - At most 3 choices per segment, 4 segments
        - O(n) to validate/copy
    
    Space Complexity: O(4) = O(1) for path
    
    Args:
        s: String of digits
        
    Returns:
        All valid IP addresses
    """
    results: list[str] = []
    segments: list[str] = []
    n = len(s)
    
    def is_valid_segment(segment: str) -> bool:
        """Check if segment is a valid IP octet."""
        if not segment:
            return False
        if len(segment) > 1 and segment[0] == '0':
            return False  # No leading zeros
        if int(segment) > 255:
            return False
        return True
    
    def backtrack(start: int, segment_count: int) -> None:
        # PRUNING: Check remaining length bounds
        remaining = n - start
        remaining_segments = 4 - segment_count
        
        if remaining < remaining_segments:  # Too few chars
            return
        if remaining > remaining_segments * 3:  # Too many chars
            return
        
        # BASE CASE: 4 segments formed
        if segment_count == 4:
            if start == n:  # Used all characters
                results.append('.'.join(segments))
            return
        
        # Try 1, 2, or 3 character segments
        for length in range(1, 4):
            if start + length > n:
                break
            
            segment = s[start:start + length]
            
            if not is_valid_segment(segment):
                continue
            
            segments.append(segment)
            backtrack(start + length, segment_count + 1)
            segments.pop()
    
    backtrack(0, 0)
    return results
```

