# 🧩 NeetCode / LeetCode Practice Framework

一套完整的 LeetCode 練習框架，支援多筆測資、自動比對、Debug 整合。

---

## 📁 專案結構

```
neetcode/
│
├── .vscode/                 ← VS Code 整合設定
│   ├── settings.json        ← Python 環境設定
│   ├── tasks.json           ← Ctrl+Shift+B 快捷任務
│   └── launch.json          ← F5 Debug 設定
│
├── runner/                  ← 執行器模組
│   ├── test_runner.py       ← 跑所有 .in/.out 並比對
│   ├── case_runner.py       ← 跑單一 .in 測資（Debug 用）
│   └── util.py              ← 共用工具函式
│
├── solutions/               ← 每一題的解答程式
│   └── 0001_two_sum.py
│
├── tests/                   ← 所有測資
│   ├── 0001_two_sum_1.in
│   ├── 0001_two_sum_1.out
│   └── ...
│
├── templates/               ← 新題目模板
│   ├── template_solution.py
│   └── template_test.txt
│
├── leetcode/                ← Python 虛擬環境 (Python 3.11)
│
├── run_tests.bat            ← Windows: 執行所有測資
├── run_case.bat             ← Windows: 執行單一測資
├── new_problem.bat          ← Windows: 建立新題目
│
└── README.md
```

---

## 🚀 快速開始

### 1. 環境設定（首次安裝）

> 參考 [LeetCode 官方環境說明](https://support.leetcode.com/hc/en-us/articles/360011833974-What-are-the-environments-for-the-programming-languages)

```powershell
# 進入專案目錄
cd /d "D:\Developer\program\python\neetcode"

# 安裝 Python 3.11（如果尚未安裝）
py install 3.11

# 建立虛擬環境
py -3.11 -m venv leetcode

# 啟動虛擬環境
leetcode\Scripts\activate

# 安裝 debugpy（Debug 用）
pip install debugpy
```

### 2. 日常使用（啟動環境）

```powershell
cd /d "D:\Developer\program\python\neetcode"
leetcode\Scripts\activate
```

### 3. 建立新題目

```batch
new_problem.bat 0007_reverse_integer
```

這會自動建立：
- `solutions/0007_reverse_integer.py`
- `tests/0007_reverse_integer_1.in`
- `tests/0007_reverse_integer_1.out`

### 4. 執行測試

```batch
# 執行所有測資
run_tests.bat 0001_two_sum

# 執行單一測資
run_case.bat 0001_two_sum 1
```

---

## ⌨️ VS Code 快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| `Ctrl+Shift+B` | 執行當前檔案對應的所有測資 |
| `F5` | Debug 當前檔案的 case #1 |

> **注意**: 請先開啟 `solutions/` 中的解答檔案，再使用快捷鍵。

---

## 📝 解答檔案格式

```python
# solutions/0001_two_sum.py
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # 你的解法
        pass

def solve():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    # 解析輸入
    nums = list(map(int, lines[0].split(',')))
    target = int(lines[1])
    
    sol = Solution()
    result = sol.twoSum(nums, target)
    
    # 輸出答案
    print(result)

if __name__ == "__main__":
    solve()
```

---

## 📋 測資檔案格式

### 輸入檔 (`.in`)
```
2,7,11,15
9
```

### 輸出檔 (`.out`)
```
[0, 1]
```

> 測資檔案命名規則: `{題號}_{題目名稱}_{編號}.in/.out`

---

## 🔧 命令列用法

```bash
# 執行所有測資
python runner/test_runner.py <problem_name>

# 執行單一測資
python runner/case_runner.py <problem_name> <case_index>
```

### 範例

```bash
python runner/test_runner.py 0001_two_sum
python runner/case_runner.py 0001_two_sum 1
```

---

## 📊 測試結果範例

```
=== 0001_two_sum_1.in ===
✅ PASS

=== 0001_two_sum_2.in ===
✅ PASS

=== 0001_two_sum_3.in ===
✅ PASS

測試結果 / Summary: 3 / 3 cases passed.
```

---

## 🐍 Python 環境

- **Python 版本**: 3.11（與 [LeetCode 官方環境](https://support.leetcode.com/hc/en-us/articles/360011833974-What-are-the-environments-for-the-programming-languages) 一致）
- **虛擬環境**: `leetcode/` (專案內)
- **已安裝套件**:
  - `debugpy` - Debug 支援

### 啟動虛擬環境

```powershell
# PowerShell
.\leetcode\Scripts\Activate.ps1

# CMD
leetcode\Scripts\activate.bat
```

### 安裝新套件

```powershell
# 先啟動虛擬環境，再安裝
leetcode\Scripts\activate
pip install <package_name>
```

---

## 💡 小技巧

1. **新增多筆測資**: 複製 `.in/.out` 檔案，修改編號即可
   ```
   0001_two_sum_1.in → 0001_two_sum_2.in
   0001_two_sum_1.out → 0001_two_sum_2.out
   ```

2. **Debug 特定測資**: 修改 `launch.json` 中的 case 編號

3. **自訂輸入格式**: 在 `solve()` 函式中自由定義解析邏輯

---

## 📜 License

MIT License - 自由使用於個人學習

