# tools/patterndocs/toml_parser.py
"""Simple TOML parser for pattern documentation."""

from __future__ import annotations
from typing import Any


def parse_toml_simple(content: str) -> dict[str, Any]:
    """Parse TOML content into a dictionary."""
    result: dict[str, Any] = {}
    current_array_name: str | None = None
    current_item: dict[str, str] = {}

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Array header: [[array_name]]
        if line.startswith("[[") and line.endswith("]]"):
            if current_array_name and current_item:
                result.setdefault(current_array_name, []).append(current_item)
            current_array_name = line[2:-2].strip()
            current_item = {}
            continue

        # Key-value pair
        if "=" in line:
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            # Remove quotes
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            if current_array_name:
                current_item[key] = value
            else:
                result[key] = value

    # Last item
    if current_array_name and current_item:
        result.setdefault(current_array_name, []).append(current_item)

    return result

