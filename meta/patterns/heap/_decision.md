---

## Decision Flowchart

Use this flowchart to determine which heap pattern applies:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HEAP PATTERN SELECTION                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │ What are you finding/doing?   │
                    └───────────────────────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
   ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
   │ Kth element  │         │   Merging    │         │  Scheduling  │
   │ or Top-K     │         │   sorted     │         │  or greedy   │
   └──────────────┘         └──────────────┘         └──────────────┘
          │                         │                         │
          ▼                         ▼                         ▼
   ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
   │ Static or    │         │ How many     │         │ What type?   │
   │ streaming?   │         │ sequences?   │         └──────────────┘
   └──────────────┘         └──────────────┘                 │
          │                         │               ┌────────┼────────┐
    ┌─────┴─────┐             ┌─────┴─────┐         │        │        │
    │           │             │           │         ▼        ▼        ▼
    ▼           ▼             ▼           ▼      Interval  Task    Repeated
 Static    Streaming       k = 2       k > 2    overlap  cooldown  largest
    │           │             │           │         │        │        │
    ▼           ▼             ▼           ▼         ▼        ▼        ▼
┌────────┐ ┌────────┐   ┌────────┐  ┌────────┐ ┌────────┐┌────────┐┌────────┐
│heap_   │ │heap_   │   │two     │  │merge_k │ │heap_   ││heap_   ││heap_   │
│kth_    │ │median_ │   │pointer │  │_sorted_│ │interval││task_   ││greedy_ │
│element │ │stream  │   │merge   │  │heap    │ │schedule││schedule││sim     │
│        │ │        │   │        │  │        │ │        ││r       ││        │
│LC 215  │ │LC 295  │   │LC 21   │  │LC 23   │ │LC 253  ││LC 621  ││LC 1046 │
│LC 347  │ │        │   │LC 88   │  │        │ │        ││        ││        │
└────────┘ └────────┘   └────────┘  └────────┘ └────────┘└────────┘└────────┘
```

### Quick Decision Table

| Clue in Problem | Pattern | Key Data Structure |
|-----------------|---------|-------------------|
| "kth largest/smallest" | heap_kth_element | Min-heap size k |
| "top k frequent" | heap_top_k | Min-heap + frequency map |
| "running/streaming median" | heap_median_stream | Two heaps (max + min) |
| "merge k sorted" | merge_k_sorted_heap | Min-heap of heads |
| "minimum rooms/resources" | heap_interval_scheduling | Min-heap of end times |
| "schedule with cooldown" | heap_task_scheduler | Max-heap + cooldown queue |
| "repeatedly process largest" | heap_greedy_simulation | Max-heap |

### Pattern Checklist

Before implementing, verify:

- [ ] **Is heap the right choice?**
  - Need repeated access to min/max? → Heap
  - Need kth element only once? → Consider quickselect
  - Need all elements sorted? → Just sort

- [ ] **Which heap type?**
  - Finding largest/max → Min-heap of size k
  - Finding smallest/min → Max-heap of size k
  - Merging sorted → Min-heap
  - Greedy simulation → Max or min depending on problem

- [ ] **Edge cases identified?**
  - Empty input
  - k > n elements
  - Duplicate values
  - Tie-breaking rules


