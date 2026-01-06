## Pattern Comparison

| Problem | Event Type | State Structure | Output | Sort Tie-break |
|---------|------------|-----------------|--------|----------------|
| **Meeting Rooms II** | ±1 (start/end) | Integer counter | Max count | End before start |
| **Car Pooling** | ±passengers | Integer counter | Boolean | Dropoff before pickup |
| **Skyline** | add/remove height | Sorted container | Critical points | Starts before ends |

## When to Use Each Pattern

```
Need to track overlap count?
├── Yes → Event Counting (Meeting Rooms II)
│   └── Need capacity check instead of max?
│       └── Yes → Capacity Tracking (Car Pooling)
└── No → Need to track max height?
    └── Yes → Height Tracking (Skyline)
```

## Data Structure Selection

| Requirement | Data Structure | Example |
|-------------|----------------|---------|
| Count only | Integer | Meeting Rooms II |
| Count with threshold | Integer | Car Pooling |
| Max of active set | Heap or SortedList | Skyline |
| Range queries | Segment Tree | Complex variants |

## Complexity Comparison

| Problem | Time | Space | Key Operation |
|---------|------|-------|---------------|
| Meeting Rooms II | O(n log n) | O(n) | Counter update |
| Car Pooling | O(n log n) | O(n) | Counter check |
| Skyline | O(n log n) | O(n) | Max query + deletion |
