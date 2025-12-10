# GitHub Pages 部署指南：互動心智圖

本指南說明如何將心智圖部署到 GitHub Pages，實現完全互動功能。

---

## 📊 完整流程圖

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        心智圖產生與部署流程                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐       │
│  │  資料來源  │ ──→ │  產生工具  │ ──→ │  輸出檔案  │ ──→ │ GitHub   │       │
│  └──────────┘     └──────────┘     └──────────┘     │ Pages    │       │
│                                                      └──────────┘       │
│  • ontology/*.toml   generate_         • *.md (靜態)                     │
│  • meta/problems/    mindmaps.py       • *.html (互動)   自動部署        │
│  • 任意文字           text_to_                                           │
│                      mindmap.py                                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ 目錄結構

```
neetcode/
├── docs/
│   ├── mindmaps/
│   │   ├── README.md                    # 心智圖索引
│   │   ├── pattern_hierarchy.md         # 靜態 Mermaid 版本
│   │   ├── algorithm_usage.md
│   │   └── ...
│   │
│   └── pages/                           # 🆕 GitHub Pages 根目錄
│       ├── index.html                   # 首頁
│       ├── mindmaps/                    # 互動心智圖
│       │   ├── index.html               # 心智圖列表
│       │   ├── pattern_hierarchy.html   # 互動版本
│       │   ├── algorithm_usage.html
│       │   └── ...
│       └── assets/
│           └── style.css
│
├── tools/
│   ├── generate_mindmaps.py             # 從 ontology 產生
│   ├── text_to_mindmap.py               # 從任意文字產生
│   └── build_pages.py                   # 🆕 建置 GitHub Pages
│
└── .github/
    └── workflows/
        └── deploy-pages.yml             # 🆕 自動部署
```

---

## 步驟 1：建立 GitHub Pages 結構

### 1.1 建立首頁

```html
<!-- docs/pages/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeetCode Mind Maps</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <div class="container">
        <h1>🧠 NeetCode Interactive Mind Maps</h1>
        <p>Visual representations of algorithm patterns and problem relationships.</p>
        
        <h2>Available Mind Maps</h2>
        <div class="grid">
            <a href="mindmaps/pattern_hierarchy.html" class="card">
                <h3>🔗 Pattern Hierarchy</h3>
                <p>API Kernels → Patterns → Problems</p>
            </a>
            <a href="mindmaps/family_derivation.html" class="card">
                <h3>🌳 Family Derivation</h3>
                <p>Base templates and derived variants</p>
            </a>
            <a href="mindmaps/algorithm_usage.html" class="card">
                <h3>⚙️ Algorithm Usage</h3>
                <p>Algorithms → Problems</p>
            </a>
            <a href="mindmaps/company_coverage.html" class="card">
                <h3>🏢 Company Coverage</h3>
                <p>Companies → Problems they ask</p>
            </a>
            <a href="mindmaps/roadmap_paths.html" class="card">
                <h3>🛣️ Learning Roadmaps</h3>
                <p>Study paths and progressions</p>
            </a>
            <a href="mindmaps/solution_variants.html" class="card">
                <h3>🔀 Solution Variants</h3>
                <p>Problems with multiple solutions</p>
            </a>
        </div>
        
        <footer>
            <p>Generated from <a href="https://github.com/yourusername/neetcode">NeetCode Repository</a></p>
        </footer>
    </div>
</body>
</html>
```

### 1.2 建立樣式

```css
/* docs/pages/assets/style.css */
:root {
    --bg: #0d1117;
    --card-bg: #161b22;
    --border: #30363d;
    --text: #c9d1d9;
    --text-muted: #8b949e;
    --link: #58a6ff;
    --accent: #238636;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

h2 {
    margin: 2rem 0 1rem;
    color: var(--text-muted);
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
}

.card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    text-decoration: none;
    color: var(--text);
    transition: border-color 0.2s, transform 0.2s;
}

.card:hover {
    border-color: var(--link);
    transform: translateY(-2px);
}

.card h3 {
    color: var(--link);
    margin-bottom: 0.5rem;
}

.card p {
    color: var(--text-muted);
    font-size: 0.9rem;
}

footer {
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    color: var(--text-muted);
    text-align: center;
}

footer a {
    color: var(--link);
}
```

---

## 步驟 2：建立互動心智圖 HTML

### 2.1 心智圖 HTML 範本

```html
<!-- docs/pages/mindmaps/pattern_hierarchy.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pattern Hierarchy - NeetCode Mind Maps</title>
    <style>
        body { margin: 0; padding: 0; }
        #toolbar {
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 1000;
            background: rgba(0,0,0,0.8);
            padding: 10px;
            border-radius: 8px;
        }
        #toolbar a, #toolbar button {
            color: white;
            margin-right: 10px;
            text-decoration: none;
        }
        #toolbar button {
            background: #238636;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
        }
        #mindmap { width: 100vw; height: 100vh; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-lib"></script>
</head>
<body>
    <div id="toolbar">
        <a href="../index.html">← Back</a>
        <button onclick="mm.fit()">Fit View</button>
        <button onclick="expandAll()">Expand All</button>
        <button onclick="collapseAll()">Collapse All</button>
    </div>
    
    <svg id="mindmap"></svg>
    
    <script>
        const { Transformer, Markmap } = window.markmap;
        const transformer = new Transformer();
        
        // Mind map content in Markdown
        const markdown = `
# API Kernels

## SubstringSlidingWindow
### sliding_window_unique
#### LeetCode 3 Longest Substring
### sliding_window_freq_cover
#### LeetCode 76 Min Window
### sliding_window_at_most_k
#### LeetCode 340 K Distinct
#### LeetCode 159 Two Distinct
### sliding_window_fixed_size
#### LeetCode 567 Permutation
#### LeetCode 438 Anagrams
### sliding_window_cost_bounded
#### LeetCode 209 Min Subarray

## KWayMerge
### merge_k_sorted_heap
#### LeetCode 23 Merge K Lists
### merge_k_sorted_divide
#### LeetCode 23 Divide Conquer
### merge_two_sorted
#### LeetCode 21 Merge Two

## GridBFSMultiSource
### grid_bfs_propagation
#### LeetCode 994 Rotting Oranges
### bfs_shortest_path
#### LeetCode 286 Walls Gates

## BacktrackingExploration
### backtracking_n_queens
#### LeetCode 51 N Queens
### backtracking_permutation
#### LeetCode 46 Permutations
### backtracking_combination
#### LeetCode 77 Combinations

## BinarySearchBoundary
### binary_search_on_answer
#### LeetCode 4 Median Arrays
### binary_search_rotated
#### LeetCode 33 Search Rotated

## LinkedListInPlaceReversal
### linked_list_k_group
#### LeetCode 25 Reverse K Group
### linked_list_full
#### LeetCode 206 Reverse List
`;
        
        const { root } = transformer.transform(markdown);
        const mm = Markmap.create('#mindmap', {
            autoFit: true,
            duration: 500,
            maxWidth: 300,
        }, root);
        
        function expandAll() {
            root.children?.forEach(function expand(n) {
                n.payload = { ...n.payload, fold: 0 };
                n.children?.forEach(expand);
            });
            mm.setData(root);
            mm.fit();
        }
        
        function collapseAll() {
            root.children?.forEach(function collapse(n) {
                if (n.children?.length) {
                    n.payload = { ...n.payload, fold: 1 };
                }
            });
            mm.setData(root);
            mm.fit();
        }
    </script>
</body>
</html>
```

---

## 步驟 3：建立自動建置腳本

```python
# tools/build_pages.py
#!/usr/bin/env python3
"""
Build GitHub Pages from mind map sources.

Usage:
    python tools/build_pages.py
"""

from pathlib import Path
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = PROJECT_ROOT / "docs" / "pages"
MINDMAPS_SOURCE = PROJECT_ROOT / "docs" / "mindmaps"
MINDMAPS_OUTPUT = PAGES_DIR / "mindmaps"

def build():
    """Build all pages."""
    print("Building GitHub Pages...")
    
    # Ensure output directory exists
    MINDMAPS_OUTPUT.mkdir(parents=True, exist_ok=True)
    
    # Copy static assets
    # (index.html and style.css should already exist)
    
    print(f"Output directory: {PAGES_DIR}")
    print("Done!")

if __name__ == "__main__":
    build()
```

---

## 步驟 4：設定 GitHub Actions 自動部署

```yaml
# .github/workflows/deploy-pages.yml
name: Deploy Mind Maps to GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'ontology/**'
      - 'meta/**'
  workflow_dispatch:  # 允許手動觸發

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Generate Mind Maps
        run: |
          python tools/generate_mindmaps.py --all
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: 'docs/pages'

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## 步驟 5：啟用 GitHub Pages

### 5.1 在 GitHub 設定

1. 進入你的 Repository → **Settings**
2. 左側選單找到 **Pages**
3. Source 選擇 **GitHub Actions**

### 5.2 手動部署（第一次）

```bash
# 1. 確保檔案結構正確
docs/
└── pages/
    ├── index.html
    ├── assets/
    │   └── style.css
    └── mindmaps/
        └── pattern_hierarchy.html

# 2. Commit 並 Push
git add .
git commit -m "feat: add GitHub Pages for interactive mind maps"
git push origin main

# 3. GitHub Actions 會自動部署
# 4. 訪問: https://yourusername.github.io/neetcode/
```

---

## 步驟 6：在 README 加入連結

```markdown
## 🧠 Interactive Mind Maps

Explore our algorithm patterns visually:

| Mind Map | Description | Links |
|----------|-------------|-------|
| Pattern Hierarchy | API Kernels → Patterns → Problems | [Static](docs/mindmaps/pattern_hierarchy.md) · [Interactive ✨](https://yourusername.github.io/neetcode/mindmaps/pattern_hierarchy.html) |
| Algorithm Usage | Which algorithms solve which problems | [Static](docs/mindmaps/algorithm_usage.md) · [Interactive ✨](https://yourusername.github.io/neetcode/mindmaps/algorithm_usage.html) |
| Company Coverage | Company interview questions | [Static](docs/mindmaps/company_coverage.md) · [Interactive ✨](https://yourusername.github.io/neetcode/mindmaps/company_coverage.html) |

👉 **[View All Interactive Mind Maps](https://yourusername.github.io/neetcode/)**
```

---

## 🔄 完整工作流程總結

```
1. 編輯 ontology/ 或 meta/problems/
   ↓
2. git push (或手動執行 python tools/generate_mindmaps.py)
   ↓
3. GitHub Actions 自動觸發
   ↓
4. 產生心智圖 (Markdown + HTML)
   ↓
5. 部署到 GitHub Pages
   ↓
6. 訪問 https://yourusername.github.io/neetcode/
   ↓
7. 使用互動心智圖！
   - 🖱️ 拖曳移動
   - 🔍 滾輪縮放
   - 👆 點擊折疊/展開
```

---

## ❓ 常見問題

### Q: 為什麼 GitHub README 不能直接互動？
A: GitHub 基於安全考量，禁止執行 JavaScript。所以需要 GitHub Pages 來託管互動版本。

### Q: 可以用自訂網域嗎？
A: 可以！在 Settings → Pages 設定 Custom domain。

### Q: 如何更新心智圖？
A: 修改 ontology/ 或 meta/ 後 push，GitHub Actions 會自動重新部署。

### Q: 本地預覽怎麼做？
A: 
```bash
# 方法 1: 直接開啟 HTML
open docs/pages/index.html

# 方法 2: 用簡單 HTTP server
cd docs/pages
python -m http.server 8000
# 訪問 http://localhost:8000
```
