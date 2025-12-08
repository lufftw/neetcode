# 測試文檔 - NeetCode Runner System

## 概述

本專案在 `test/core-runner-baseline` 分支上建立了完整的**行為測試（Characterization Tests）**套件，用於確保重構過程中不會破壞現有功能。

## 測試負責人

**luffdev** - 單元測試負責人

## 核心目標

> 用測試把「行為」釘死，幫忙守住重構不爆炸

## 測試策略

### 1. 行為測試（Characterization Tests）

針對 `main` 分支上的舊版實作，建立測試確保：

- ✅ 給一樣的輸入 → always 一樣輸出
- ✅ 邊界情況（空輸入、錯誤輸入、大資料）都被測到
- ✅ 這些測試之後會變成**重構後必須通過的驗證標準**

### 2. 測試分類

#### 單元測試（Unit Tests）
- `test_util.py` - 工具函數測試
- `test_case_runner.py` - 單案例執行器測試
- `test_test_runner.py` - 測試執行器核心功能測試
- `test_complexity_estimator.py` - 複雜度估算器測試

#### 邊界測試（Edge Case Tests）
- `test_edge_cases.py` - 涵蓋：
  - 空輸入
  - 錯誤輸入
  - 大資料（1MB+）
  - 特殊字元（Unicode、emoji、CJK）
  - 格式錯誤的資料

#### 整合測試（Integration Tests）
- `test_integration.py` - 端到端工作流程測試：
  - 單案例執行流程
  - 多案例執行流程
  - 多解法支援
  - 比較模式（exact/sorted/set）
  - JUDGE_FUNC 支援

## 測試覆蓋範圍

### runner/util.py
- ✅ `normalize_output()` - 輸出正規化
- ✅ `compare_outputs()` - 三種比較模式（exact/sorted/set）
- ✅ `compare_result()` - 支援 JUDGE_FUNC
- ✅ `_compare_sorted()` - 排序比較輔助函數
- ✅ `_compare_set()` - 集合比較輔助函數
- ✅ 路徑輔助函數（get_solution_path, get_test_input_path, etc.）
- ✅ 檔案操作函數（read_file, write_file, file_exists）

### runner/case_runner.py
- ✅ 命令列參數解析和驗證
- ✅ 檔案存在性檢查
- ✅ 錯誤處理（缺少參數、檔案不存在）
- ✅ 單一測試案例執行流程

### runner/test_runner.py
- ✅ `normalize_output()` - 輸出正規化
- ✅ `load_solution_module()` - 解法模組載入
- ✅ `load_generator_module()` - 生成器模組載入
- ✅ `run_one_case()` - 單案例執行
- ✅ `save_failed_case()` - 失敗案例保存
- ✅ `truncate_input()` - 輸入截斷
- ✅ `format_validation_label()` - 驗證標籤格式化
- ✅ `run_method_tests()` - 多解法測試
- ✅ `print_benchmark_summary()` - 效能摘要輸出

### runner/complexity_estimator.py
- ✅ `ComplexityResult` - 結果資料類別
- ✅ `ComplexityEstimator.is_available()` - 可用性檢查
- ✅ `ComplexityEstimator.can_estimate()` - 估算能力檢查
- ✅ `ComplexityEstimator.estimate()` - 複雜度估算
- ✅ `_run_with_mock_stdin()` - Mock stdin 機制
- ✅ `format_complexity_result()` - 結果格式化

## 測試統計

- **測試檔案數量**: 6
- **測試類別數量**: 50+
- **測試案例數量**: 150+
- **測試標記**:
  - `@pytest.mark.unit` - 單元測試
  - `@pytest.mark.integration` - 整合測試
  - `@pytest.mark.edge_case` - 邊界測試
  - `@pytest.mark.slow` - 慢速測試
  - `@pytest.mark.requires_big_o` - 需要 big-O 套件

## 如何運行測試

### 安裝依賴

```bash
python -m pip install pytest pytest-cov
```

### 運行所有測試

```bash
# Windows
run_unit_tests.bat

# Linux/Mac
./run_unit_tests.sh

# 或直接使用 pytest
python -m pytest tests_unit -v
```

### 運行特定測試

```bash
# 只運行單元測試
python -m pytest tests_unit -v -m unit

# 只運行整合測試
python -m pytest tests_unit -v -m integration

# 只運行邊界測試
python -m pytest tests_unit -v -m edge_case

# 運行特定檔案
python -m pytest tests_unit/test_util.py -v
```

### 生成覆蓋率報告

```bash
python -m pytest tests_unit --cov=runner --cov-report=html
```

## 測試原則

### 1. 行為優先
測試「做什麼」而不是「怎麼做」。重構可以改變實作，但不能改變行為。

### 2. 輸入輸出驗證
給定相同輸入，必須得到相同輸出。這是行為測試的核心。

### 3. 邊界條件覆蓋
測試極端情況：
- 空輸入
- 最小值/最大值
- 錯誤格式
- 大資料量
- 特殊字元

### 4. 獨立性
每個測試獨立運行，不依賴其他測試的執行順序或狀態。

### 5. 可重複性
測試結果必須是確定性的，不受時間、環境等因素影響。

## 重構工作流程

### 階段 1: 建立基線（✅ 已完成）
1. ✅ 在 `test/core-runner-baseline` 分支建立測試
2. ✅ 針對舊實作寫測試
3. ✅ 確保所有測試通過

### 階段 2: 重構驗證（待進行）
1. 切換到重構分支
2. 進行重構
3. 運行測試確保行為一致
4. 如果測試失敗：
   - 檢查是否為預期的行為改變
   - 如果是意外破壞，修復代碼
   - 如果是預期改變，更新測試

### 階段 3: 持續維護
1. 新功能必須附帶測試
2. Bug 修復必須先寫測試重現問題
3. 定期運行測試確保品質

## 測試覆蓋的關鍵場景

### 1. 基本功能
- ✅ 讀取測試輸入
- ✅ 執行解法
- ✅ 比較輸出
- ✅ 報告結果

### 2. 多解法支援
- ✅ SOLUTIONS 元資料載入
- ✅ 環境變數傳遞（SOLUTION_METHOD）
- ✅ 多解法效能比較
- ✅ 複雜度資訊顯示

### 3. 比較模式
- ✅ exact - 精確匹配
- ✅ sorted - 排序後比較
- ✅ set - 集合比較（忽略順序和重複）

### 4. 自訂驗證
- ✅ JUDGE_FUNC 支援
- ✅ judge-only 模式（無 .out 檔案）
- ✅ 自訂驗證邏輯

### 5. 生成器支援
- ✅ 隨機測試生成
- ✅ 失敗案例保存
- ✅ 種子重現

### 6. 複雜度估算
- ✅ big-O 整合
- ✅ Mock stdin 機制
- ✅ 多次運行平均

## 已知限制和注意事項

1. **Python 版本**: 測試在 Python 3.14.2 上開發
2. **big-O 套件**: 複雜度估算測試需要 `big-O` 套件
3. **檔案系統**: 某些測試會創建臨時檔案
4. **路徑分隔符**: 測試考慮了 Windows/Unix 路徑差異

## 測試檔案結構

```
tests_unit/
├── __init__.py                    # 套件初始化
├── test_util.py                   # util.py 測試（40+ 測試）
├── test_case_runner.py            # case_runner.py 測試（15+ 測試）
├── test_test_runner.py            # test_runner.py 測試（30+ 測試）
├── test_complexity_estimator.py   # complexity_estimator.py 測試（25+ 測試）
├── test_edge_cases.py             # 邊界測試（40+ 測試）
├── test_integration.py            # 整合測試（20+ 測試）
└── README.md                      # 測試說明文檔
```

## 配置檔案

- `pytest.ini` - pytest 配置
- `run_unit_tests.bat` - Windows 測試執行腳本
- `run_unit_tests.sh` - Unix/Linux 測試執行腳本

## 下一步

1. **確保測試通過**: 在當前環境運行所有測試
2. **建立 CI/CD**: 整合到持續整合流程
3. **覆蓋率目標**: 達到 80%+ 的代碼覆蓋率
4. **效能基準**: 建立效能基準測試
5. **文檔完善**: 持續更新測試文檔

## 聯絡資訊

**測試負責人**: luffdev  
**分支**: `test/core-runner-baseline`  
**建立日期**: 2025-12-08

---

## 附錄: 測試命令快速參考

```bash
# 安裝依賴
python -m pip install pytest pytest-cov

# 運行所有測試
python -m pytest tests_unit -v

# 運行特定標記的測試
python -m pytest tests_unit -v -m unit
python -m pytest tests_unit -v -m integration
python -m pytest tests_unit -v -m edge_case

# 運行特定檔案
python -m pytest tests_unit/test_util.py -v

# 生成覆蓋率報告
python -m pytest tests_unit --cov=runner --cov-report=html

# 運行並顯示詳細輸出
python -m pytest tests_unit -v --tb=long

# 運行並在第一個失敗時停止
python -m pytest tests_unit -v -x

# 運行失敗的測試
python -m pytest tests_unit -v --lf
```

