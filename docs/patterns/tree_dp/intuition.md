# Tree DP - Intuition Guide

## The Mental Model: A Family Inheritance Decision

Imagine a family tree where each person has some wealth. You're the family advisor helping them make inheritance decisions, but there's a catch: **if a parent takes an inheritance, their children can't, and vice versa** (they're too proud to both claim it).

Your job: maximize the total wealth the family keeps.

```
       Grandpa ($3)
        /       \
   Dad ($4)    Uncle ($5)
    /    \         \
Son ($1) Daughter ($3) Cousin ($1)
```

You can't just be greedy and pick the richest. If you pick Dad ($4), you lose access to Grandpa ($3) and both kids ($1 + $3). Sometimes skipping a node unlocks better options.

This is **Tree DP**: making optimal decisions at each node based on subtree outcomes.

## The Core Insight: Bottom-Up Thinking

Trees have a beautiful property: **leaves have no dependencies**. Start there, work up.

```
Step 1: Process leaves
  Son: Take $1 or $0
  Daughter: Take $3 or $0
  Cousin: Take $1 or $0

Step 2: Process their parents
  Dad:
    - If I take $4, kids can't → $4 + $0 + $0 = $4
    - If I skip, kids are free → $0 + max($1,$0) + max($3,$0) = $4
  Uncle:
    - Take $5, kid can't → $5
    - Skip, kid free → max($1,$0) = $1
    → Dad returns (4, 4), Uncle returns (5, 1)

Step 3: Process root
  Grandpa:
    - Take $3, must skip kids → $3 + 4 + 1 = $8
    - Skip, kids are free → $0 + max(4,4) + max(5,1) = $9
    → Answer: $9 (skip Grandpa, take Dad's $4 and Uncle's $5)
```

## Pattern 1: Include/Exclude (Two States)

**When to use**: Binary decision at each node (take it or leave it).

```python
def dfs(node):
    if not node:
        return (0, 0)  # (if_included, if_excluded)

    left = dfs(node.left)
    right = dfs(node.right)

    # If I'm included, children can't be
    include = node.val + left[1] + right[1]

    # If I'm excluded, each child decides independently
    exclude = max(left) + max(right)

    return (include, exclude)
```

**Visual**:
```
     Take me?
    /        \
   Yes        No
   ↓          ↓
 Kids: No   Kids: Free choice
```

## Pattern 2: Path Contribution (Max Path Sum)

**The twist**: We're finding a path, and paths can't branch.

```
    This is OK:          This is NOT a path:
        A                      A
       / \                    /|\
      B   C                  B C D

    Path: B → A → C         Not a single path!
```

So when we return information to the parent, we can only give **one branch**.

```python
def dfs(node):
    if not node:
        return 0

    left = max(0, dfs(node.left))   # Ignore negative branches
    right = max(0, dfs(node.right))

    # Path THROUGH this node (potential answer)
    path_through = node.val + left + right
    global_max = max(global_max, path_through)

    # Return: best single-branch contribution
    # (parent can only use ONE direction)
    return node.val + max(left, right)
```

**Visual**:
```
Path through A:
    left_branch → A → right_branch
         ↑           ↑
    (can use)    (can use)

Path extending upward from A:
    parent → A → one_child
                    ↑
            (only one branch allowed)
```

## Pattern 3: Multi-State (Camera Coverage)

**The problem**: Place minimum cameras such that every node is monitored. A camera monitors itself, parent, and children.

**Why 3 states?** Two states (has_camera / no_camera) don't tell us enough:
- "No camera" could mean "I'm covered by my child's camera"
- "No camera" could also mean "I need my parent to cover me"

```
State 0: NOT COVERED (needs help from parent)
State 1: COVERED (by child's camera, no camera here)
State 2: HAS CAMERA (covers self, parent, children)
```

**State transitions**:
```python
if left == 0 or right == 0:
    # A child is naked! Must place camera
    return 2

if left == 2 or right == 2:
    # A child has camera → I'm covered
    return 1

# Both children covered but no camera nearby
return 0  # Need parent to save me
```

**Visual**:
```
        Parent
       /      \
    [0]       [1]
    naked   covered

Parent MUST place camera (return 2)
because left child is naked.
```

## The Key Questions

When facing a tree DP problem, ask:

### 1. How many states per node?
```
Binary choice?           → 2 states (yes/no)
Path optimization?       → 1 state (contribution)
Coverage/constraint?     → 3+ states
```

### 2. What do I return vs track globally?
```
House Robber: Return both states to parent
Path Sum: Return contribution, track max globally
Cameras: Return coverage state, track camera count
```

### 3. What are the transition rules?
```
Draw out the state machine:
Parent_state = f(left_state, right_state, node_val)
```

## Common Mistakes

### Mistake 1: Wrong number of states
```
❌ "I'll use just (has_camera, no_camera)"
   - Doesn't distinguish "covered" from "needs coverage"

✅ Use 3 states: not_covered, covered, has_camera
```

### Mistake 2: Returning both branches for path problems
```
❌ return (left, right, through)  # Path can't fork!

✅ return node.val + max(left, right)  # Single branch
```

### Mistake 3: Forgetting the root check
```
❌ def cameras(root):
       return dfs(root)  # What if root returns 0 (uncovered)?

✅ def cameras(root):
       if dfs(root) == 0:
           cameras += 1  # Root needs a camera
       return cameras
```

## Visual Summary

```
Tree DP Patterns:

1. INCLUDE/EXCLUDE           2. PATH SUM              3. MULTI-STATE

   Return: (inc, exc)        Return: contribution     Return: state
   Answer: max(root)         Answer: global_max       Answer: count

        Node                      Node                    Node
       /    \                    /    \                  /    \
   (i,e)   (i,e)            contrib contrib          state  state
     ↓                          ↓                       ↓
   combine                  max + track             transition
```

## Quick Decision Tree

```
Tree optimization problem?
├─ Yes → Binary choice per node?
│        ├─ Yes → Include/Exclude (2 states)
│        └─ No → Path or coverage?
│                 ├─ Path → Return contribution + track global
│                 └─ Coverage → Multi-state (3+)
└─ No → Use BFS/DFS traversal
```

Tree DP is about **propagating optimal decisions upward**. Think bottom-up: what do leaves know? What do parents need? Let the states flow.
