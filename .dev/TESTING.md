# 測試文檔 - NeetCode Practice Framework

## 概述

本專案建立了完整的測試套件，分為**三大類別**：

| 類別 | 目錄 | 用途 | 測試數量 |
|------|------|------|----------|
| **1. 元件功能測試** | `.dev/tests/` | 測試 Runner 模組功能 | ~273 |
| **2. 測資正確性測試** | `.dev/tests_solutions/` | 測試 Solution 執行結果 | ~99 |
| **3. 格式合規測試** | `tools/tests/` | 測試 Solution 格式規範 | ~10 |

## 測試負責人

**luffdev** - 單元測試負責人

## 核心目標

> 用測試把「行為」釘死，幫忙守住重構不爆炸

---

## 快速開始

### 安裝依賴

```bash
python -m pip install pytest pytest-cov
```

### 運行所有測試（推薦）

```bash
# Windows
.dev\run_all_tests.bat

# Linux/Mac
.dev/run_all_tests.sh
```

### 分別運行各類測試

```bash
# 1. 格式合規測試
tools\run_format_tests.bat      # Windows
tools/run_format_tests.sh       # Linux/Mac

# 2. 元件功能測試
.dev\run_tests.bat              # Windows
.dev/run_tests.sh               # Linux/Mac

# 3. 測資正確性測試
.dev\run_tests_solutions.bat    # Windows
.dev/run_tests_solutions.sh     # Linux/Mac
```

---

## 測試類別詳解

### 1. 格式合規測試 (Solution Format Tests)

**位置**: `tools/tests/`

測試 Solution 檔案是否符合 Pure Polymorphic Architecture 規範。

#### 測試項目

| 測試 | 說明 |
|------|------|
| `test_solution_comment_format` | Solution 註解使用 "Solution 1:" 格式 |
| `test_complexity_comments` | 有 Time/Space 複雜度註解 |
| `test_solutions_dictionary_exists` | SOLUTIONS 字典存在 |
| `test_solutions_dictionary_structure` | SOLUTIONS 有 'class' 欄位 |
| `test_no_wrapper_functions` | 無 solve_* wrapper 函數 |
| `test_uses_get_solver` | 使用 get_solver() 模式 |
| `test_solution_comment_before_class` | 註解在 class 之前 |
| `test_all_solution_classes_have_comments` | 所有 Solution 類別有註解 |

#### 運行方式

```bash
# 快速檢查
python tools/check_solutions.py
python tools/check_solutions.py --verbose  # 顯示修正建議

# 單元測試
python -m pytest tools/tests/test_solution_format.py -v
```

#### 相關文檔

- [tools/FORMAT_CHECKING.md](../tools/FORMAT_CHECKING.md) - 格式檢查工具詳細說明

---

### 2. 元件功能測試 (Component Tests)

**位置**: `.dev/tests/`

測試 Runner 系統的核心功能，確保重構不會破壞現有行為。

#### 測試檔案

| 檔案 | 測試對象 | 測試數 |
|------|----------|--------|
| `test_util.py` | runner/util.py | 40+ |
| `test_case_runner.py` | runner/case_runner.py | 15+ |
| `test_test_runner.py` | runner/test_runner.py | 30+ |
| `test_complexity_estimator.py` | runner/complexity_estimator.py | 25+ |
| `test_edge_cases.py` | 邊界條件 | 40+ |
| `test_integration.py` | 整合測試 | 20+ |
| `test_generate_mindmaps.py` | tools/generate_mindmaps.py | 50+ |
| `test_generate_pattern_docs.py` | tools/generate_pattern_docs.py | 50+ |

#### 測試覆蓋範圍

##### runner/util.py
- ✅ `normalize_output()` - 輸出正規化
- ✅ `compare_outputs()` - 三種比較模式（exact/sorted/set）
- ✅ `compare_result()` - 支援 JUDGE_FUNC
- ✅ 路徑輔助函數
- ✅ 檔案操作函數

##### runner/case_runner.py
- ✅ 命令列參數解析和驗證
- ✅ 檔案存在性檢查
- ✅ 單一測試案例執行流程

##### runner/test_runner.py
- ✅ `load_solution_module()` - 解法模組載入
- ✅ `load_generator_module()` - 生成器模組載入
- ✅ `run_one_case()` - 單案例執行
- ✅ 多解法支援（SOLUTIONS metadata）
- ✅ 比較模式（exact/sorted/set）
- ✅ JUDGE_FUNC 支援

##### runner/complexity_estimator.py
- ✅ 可用性檢查
- ✅ 複雜度估算
- ✅ Mock stdin 機制
- ✅ 結果格式化

#### 運行方式

```bash
# 全部元件測試
python -m pytest .dev/tests -v

# 按標記運行
python -m pytest .dev/tests -v -m unit
python -m pytest .dev/tests -v -m integration
python -m pytest .dev/tests -v -m edge_case

# 特定檔案
python -m pytest .dev/tests/test_util.py -v
```

---

### 3. 測資正確性測試 (Solution Correctness Tests)

**位置**: `.dev/tests_solutions/`

測試所有 Solution 檔案的執行結果是否正確。

#### 測試類型

| 測試 | 說明 |
|------|------|
| `test_static_tests` | 使用 tests/ 目錄的靜態測資 |
| `test_generated_tests` | 使用生成器產生測資（需要 JUDGE_FUNC） |
| `test_combined_static_and_generated` | 兩者結合 |

#### 跳過條件

測試會自動跳過：
- 無法載入的 Solution 模組
- 沒有靜態測資的問題
- 沒有生成器的問題
- 沒有 JUDGE_FUNC 的問題（生成測試需要）

#### 運行方式

```bash
# 全部 Solution 測試
python -m pytest .dev/tests_solutions -v

# 特定問題
python -m pytest .dev/tests_solutions -v -k "0023"

# 只測靜態測資
python -m pytest .dev/tests_solutions/test_all_solutions.py::TestAllSolutions::test_static_tests -v
```

---

## 測試原則

### 1. 行為優先
測試「做什麼」而不是「怎麼做」。重構可以改變實作，但不能改變行為。

### 2. 輸入輸出驗證
給定相同輸入，必須得到相同輸出。

### 3. 邊界條件覆蓋
測試極端情況：空輸入、最小值/最大值、錯誤格式、大資料量、特殊字元。

### 4. 獨立性
每個測試獨立運行，不依賴其他測試的執行順序或狀態。

### 5. 可重複性
測試結果必須是確定性的，不受時間、環境等因素影響。

---

## 測試標記 (Markers)

```python
@pytest.mark.unit          # 單元測試
@pytest.mark.integration   # 整合測試
@pytest.mark.edge_case     # 邊界測試
@pytest.mark.slow          # 慢速測試
@pytest.mark.requires_big_o # 需要 big-O 套件
```

---

## 測試目錄結構

```
neetcode/
├── .dev/
│   ├── tests/                          # 元件功能測試
│   │   ├── test_util.py
│   │   ├── test_case_runner.py
│   │   ├── test_test_runner.py
│   │   ├── test_complexity_estimator.py
│   │   ├── test_edge_cases.py
│   │   ├── test_integration.py
│   │   ├── test_generate_mindmaps.py
│   │   ├── test_generate_pattern_docs.py
│   │   └── README.md
│   │
│   ├── tests_solutions/                # 測資正確性測試
│   │   ├── test_all_solutions.py
│   │   └── README.md
│   │
│   ├── run_tests.bat/sh                # 元件測試腳本
│   ├── run_tests_solutions.bat/sh      # 測資測試腳本
│   ├── run_all_tests.bat/sh            # ★ 全專案測試腳本
│   │
│   ├── TESTING.md                      # 本文件
│   ├── VIRTUAL_ENV_SETUP.md
│   └── README.md
│
└── tools/
    ├── tests/                          # 格式合規測試
    │   └── test_solution_format.py
    │
    ├── check_solutions.py              # 格式檢查工具
    ├── run_format_tests.py
    ├── run_format_tests.bat/sh         # 格式測試腳本
    └── FORMAT_CHECKING.md
```

---

## 腳本總覽

| 腳本 | 用途 | 位置 |
|------|------|------|
| `run_all_tests.bat/sh` | ★ 運行全部三類測試 | `.dev/` |
| `run_tests.bat/sh` | 運行元件功能測試 | `.dev/` |
| `run_tests_solutions.bat/sh` | 運行測資正確性測試 | `.dev/` |
| `run_format_tests.bat/sh` | 運行格式合規測試 | `tools/` |

---

## 開發工作流程

### 添加新功能

1. 先寫測試（TDD）
2. 實作功能
3. 運行測試確保通過
4. 提交代碼

### 修復 Bug

1. 先寫測試重現 bug
2. 修復 bug
3. 確保測試通過
4. 提交代碼

### 重構代碼

1. 確保現有測試全部通過
2. 進行重構
3. 再次運行測試
4. 如果失敗，修復代碼或更新測試
5. 提交代碼

### 添加新 Solution

1. 確保遵循格式規範（運行 `python tools/check_solutions.py`）
2. 添加測試案例到 `tests/` 目錄
3. 運行 `python -m pytest .dev/tests_solutions -v -k "問題編號"`
4. 提交代碼

---

## CI/CD 整合

### GitHub Actions 範例

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install pytest pytest-cov
      
      - name: Format Tests
        run: |
          python tools/check_solutions.py
          pytest tools/tests/ -v
      
      - name: Component Tests
        run: pytest .dev/tests/ -v
      
      - name: Solution Tests
        run: pytest .dev/tests_solutions/ -v
```

---

## 命令參考

```bash
# === 全專案測試 ===
.dev\run_all_tests.bat                          # Windows
.dev/run_all_tests.sh                           # Linux/Mac

# === 格式測試 ===
python tools/check_solutions.py                 # 快速檢查
python tools/check_solutions.py --verbose       # 顯示建議
python -m pytest tools/tests -v                 # 單元測試

# === 元件測試 ===
python -m pytest .dev/tests -v                  # 全部
python -m pytest .dev/tests -v -m unit          # 單元測試
python -m pytest .dev/tests -v -m integration   # 整合測試
python -m pytest .dev/tests -v -m edge_case     # 邊界測試

# === 測資測試 ===
python -m pytest .dev/tests_solutions -v        # 全部
python -m pytest .dev/tests_solutions -v -k "0023"  # 特定問題

# === 覆蓋率 ===
python -m pytest .dev/tests --cov=runner --cov-report=html

# === 其他選項 ===
python -m pytest ... -x                         # 第一個失敗時停止
python -m pytest ... --lf                       # 只跑失敗的測試
python -m pytest ... --tb=short                 # 簡短錯誤訊息
```

---

## 聯絡資訊

**測試負責人**: luffdev  
**建立日期**: 2025-12-08  
**最後更新**: 2025-12-12
