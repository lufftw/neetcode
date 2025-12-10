# tools/mindmaps/templates.py
"""HTML templates for mind map generation."""

HTML_TEMPLATE_MANUAL = '''<!DOCTYPE html>
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
            const markdown = `{markdown_content}`;
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

HTML_TEMPLATE_AUTOLOADER = '''<!DOCTYPE html>
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
    <script>
        window.markmap = {{
            autoLoader: {{
                toolbar: true,
                onReady: function() {{
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
            }}
        }};
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
    </script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader"></script>
</head>
<body>
    <div id="topbar">
        <button onclick="fitView()">Fit View</button>
        <button onclick="expandAll()">Expand All</button>
        <button onclick="collapseAll()">Collapse All</button>
    </div>
    <div class="markmap">
{markdown_content}
    </div>
</body>
</html>'''

INDEX_HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeetCode Mind Maps</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🧠 <span>NeetCode</span> Mind Maps</h1>
            <p class="subtitle">Interactive visualizations of algorithm patterns and problem relationships</p>
        </header>
        <section>
            <h2>Available Mind Maps</h2>
            <div class="grid">{cards}</div>
        </section>
        <section class="tips">
            <h2>Navigation</h2>
            <ul>
                <li><strong>Drag</strong> — Move around</li>
                <li><strong>Scroll</strong> — Zoom in/out</li>
                <li><strong>Click node</strong> — Expand/collapse</li>
                <li><strong>Toolbar</strong> — Fit, zoom, fullscreen</li>
            </ul>
        </section>
        <footer>
            <p>Part of <a href="https://github.com/lufftw/neetcode">NeetCode Practice Framework</a></p>
            <p class="meta">Generated by <code>generate_mindmaps.py --html</code></p>
        </footer>
    </div>
</body>
</html>'''

CARD_TEMPLATE = '''                <a href="mindmaps/{filename}.html" class="card">
                    <div class="icon">{icon}</div>
                    <h3>{title}</h3>
                    <p>{description}</p>
                </a>'''

STYLE_CSS = ''':root {
    --bg: #ffffff; --bg-secondary: #f6f8fa; --border: #d0d7de;
    --text: #24292f; --text-muted: #57606a; --link: #0969da; --accent: #f59e0b;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.6; min-height: 100vh;
}
.container { max-width: 1100px; margin: 0 auto; padding: 3rem 2rem; }
header { text-align: center; margin-bottom: 3rem; }
h1 { font-size: 2.2rem; margin-bottom: 0.5rem; }
h1 span { color: var(--accent); }
.subtitle { color: var(--text-muted); font-size: 1rem; }
h2 { font-size: 1.2rem; margin-bottom: 1.5rem; font-weight: 600; }
section { margin-bottom: 3rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; }
.card {
    background: var(--bg); border: 1px solid var(--border); border-radius: 8px;
    padding: 1.25rem; text-decoration: none; color: var(--text);
    transition: all 0.15s ease; display: block;
}
.card:hover { border-color: var(--link); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); }
.card .icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.card h3 { color: var(--link); margin-bottom: 0.25rem; font-size: 1rem; font-weight: 600; }
.card p { color: var(--text-muted); font-size: 0.85rem; margin: 0; }
.tips {
    background: var(--bg-secondary); border: 1px solid var(--border);
    border-radius: 8px; padding: 1.25rem 1.5rem;
}
.tips h2 { margin-bottom: 1rem; }
.tips ul {
    list-style: none; display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;
}
.tips li { color: var(--text-muted); font-size: 0.85rem; }
footer {
    text-align: center; padding-top: 2rem; border-top: 1px solid var(--border);
    color: var(--text-muted); font-size: 0.85rem;
}
footer a { color: var(--link); text-decoration: none; }
footer a:hover { text-decoration: underline; }
footer .meta { margin-top: 0.5rem; font-size: 0.8rem; }
footer code { background: var(--bg-secondary); padding: 2px 6px; border-radius: 4px; font-size: 0.85em; }
'''

