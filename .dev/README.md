# 開發者與維護者專區

> ⚠️ **注意**: 此資料夾專為專案維護者使用，包含單元測試、開發文檔和維護工具。  
> 一般使用者請參考根目錄的 [README.md](../README.md)

---

## 📁 資料夾結構

```
.dev/
├── tests/                          # 元件功能測試（Runner 模組）
│   ├── test_util.py                # util.py 測試 (40+ tests)
│   ├── test_case_runner.py         # case_runner.py 測試 (15+ tests)
│   ├── test_test_runner.py         # test_runner.py 測試 (30+ tests)
│   ├── test_complexity_estimator.py # complexity_estimator.py 測試 (25+ tests)
│   ├── test_edge_cases.py          # 邊界條件測試 (40+ tests)
│   ├── test_integration.py         # 整合測試 (20+ tests)
│   ├── test_generate_mindmaps.py   # mindmap 生成器測試 (50+ tests)
│   ├── test_generate_pattern_docs.py # pattern doc 生成器測試 (50+ tests)
│   └── README.md
│
├── tests_solutions/                # 測資正確性測試
│   ├── test_all_solutions.py       # 所有 Solution 測試 (~99 tests)
│   └── README.md
│
├── run_tests.bat                   # Windows - 元件測試
├── run_tests.sh                    # Linux/Mac - 元件測試
├── run_tests_solutions.bat         # Windows - 測資測試
├── run_tests_solutions.sh          # Linux/Mac - 測資測試
├── run_all_tests.bat               # ★ Windows - 全專案測試
├── run_all_tests.sh                # ★ Linux/Mac - 全專案測試
│
├── TESTING.md                      # 完整測試文檔
├── VIRTUAL_ENV_SETUP.md            # 虛擬環境設定指南
└── README.md                       # 本文件
```

---

## 🎯 測試分類

本專案的測試分為**三大類別**：

| 類別 | 目錄 | 用途 | 數量 |
|------|------|------|------|
| **格式合規測試** | `tools/tests/` | Solution 格式規範 | ~10 |
| **元件功能測試** | `.dev/tests/` | Runner 模組功能 | ~273 |
| **測資正確性測試** | `.dev/tests_solutions/` | Solution 執行結果 | ~99 |

---

## 🚀 快速開始

### 1. 確保虛擬環境已建立

```bash
# Windows
python -m venv leetcode
leetcode\Scripts\activate

# Linux/Mac
python -m venv leetcode
source leetcode/bin/activate
```

### 2. 安裝測試依賴

```bash
pip install pytest pytest-cov
```

### 3. 運行全部測試（推薦）

```bash
# Windows
.dev\run_all_tests.bat

# Linux/Mac
.dev/run_all_tests.sh
```

這會依序執行：
1. ✅ Solution 格式合規測試
2. ✅ Runner 元件功能測試
3. ✅ Solution 測資正確性測試

### 4. 分別運行各類測試

```bash
# === 格式合規測試 ===
# Windows
tools\run_format_tests.bat
# Linux/Mac
tools/run_format_tests.sh

# === 元件功能測試 ===
# Windows
.dev\run_tests.bat
# Linux/Mac
.dev/run_tests.sh

# === 測資正確性測試 ===
# Windows
.dev\run_tests_solutions.bat
# Linux/Mac
.dev/run_tests_solutions.sh
```

---

## 📊 測試統計

| 項目 | 數量 |
|------|------|
| 測試檔案 | 10 |
| 測試類別 | 70+ |
| 測試案例 | 380+ |
| 代碼覆蓋率 | 80-100% |

### 測試覆蓋範圍

- ✅ `runner/util.py` - 100% 覆蓋
- ✅ `runner/case_runner.py` - 90% 覆蓋
- ✅ `runner/test_runner.py` - 85% 覆蓋
- ✅ `runner/complexity_estimator.py` - 80% 覆蓋
- ✅ `solutions/*.py` - 格式合規驗證

---

## 📚 文檔索引

### 核心文檔

| 文檔 | 說明 |
|------|------|
| [TESTING.md](TESTING.md) | 完整測試文檔（策略、原則、工作流程） |
| [VIRTUAL_ENV_SETUP.md](VIRTUAL_ENV_SETUP.md) | 虛擬環境設定指南 |
| [tests/README.md](tests/README.md) | 元件測試詳細說明 |
| [tests_solutions/README.md](tests_solutions/README.md) | 測資測試詳細說明 |
| [../tools/FORMAT_CHECKING.md](../tools/FORMAT_CHECKING.md) | 格式檢查工具說明 |

---

## 🔧 開發工作流程

### 添加新 Solution

1. 確保遵循格式規範
   ```bash
   python tools/check_solutions.py --verbose
   ```
2. 添加測試案例到 `tests/` 目錄
3. 運行測試驗證
   ```bash
   python -m pytest .dev/tests_solutions -v -k "問題編號"
   ```
4. 提交代碼

### 修改 Runner 模組

1. 先運行現有測試確保通過
2. 進行修改
3. 再次運行測試
   ```bash
   python -m pytest .dev/tests -v
   ```
4. 提交代碼

### 重構代碼

1. 運行全部測試建立基線
   ```bash
   .dev\run_all_tests.bat
   ```
2. 進行重構
3. 再次運行全部測試確保行為一致
4. 提交代碼

---

## 📈 測試命令參考

```bash
# === 全專案測試 ===
.dev\run_all_tests.bat                    # Windows
.dev/run_all_tests.sh                     # Linux/Mac

# === 格式測試 ===
python tools/check_solutions.py           # 快速檢查
python tools/check_solutions.py --verbose # 顯示建議
python -m pytest tools/tests -v           # 單元測試

# === 元件測試 ===
python -m pytest .dev/tests -v            # 全部
python -m pytest .dev/tests -v -m unit    # 按標記

# === 測資測試 ===
python -m pytest .dev/tests_solutions -v  # 全部
python -m pytest .dev/tests_solutions -v -k "0023"  # 特定問題

# === 覆蓋率報告 ===
python -m pytest .dev/tests --cov=runner --cov-report=html
```

---

## 🎓 測試原則

1. **行為測試優先** - 測試「做什麼」而不是「怎麼做」
2. **獨立性** - 每個測試獨立運行，不依賴其他測試
3. **可重複性** - 測試結果是確定性的
4. **清晰性** - 測試易於理解和維護
5. **完整性** - 覆蓋正常情況和邊界情況

---

## 📞 聯絡資訊

**測試負責人**: luffdev  
**建立日期**: 2025-12-08  
**最後更新**: 2025-12-12

---

## 🔗 相關連結

- [專案主 README](../README.md) - 專案整體說明
- [根目錄 pytest.ini](../pytest.ini) - pytest 配置文件
- [requirements.txt](../requirements.txt) - 專案依賴
- [tools/FORMAT_CHECKING.md](../tools/FORMAT_CHECKING.md) - 格式檢查說明

---

**注意**: 此資料夾的內容專為維護者使用，一般使用者無需關注。
