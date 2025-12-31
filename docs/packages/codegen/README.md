# CodeGen 規格書

> **Status**: Draft  
> **Scope**: `packages/codegen/` 模組  
> **Last Updated**: 2025-12-31

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [solution_header](#3-solution_header)
4. [Helper Catalog](#4-helper-catalog)
5. [Reference Skeleton](#5-reference-skeleton)
6. [Practice Skeleton](#6-practice-skeleton)
7. [Configuration](#7-configuration)
8. [CLI Reference](#8-cli-reference)
9. [Practice Workspace](#9-practice-workspace)
10. [Examples](#10-examples)

---

## 1. Overview

### 1.1 Goals

CodeGen 的核心目標是打造 **LeetCode-like 練習體驗**：

| Goal | Description |
|------|-------------|
| **Reference Generation** | 生成符合 `solution-contract.md` 的 solution 骨架到 `solutions/` |
| **Practice Generation** | 生成練習用骨架到 `practices/`，重用 reference 的 infrastructure |
| **專注 Solution** | 練習時，使用者只需專注寫 `class Solution`，其他由平台提供 |
| **可重用元件** | `solution_header`、Helper Catalog 等可被其他模組使用 |

### 1.2 Non-Goals

| Non-Goal | Reason |
|----------|--------|
| ❌ 取代 `tools/` | CodeGen 是獨立 package，不參考 `tools/` |
| ❌ 自動生成完整解答 | 只生成骨架，使用者自己寫 Solution |
| ❌ History/Restore 管理 | 由 Practice Workspace 模組負責 |
| ❌ Runner 執行 | 由 `runner/` 負責 |

### 1.3 Terminology

| Term | Definition |
|------|------------|
| **Reference** | `solutions/` 目錄下的 canonical 解答 |
| **Practice** | `practices/` 目錄下的練習檔案 |
| **Skeleton** | 生成的檔案骨架（包含 header、imports、stubs） |
| **solution_header** | Solution 檔案的 file-level docstring（題目資訊） |
| **Helper** | 輔助 class（如 `ListNode`、`TreeNode`） |
| **Infrastructure** | solve()、parser、helper functions 的統稱 |

---

## 2. Architecture

### 2.1 Directory Structure

```
neetcode/
├── solutions/                     # Reference / Canonical solutions
│   └── <id>_<slug>.py
│
├── practices/                     # Active practice files
│   ├── <id>_<slug>.py
│   └── _history/                  # 練習歷史版本（舊 → 新）
│       └── <id>_<slug>.py.<timestamp>.bak
│
├── packages/
│   ├── codegen/                   # CodeGen package（Stateless）
│   │   ├── __init__.py
│   │   ├── cli.py                 # codegen new / codegen practice
│   │   ├── core/                  # 共享核心
│   │   │   ├── __init__.py
│   │   │   ├── solution_header.py # render_solution_header()
│   │   │   ├── stub_parser.py     # parse_code_stub() -> StubInfo
│   │   │   ├── assemble.py        # assemble_module() 組裝檔案
│   │   │   ├── config.py          # CodeGenConfig
│   │   │   └── helpers/
│   │   │       ├── __init__.py
│   │   │       ├── catalog.py     # Canonical helper 定義
│   │   │       ├── detect.py      # 從 StubInfo 推導 helpers
│   │   │       └── emit.py        # Helper 輸出策略
│   │   ├── reference/             # Reference 生成（解耦）
│   │   │   ├── __init__.py
│   │   │   └── generator.py       # generate_reference_skeleton()
│   │   └── practice/              # Practice 生成（解耦）
│   │       ├── __init__.py
│   │       ├── generator.py       # generate_practice_skeleton()
│   │       └── reuse.py           # 從 reference 複製 + 替換
│   │
│   └── practice_workspace/        # Practice Workspace（Stateful）
│       ├── __init__.py
│       ├── history.py             # 列出歷史版本
│       └── restore.py             # 恢復歷史版本
│
└── .neetcode/
    └── codegen.toml               # 使用者設定
```

### 2.2 Package 邊界設計

| Package | 角色 | 職責 |
|---------|------|------|
| `packages/codegen/` | **Stateless** | 生成檔案內容並寫入 |
| `packages/practice_workspace/` | **Stateful** | Practice 歷史與 restore 管理 |
| `runner/` | **Execution** | 執行測試（與上述解耦） |

### 2.3 Core Module Responsibilities

| Module | 職責 | 說明 |
|--------|------|------|
| `solution_header.py` | 渲染 file-level docstring | 依賴 `leetcode_datasource` |
| `stub_parser.py` | 解析 Code stub | **只解析，不猜測** |
| `assemble.py` | 組裝完整檔案 | 避免組裝邏輯分散 |
| `config.py` | Config 載入與合併 | 支援 TOML |
| `helpers/catalog.py` | Canonical helper 定義 | ListNode, TreeNode, etc. |
| `helpers/detect.py` | 從 StubInfo 推導 helpers | 責任與 parser 分離 |
| `helpers/emit.py` | 輸出 helper code | inline / import |

### 2.4 Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                    Dependency Direction                      │
│                                                              │
│   ┌──────────────────┐      ┌─────────────────────────┐     │
│   │ packages/codegen │      │ packages/practice_workspace │  │
│   └────────┬─────────┘      └─────────────────────────┘     │
│            │                         │                       │
│            │    ┌────────────────────┘                       │
│            ▼    ▼                                            │
│   ┌────────────────────────────┐                            │
│   │ packages/leetcode_datasource │                          │
│   └────────────────────────────┘                            │
│                                                              │
│   ✅ codegen → leetcode_datasource                          │
│   ✅ practice_workspace → (filesystem only)                 │
│   ❌ codegen → tools  (FORBIDDEN)                           │
│   ❌ codegen → runner (FORBIDDEN)                           │
│   ❌ practice_workspace → codegen (FORBIDDEN)               │
└─────────────────────────────────────────────────────────────┘
```

### 2.5 設計哲學

| 原則 | 說明 |
|------|------|
| **codegen = stateless** | 只負責生成，不管狀態 |
| **workspace = stateful** | 只管歷史與 restore |
| **runner = execution** | 只負責執行 |
| **stub_parser：解析，不猜** | 責任分離 |
| **helpers：集中管理、集中推導** | 避免分散 |
| **assemble.py：集中組裝** | 避免重複 |

---

## 3. solution_header

> **Module**: `packages/codegen/core/solution_header.py`

### 3.1 Definition

`solution_header` 是一個函式，用**題目 metadata** 產生 **solution 檔案的 file-level docstring**。

> Header 服務的是「solution 檔案」，不是抽象 problem。

```python
# packages/codegen/core/solution_header.py

def render_solution_header(meta: ProblemMeta, level: str = "full") -> str:
    """
    渲染 solution 檔案的 header（file-level docstring）。
    
    Args:
        meta: 題目 metadata（來自 leetcode_datasource）
        level: 資料等級 ("minimal" | "standard" | "full")
    
    Returns:
        str: 格式化的 docstring（含三引號）
    """
```

### 3.2 Data Levels

| Level | 包含內容 | 用途 |
|-------|----------|------|
| `minimal` | title, slug, difficulty, url | 最小可用 |
| `standard` | + topics, constraints | 一般用途 |
| `full` | + examples, hints, follow-up, notes | **預設**，完整練習 |

### 3.3 Output Format

```python
"""
Problem: Two Sum
Link: https://leetcode.com/problems/two-sum/

Given an array of integers nums and an integer target, return indices 
of the two numbers such that they add up to target.

Example 1:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
    Input: nums = [3,2,4], target = 6
    Output: [1,2]

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9

Topics: Array, Hash Table

Hint 1: A really brute force way would be to search for all possible pairs...

Follow-up: Can you come up with an algorithm that is less than O(n²) time complexity?
"""
```

### 3.4 API

```python
from packages.codegen.core.solution_header import render_solution_header
from packages.leetcode_datasource import LeetCodeDataSource

ds = LeetCodeDataSource()
meta = ds.get_by_frontend_id(1)

# 預設 full
header = render_solution_header(meta)

# 指定 level
header = render_solution_header(meta, level="minimal")
```

**也可從 package 根 import**：

```python
from packages.codegen import render_solution_header
```

---

## 4. Helper Catalog

> **Module**: `packages/codegen/core/helpers/`

### 4.1 Canonical Definitions (MVP)

| Helper | 用途 | Signature |
|--------|------|-----------|
| `ListNode` | Linked List 題 | `val: int, next: ListNode` |
| `TreeNode` | Binary Tree 題 | `val: int, left: TreeNode, right: TreeNode` |
| `Node` | 帶 random pointer | `val: int, next: Node, random: Node` |
| `NestedInteger` | Nested List 題 | interface |

### 4.2 Canonical Code

```python
# packages/codegen/helpers/catalog.py

HELPER_CATALOG = {
    "ListNode": '''
class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next
''',
    
    "TreeNode": '''
class TreeNode:
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right
''',
    
    "Node": '''
class Node:
    def __init__(self, val: int = 0, next: 'Node' = None, random: 'Node' = None):
        self.val = val
        self.next = next
        self.random = random
''',
    
    "NestedInteger": '''
class NestedInteger:
    """Interface for Nested List problems."""
    def isInteger(self) -> bool: ...
    def getInteger(self) -> int: ...
    def getList(self) -> list['NestedInteger']: ...
''',
}
```

### 4.3 stub_parser.py（解析，不猜）

**職責**：只解析 Code stub，不做任何推導或猜測。

```python
# packages/codegen/core/stub_parser.py
from dataclasses import dataclass

@dataclass
class StubInfo:
    """解析後的 Code stub 資訊。"""
    class_name: str                           # "Solution"
    method_name: str                          # "addTwoNumbers"
    params: list[tuple[str, str]]             # [("l1", "Optional[ListNode]"), ...]
    return_type: str                          # "Optional[ListNode]"
    raw_signature: str                        # 原始 signature 字串


def parse_code_stub(code_stub: str) -> StubInfo:
    """
    解析 LeetCode Code stub。
    
    Args:
        code_stub: LeetCode 提供的 Python code template
        
    Returns:
        StubInfo: 結構化資訊
        
    Example:
        >>> stub = '''
        ... class Solution:
        ...     def twoSum(self, nums: List[int], target: int) -> List[int]:
        ... '''
        >>> info = parse_code_stub(stub)
        >>> info.method_name
        'twoSum'
        >>> info.params
        [('nums', 'List[int]'), ('target', 'int')]
    """
    # 實作：用 ast 或 regex 解析
    ...
```

### 4.4 Detection Logic（從 StubInfo 推導 helpers）

**職責**：根據 `StubInfo` 的 params 和 return_type，推導需要哪些 helpers。

```python
# packages/codegen/core/helpers/detect.py

def detect_required_helpers(stub_info: StubInfo) -> set[str]:
    """
    從 StubInfo 推導需要哪些 helper classes。
    
    Args:
        stub_info: 解析後的 stub 資訊
        
    Returns:
        set[str]: 需要的 helper 名稱集合
    
    Example:
        >>> info = StubInfo(
        ...     class_name="Solution",
        ...     method_name="addTwoNumbers",
        ...     params=[("l1", "Optional[ListNode]"), ("l2", "Optional[ListNode]")],
        ...     return_type="Optional[ListNode]",
        ...     raw_signature="..."
        ... )
        >>> detect_required_helpers(info)
        {'ListNode'}
    """
    required = set()
    
    # 檢查所有 type hints
    all_types = [t for _, t in stub_info.params] + [stub_info.return_type]
    
    for helper_name in HELPER_CATALOG.keys():
        for type_hint in all_types:
            if helper_name in type_hint:
                required.add(helper_name)
                break
    
    return required
```

**責任分離的好處**：
- `stub_parser`：純解析，易測試，不受 helper 規則影響
- `detect`：專注推導，規則變化不影響 parser

### 4.5 Emit Strategy

| Mode | 行為 | 設定 |
|------|------|------|
| `inline` | 將 helper 定義直接寫入檔案（**預設**） | `helpers.mode = "inline"` |
| `import` | 從共用模組 import（未來） | `helpers.mode = "import"` |
| `none` | 不生成，讓使用者自己加 | `helpers.mode = "none"` |

### 4.6 assemble.py（集中組裝）

**職責**：把已產生好的區塊組合成完整檔案，避免組裝邏輯分散。

```python
# packages/codegen/core/assemble.py

def assemble_module(
    header: str,
    imports: str,
    helpers: str,
    judge_func: str,
    solutions_dict: str,
    solution_classes: str,
    helper_functions: str,
    solve_fn: str,
) -> str:
    """
    組裝完整的 solution/practice 檔案。
    
    Args:
        header: file-level docstring
        imports: import statements
        helpers: helper class definitions (ListNode, etc.)
        judge_func: JUDGE_FUNC definition (可為空)
        solutions_dict: SOLUTIONS = {...}
        solution_classes: Solution class(es)
        helper_functions: 輔助函式 (list_to_linkedlist, etc.)
        solve_fn: solve() function
        
    Returns:
        str: 完整的 Python 模組內容
    """
    sections = [
        header,
        imports,
        helpers,
        judge_func,
        solutions_dict,
        solution_classes,
        helper_functions,
        solve_fn,
        'if __name__ == "__main__":\n    solve()\n',
    ]
    
    # 過濾空區塊，用適當空行連接
    non_empty = [s for s in sections if s.strip()]
    return '\n\n'.join(non_empty)
```

**設計原則**：
- 不引入模板系統（無 Jinja2 依賴）
- 純 Python 函式，責任單一
- Reference/Practice generator 都使用同一個 assemble

---

## 5. Reference Skeleton

### 5.1 Generation Flow

```
codegen new <id>
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│  1. 檢查 solutions/<id>_<slug>.py 是否存在              │
│     ├── 存在 → 不動它，提示使用 codegen practice       │
│     └── 不存在 → 繼續                                   │
│                                                          │
│  2. 從 leetcode_datasource 取得題目 metadata            │
│                                                          │
│  3. 生成 skeleton 內容                                   │
│     ├── solution_header（full）                         │
│     ├── imports                                          │
│     ├── helpers（偵測 + emit）                          │
│     ├── JUDGE_FUNC（若需要，placeholder）               │
│     ├── SOLUTIONS dict                                   │
│     ├── Solution class stub                              │
│     ├── helper functions（若需要，placeholder）         │
│     └── solve()（placeholder 或 core 建議版）           │
│                                                          │
│  4. 寫入 solutions/<id>_<slug>.py                       │
└──────────────────────────────────────────────────────────┘
```

### 5.2 Output Structure

```python
# solutions/<id>_<slug>.py
"""
{solution_header - full level}
"""
from typing import List, Optional
from _runner import get_solver


# ============================================
# Helper Classes (if needed)
# ============================================
class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "{method_name}",
        "complexity": "TODO: O(?)",
        "description": "TODO: describe your approach",
    },
}


# ============================================
# Solution
# ============================================
class Solution:
    def {method_name}(self, {params}) -> {return_type}:
        # TODO: Implement your solution
        pass


# ============================================
# solve() - stdin/stdout interface
# ============================================
def solve():
    """
    Input format:
        TODO: Define based on problem
        
    Example (from problem):
        {example_input}
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    # TODO: Parse input
    # ...
    
    solver = get_solver(SOLUTIONS)
    # TODO: Call method
    # result = solver.{method_name}(...)
    
    # TODO: Print result
    # print(result)
    pass


if __name__ == "__main__":
    solve()
```

### 5.3 solve() Strategy

| 策略 | 行為 | 設定 |
|------|------|------|
| `placeholder` | 生成 TODO placeholder（**預設**） | `skeleton.solve_mode = "placeholder"` |
| `infer` | 嘗試從 examples 推導 | `skeleton.solve_mode = "infer"` |

**推導失敗時**：自動 fallback 到 placeholder。

---

## 6. Practice Skeleton

### 6.1 Generation Flow

```
codegen practice <id>
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│  1. 檢查 practices/<id>_<slug>.py 是否存在              │
│     └── 存在 → 先存到 _history/（由 workspace 處理）   │
│                                                          │
│  2. 檢查 solutions/<id>_<slug>.py 是否存在              │
│     ├── 存在 → 使用 Reuse Strategy（見 6.2）           │
│     └── 不存在 → 使用 Reference Skeleton 流程          │
│                                                          │
│  3. 生成 practice skeleton                               │
│                                                          │
│  4. 寫入 practices/<id>_<slug>.py                       │
└──────────────────────────────────────────────────────────┘
```

### 6.2 Reuse Strategy（核心）

當 `solutions/<id>` 存在時：

| 元件 | 處理方式 |
|------|----------|
| **solution_header** | ✅ 完整保留 |
| **imports** | ✅ 完整保留 |
| **Helper classes** | ✅ 完整保留 |
| **JUDGE_FUNC + helpers** | ✅ 完整保留 |
| **SOLUTIONS dict** | ⚠️ 保留結構，清空 `complexity`/`description` |
| **Solution class(es)** | ⚠️ 保留 signature，清空 body |
| **Helper functions** | ✅ 完整保留 |
| **solve()** | ✅ 完整保留 |

**核心理念**：
> 練習時，使用者只需專注寫 `class Solution`，其他 infrastructure 由平台提供。

### 6.3 Multi-Solution Handling

| Mode | 行為 | 設定 |
|------|------|------|
| `single` | 只保留 default Solution（**預設**） | `practice.multi_solution_mode = "single"` |
| `all` | 保留所有 Solution classes，全部清空 | `--all-solutions` flag |

**Single Mode 輸出**：

```python
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "lengthOfLongestSubstring",
        "complexity": "TODO: O(?)",
        "description": "TODO: describe your approach",
    },
}

# ============================================================
# 👇 YOUR SOLUTION - Implement below
# 💡 Reference has 3 approaches: solutions/0003_...py
# ============================================================
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # TODO: Implement your solution
        pass
```

**All Mode 輸出**：

```python
SOLUTIONS = {
    "default": {"class": "Solution", ...},
    "dict": {"class": "SolutionDict", ...},
    "set": {"class": "SolutionWithSet", ...},
}

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        pass

class SolutionDict:
    def lengthOfLongestSubstring(self, s: str) -> int:
        pass

class SolutionWithSet:
    def lengthOfLongestSubstring(self, s: str) -> int:
        pass
```

### 6.4 Practice Output Structure

```python
# practices/<id>_<slug>.py
"""
{solution_header - 完整保留自 reference}
"""
from typing import List, Optional
from _runner import get_solver


# Helper classes（完整保留自 reference）
class ListNode:
    ...


# JUDGE_FUNC（完整保留自 reference，若有）
def judge(actual, expected, input_data: str) -> bool:
    ...

JUDGE_FUNC = judge


# SOLUTIONS（保留結構，清空 complexity/description）
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "addTwoNumbers",
        "complexity": "TODO: O(?)",
        "description": "TODO: describe your approach",
    },
}


# ============================================================
# 👇 YOUR SOLUTION - Implement below
# 💡 Reference: solutions/0002_add_two_numbers.py
# ============================================================
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        # TODO: Implement your solution
        pass


# Helper functions（完整保留自 reference）
def list_to_linkedlist(lst: List[int]) -> Optional[ListNode]:
    ...

def linkedlist_to_list(node: Optional[ListNode]) -> List[int]:
    ...


# solve()（完整保留自 reference）
def solve():
    ...


if __name__ == "__main__":
    solve()
```

---

## 7. Configuration

### 7.1 Config File

```toml
# .neetcode/codegen.toml

[header]
# solution_header 等級
# "minimal" | "standard" | "full"
level = "full"

[helpers]
# Helper 輸出策略
# "inline" | "import" | "none"
mode = "inline"

[skeleton]
# solve() 生成策略
# "placeholder" | "infer"
solve_mode = "placeholder"

[practice]
# 多解法處理
# "single" | "all"
multi_solution_mode = "single"
```

### 7.2 Priority Order

```
CLI flag > .neetcode/codegen.toml > package defaults
```

### 7.3 Defaults

| Setting | Default |
|---------|---------|
| `header.level` | `"full"` |
| `helpers.mode` | `"inline"` |
| `skeleton.solve_mode` | `"placeholder"` |
| `practice.multi_solution_mode` | `"single"` |

---

## 8. CLI Reference

### 8.1 codegen new

生成 Reference Skeleton 到 `solutions/`。

```bash
codegen new <problem_id>
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `problem_id` | ✅ | LeetCode 題號（如 `1`, `23`, `994`） |

**Options:**

| Option | Description |
|--------|-------------|
| `--header-level <level>` | Override header level (`minimal`, `standard`, `full`) |
| `--solve-mode <mode>` | Override solve mode (`placeholder`, `infer`) |
| `--dry-run` | 只輸出內容，不寫檔 |

**Examples:**

```bash
# 生成 Two Sum 的 reference skeleton
codegen new 1

# 使用 minimal header
codegen new 1 --header-level minimal

# 嘗試推導 solve()
codegen new 1 --solve-mode infer

# 只預覽，不寫檔
codegen new 1 --dry-run
```

**Output:**

```
✅ Created: solutions/0001_two_sum.py
```

```
ℹ️  Reference already exists: solutions/0001_two_sum.py
   Use `codegen practice 1` to start practicing.
```

### 8.2 codegen practice

生成 Practice Skeleton 到 `practices/`。

```bash
codegen practice <problem_id>
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `problem_id` | ✅ | LeetCode 題號 |

**Options:**

| Option | Description |
|--------|-------------|
| `--all-solutions` | 保留所有 Solution classes（多解法題目） |
| `--dry-run` | 只輸出內容，不寫檔 |

**Examples:**

```bash
# 生成練習骨架
codegen practice 1

# 多解法題目，保留所有解法
codegen practice 3 --all-solutions
```

**Output:**

```
✅ Created: practices/0001_two_sum.py
   (reusing infrastructure from solutions/0001_two_sum.py)
```

```
ℹ️  Existing practice found: practices/0001_two_sum.py
✅ Saved to history: practices/_history/0001_two_sum.py.20251231_160000.bak
✅ Generated: practices/0001_two_sum.py
```

---

## 9. Practice Workspace

> **Package**: `packages/practice_workspace/`  
> **角色**: Stateful — 管理 Practice 歷史與 restore

Practice Workspace 是**獨立 package**，與 CodeGen 解耦。

### 9.1 Package Structure

```
packages/practice_workspace/
├── __init__.py
├── history.py             # 列出歷史版本
├── restore.py             # 恢復歷史版本
└── utils.py               # 共用工具（timestamp 處理等）
```

### 9.2 職責邊界

| 職責 | Practice Workspace | CodeGen |
|------|-------------------|---------|
| 保存舊版 practice 到 `_history/` | ✅ | ❌ |
| 列出 history | ✅ | ❌ |
| restore 某一版 | ✅ | ❌ |
| 生成檔案內容 | ❌ | ✅ |

### 9.3 practice history

列出練習歷史版本。

```bash
practice history <problem_id>
```

**Output（舊 → 新，最新在最下面）**：

```
Practice history for 0001_two_sum:

  [1] 20251225_200000  (6 days ago)
  [2] 20251230_091500  (1 day ago)
  [3] 20251231_143022  (2 hours ago)   ← latest

Total: 3 versions
```

### 9.4 practice restore

恢復歷史版本。

```bash
practice restore <problem_id>
```

**預設行為**：列出選項讓使用者選擇（互動模式）。

```
Available versions for 0001_two_sum:

  [1] 20251225_200000  (6 days ago)
  [2] 20251230_091500  (1 day ago)
  [3] 20251231_143022  (2 hours ago)   ← latest

Select version to restore [3]: 2

✅ Restored: practices/0001_two_sum.py
   (from: 20251230_091500)
```

**Options:**

| Option | Description |
|--------|-------------|
| `--latest` | 直接恢復最新版本（不互動） |
| `--at <timestamp>` | 恢復指定時間戳版本 |

### 9.5 與 CodeGen 的協作

當執行 `codegen practice <id>` 時：

1. **CodeGen** 檢查 `practices/<id>.py` 是否存在
2. 若存在，**CodeGen 呼叫 Practice Workspace** 保存到 `_history/`
3. **CodeGen** 生成新的 practice skeleton
4. **CodeGen** 寫入 `practices/<id>.py`

```python
# packages/codegen/practice/generator.py

from packages.practice_workspace import save_to_history

def generate_practice_skeleton(problem_id: int):
    practice_path = get_practice_path(problem_id)
    
    # 若已存在，先保存到 history
    if practice_path.exists():
        save_to_history(practice_path)
    
    # 生成新 skeleton
    content = _generate_content(problem_id)
    
    # 寫入
    practice_path.write_text(content)
```

---

## 10. Examples

### 10.1 Simple Problem (Two Sum)

```bash
# 1. 生成 reference
$ codegen new 1
✅ Created: solutions/0001_two_sum.py

# 2. 你完成 reference 解答...

# 3. 開始練習
$ codegen practice 1
✅ Created: practices/0001_two_sum.py
   (reusing infrastructure from solutions/0001_two_sum.py)

# 4. 執行測試
$ python runner/test_runner.py 0001 --practice
```

### 10.2 Linked List Problem (Add Two Numbers)

```bash
$ codegen new 2
✅ Created: solutions/0002_add_two_numbers.py
   (detected helpers: ListNode)

# Reference 會包含：
# - ListNode class（from catalog）
# - list_to_linkedlist, linkedlist_to_list helpers
# - solve() placeholder
```

### 10.3 Multi-Solution Problem (Longest Substring)

```bash
# Reference 有 3 種解法
$ codegen practice 3
✅ Created: practices/0003_longest_substring_without_repeating_characters.py
   (single mode: only default Solution)

# 想練習所有解法
$ codegen practice 3 --all-solutions
✅ Created: practices/0003_longest_substring_without_repeating_characters.py
   (all mode: 3 Solution classes)
```

---

## Appendix

### A. Glossary

| Term | Definition |
|------|------------|
| **Reference** | `solutions/` 目錄下的 canonical 解答 |
| **Practice** | `practices/` 目錄下的練習檔案 |
| **Skeleton** | 生成的檔案骨架 |
| **solution_header** | 檔案開頭的題目描述 docstring |
| **Helper** | ListNode, TreeNode 等輔助 class |
| **Infrastructure** | solve(), parser, helpers 的統稱 |
| **Catalog** | Canonical helper 定義集合 |

### B. Related Documents

| Document | Description |
|----------|-------------|
| [solution-contract.md](../../contracts/solution-contract.md) | Solution 檔案規格 |
| [packages-architecture-spec.md](../../architecture/packages-overview.md) | Packages 架構規格 |
| [leetcode_datasource](../leetcode_datasource/README.md) | 資料層文件 |

### C. Changelog

| Date | Change |
|------|--------|
| 2025-12-31 | Initial draft |

