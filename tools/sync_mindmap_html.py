#!/usr/bin/env python3
"""
Sync Mindmap Markdown to HTML.

Reads a markdown file and generates the corresponding HTML file
with the markdown content embedded for Markmap rendering.

Usage:
    python tools/sync_mindmap_html.py docs/mindmaps/neetcode-ontology-agent-evolved-zh-tw.md
    python tools/sync_mindmap_html.py --all  # Sync all md files in docs/mindmaps/
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def get_title_from_frontmatter(content: str) -> str:
    """Extract title from YAML frontmatter."""
    match = re.search(r'^---\s*\n.*?^title:\s*(.+?)\s*$.*?^---', content, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return "NeetCode Mind Maps"


def generate_html(markdown_content: str, title: str) -> str:
    """Generate HTML with embedded markdown for Markmap."""
    # Escape backticks and backslashes for JS template literal
    escaped_content = markdown_content.replace("\\", "\\\\").replace("`", "\\`")
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - NeetCode Mind Maps</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ height: 100%; }}
        .markmap {{ width: 100%; height: 100%; }}
        .markmap > svg {{ width: 100%; height: 100%; }}
        #topbar {{
            position: fixed; top: 0; left: 0; right: 0; z-index: 100;
            background: #fff; border-bottom: 1px solid #e5e7eb;
            padding: 8px 16px; display: flex; gap: 8px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 13px;
        }}
        #topbar button {{
            padding: 4px 12px; border: 1px solid #d1d5db;
            border-radius: 4px; background: #fff; cursor: pointer;
        }}
        #topbar button:hover {{ background: #f3f4f6; }}
        .markmap {{ margin-top: 40px; height: calc(100% - 40px); }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-lib"></script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-toolbar"></script>
    <script>
        function fitView() {{
            var svg = document.querySelector('.markmap > svg');
            if (svg && svg.mm) svg.mm.fit();
        }}
        function expandAll() {{
            var svg = document.querySelector('.markmap > svg');
            if (svg && svg.mm) {{
                var root = svg.mm.state.data;
                (function expand(n) {{
                    n.payload = Object.assign({{}}, n.payload, {{ fold: 0 }});
                    if (n.children) n.children.forEach(expand);
                }})(root);
                svg.mm.setData(root); svg.mm.fit();
            }}
        }}
        function collapseAll() {{
            var svg = document.querySelector('.markmap > svg');
            if (svg && svg.mm) {{
                var root = svg.mm.state.data;
                root.children && root.children.forEach(function collapse(n) {{
                    if (n.children && n.children.length) {{
                        n.payload = Object.assign({{}}, n.payload, {{ fold: 1 }});
                        n.children.forEach(collapse);
                    }}
                }});
                svg.mm.setData(root); svg.mm.fit();
            }}
        }}
        document.addEventListener('DOMContentLoaded', function() {{
            const {{ Transformer, Markmap }} = window.markmap;
            const transformer = new Transformer();
            const markdown = `{escaped_content}`;
            const {{ root }} = transformer.transform(markdown);
            const svg = d3.select('.markmap').append('svg');
            const mm = Markmap.create(svg.node(), {{ color: (node) => node.payload?.color || '#f59e0b' }}, root);
            svg.node().mm = mm;
            if (window.markmap && window.markmap.Toolbar) {{
                const toolbar = new window.markmap.Toolbar();
                toolbar.attach(mm);
                setTimeout(function() {{
                    document.querySelectorAll('.mm-toolbar').forEach(function(toolbar) {{
                        toolbar.querySelectorAll('.mm-toolbar-item').forEach(function(item) {{
                            if ((item.title || '').toLowerCase().includes('dark')) item.remove();
                        }});
                        var brand = toolbar.querySelector('.mm-toolbar-brand');
                        if (brand) {{
                            brand.innerHTML = '🟡 NeetCode';
                            brand.href = '#'; brand.onclick = function(e) {{ e.preventDefault(); }};
                            brand.style.fontSize = '12px'; brand.style.color = '#666';
                        }}
                    }});
                }}, 200);
            }}
        }});
    </script>
</head>
<body>
    <div id="topbar">
        <button onclick="fitView()">Fit View</button>
        <button onclick="expandAll()">Expand All</button>
        <button onclick="collapseAll()">Collapse All</button>
    </div>
    <div class="markmap"></div>
</body>
</html>'''


def sync_file(md_path: Path, html_dir: Path) -> Path:
    """Sync a single markdown file to HTML."""
    content = md_path.read_text(encoding="utf-8")
    title = get_title_from_frontmatter(content)
    html_content = generate_html(content, title)
    
    html_path = html_dir / f"{md_path.stem}.html"
    html_path.write_text(html_content, encoding="utf-8")
    
    return html_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Mindmap Markdown to HTML")
    parser.add_argument(
        "files",
        nargs="*",
        help="Markdown files to sync"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Sync all .md files in docs/mindmaps/"
    )
    
    args = parser.parse_args()
    
    # Determine project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent if script_dir.name == "tools" else script_dir
    
    md_dir = project_root / "docs" / "mindmaps"
    html_dir = project_root / "docs" / "pages" / "mindmaps"
    html_dir.mkdir(parents=True, exist_ok=True)
    
    if args.all:
        files = list(md_dir.glob("*.md"))
    elif args.files:
        files = [Path(f) for f in args.files]
    else:
        print("Usage: python tools/sync_mindmap_html.py <file.md> or --all")
        return 1
    
    if not files:
        print("No markdown files found.")
        return 1
    
    print(f"\n🔄 Syncing {len(files)} file(s)...\n")
    
    for md_path in files:
        if not md_path.exists():
            print(f"  ❌ Not found: {md_path}")
            continue
        
        html_path = sync_file(md_path, html_dir)
        print(f"  ✓ {md_path.name} → {html_path.name}")
    
    print(f"\n✅ Done! HTML files saved to: {html_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

