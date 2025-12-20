# mkdocs_plugins/mindmaps_lastmod.py
"""
MkDocs plugin: provide lastmod timestamps for static files.

Behavior:
- mkdocs.yml only enables this plugin.
- Configuration is read from a sidecar file with the same basename:
    mkdocs_plugins/mindmaps_lastmod.yml
- For each matched static file:
    - Prefer Git commit time
    - Fallback to file mtime if Git info is unavailable

Output:
  config.extra["static_lastmod"][f.url] = "<ISO-8601 timestamp>"
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files, File

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


class MindmapsLastmodPlugin(BasePlugin):
    EXTRA_KEY = "static_lastmod"

    def on_files(self, files: Files, config) -> Files:
        rules = self._load_rules()
        if not rules:
            return files  # no-op

        docs_dir = Path(config["docs_dir"]).resolve()
        repo_root = self._guess_repo_root(config)

        mapping: Dict[str, str] = {}

        for f in files:
            if not self._match(f, rules):
                continue

            src = f.src_path or ""
            abs_path = (docs_dir / src).resolve()
            if not abs_path.exists():
                continue

            lastmod = (
                self._git_lastmod_iso(repo_root, abs_path)
                or self._file_mtime_iso(abs_path)
            )

            if lastmod:
                mapping[f.url] = lastmod

        if mapping:
            extra = config.get("extra") or {}
            extra[self.EXTRA_KEY] = mapping
            config["extra"] = extra

        return files

    # ------------------------------------------------------------------ config

    def _load_rules(self) -> List[Tuple[str, List[str]]]:
        if yaml is None:
            return []

        sidecar = Path(__file__).with_suffix(".yml")
        if not sidecar.exists():
            return []

        try:
            raw = yaml.safe_load(sidecar.read_text(encoding="utf-8")) or {}
        except Exception:
            return []

        rules_raw = raw.get("rules")
        if not isinstance(rules_raw, list):
            return []

        rules: List[Tuple[str, List[str]]] = []

        for item in rules_raw:
            if not isinstance(item, dict):
                continue

            path = str(item.get("path", "")).strip()
            exts = item.get("extensions", [])

            if not path or not isinstance(exts, list) or not exts:
                continue

            prefix = path.replace("\\", "/").rstrip("/") + "/"

            norm_exts: List[str] = []
            for e in exts:
                e = str(e).strip().lower()
                if not e:
                    continue
                if not e.startswith("."):
                    e = "." + e
                norm_exts.append(e)

            if norm_exts:
                rules.append((prefix, norm_exts))

        return rules

    # ---------------------------------------------------------------- matching

    def _match(self, f: File, rules: List[Tuple[str, List[str]]]) -> bool:
        src = (f.src_path or "").replace("\\", "/").lower()
        for prefix, exts in rules:
            if src.startswith(prefix.lower()) and any(src.endswith(e) for e in exts):
                return True
        return False

    # ------------------------------------------------------------------- utils

    def _guess_repo_root(self, config) -> Path:
        cfg = config.get("config_file_path")
        if cfg:
            return Path(cfg).resolve().parent
        return Path(os.getcwd()).resolve()

    def _git_lastmod_iso(self, repo_root: Path, file_path: Path) -> Optional[str]:
        try:
            rel = os.path.relpath(str(file_path), str(repo_root))
            out = subprocess.check_output(
                ["git", "log", "-1", "--format=%cI", "--", rel],
                cwd=str(repo_root),
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
            return out or None
        except Exception:
            return None

    def _file_mtime_iso(self, file_path: Path) -> Optional[str]:
        try:
            ts = os.path.getmtime(file_path)
            return (
                __import__("datetime")
                .datetime.fromtimestamp(ts, tz=__import__("datetime").timezone.utc)
                .isoformat()
            )
        except Exception:
            return None
