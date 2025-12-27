# 🔧 NeetCode Tools

Developer tools for checking, validating, and generating project content.

---

## 📁 Directory Structure

```
tools/
├── mindmaps/              # 🗺️ 思維導圖工具
│   ├── core/              # 核心模組
│   ├── ai-markmap-agent/  # AI 思維導圖代理
│   ├── ai_mindmap/        # AI 思維導圖模組
│   ├── hooks/             # Git hooks
│   ├── prompts/           # AI 提示詞
│   ├── shared/            # 共享工具
│   ├── tests/             # 測試
│   └── *.py               # 入口腳本
│
├── pattern-docs/          # 📚 模式文檔生成
│
├── review-code/           # 🔍 代碼審查
│   └── validation/        # 驗證工具
│
├── docstring/             # 📝 文檔字符串工具
│
├── leetcode-api/          # 🔗 LeetCode API
│
├── maintenance/           # 🔧 維護工具
│   └── doc-naming/        # 文檔命名工具
│
└── _staging/              # 📦 暫存區（待整理）
```

---

## 📋 Quick Reference

| Category | Tool | Purpose |
|----------|------|---------|
| **Mind Maps** | `mindmaps/generate_mindmaps.py` | Rule-based mind map generation |
| | `mindmaps/generate_mindmaps_ai.py` | AI-powered mind map generation |
| | `mindmaps/sync_mindmap_html.py` | Sync markdown to HTML |
| | `mindmaps/html_meta_description_generator.py` | Generate SEO meta descriptions |
| **Pattern Docs** | `pattern-docs/generate_pattern_docs.py` | Pattern documentation generation |
| **Validation** | `review-code/validation/check_solutions.py` | Validate solution file compliance |
| | `review-code/validation/run_format_tests.py` | Run format unit tests |
| | `review-code/validation/check_test_files.py` | Check test files format |
| **Docstring** | `docstring/formatter.py` | Docstring formatting |

---

## 🚀 Quick Start

```bash
# Generate mind maps (rule-based)
python tools/mindmaps/generate_mindmaps.py --html

# Generate mind maps (AI)
python tools/mindmaps/generate_mindmaps_ai.py --goal interview

# Generate pattern documentation
python tools/pattern-docs/generate_pattern_docs.py

# Check all solution files
python tools/review-code/validation/check_solutions.py

# Generate SEO meta descriptions
python tools/mindmaps/html_meta_description_generator.py
```

---

## 📚 Full Documentation

For complete documentation, please see:

- **[Tools Overview](../docs/tools/README.md)** - Complete tools reference
- **[AI Markmap Agent](mindmaps/ai-markmap-agent/docs/)** - AI-powered mind map generation
- **[Pattern Docs Generator](../docs/tools/patterndocs/README.md)** - Pattern documentation guide
- **[Reorganization Plan](reorganization-plan.md)** - Directory restructuring details

---

**Note**: See `reorganization-plan.md` for the complete restructuring plan and path migration details.
