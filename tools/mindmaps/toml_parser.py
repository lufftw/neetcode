# tools/mindmaps/toml_parser.py
"""Simple TOML parser for mind map generation."""

from __future__ import annotations
from typing import Any


def parse_toml_simple(content: str) -> dict[str, Any]:
    """Parse TOML content into a dictionary."""
    result: dict[str, Any] = {}
    current_array_name: str | None = None
    current_table_name: str | None = None
    current_item: dict[str, Any] = {}

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Array header: [[array_name]]
        if line.startswith("[[") and line.endswith("]]"):
            if current_array_name and current_item:
                result.setdefault(current_array_name, []).append(current_item)
            current_array_name = line[2:-2].strip()
            current_table_name = None
            current_item = {}
            continue

        # Table header: [table_name]
        if line.startswith("[") and line.endswith("]") and not line.startswith("[["):
            if current_array_name and current_item:
                result.setdefault(current_array_name, []).append(current_item)
                current_item = {}
                current_array_name = None
            current_table_name = line[1:-1].strip()
            result.setdefault(current_table_name, {})
            continue

        # Key-value pair
        if "=" in line:
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            parsed_value = parse_toml_value(value)

            if current_array_name:
                current_item[key] = parsed_value
            elif current_table_name:
                result[current_table_name][key] = parsed_value
            else:
                result[key] = parsed_value

    # Last item
    if current_array_name and current_item:
        result.setdefault(current_array_name, []).append(current_item)

    return result


def parse_toml_value(value: str) -> Any:
    """Parse a TOML value string."""
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [
            item.strip()[1:-1] if item.strip().startswith('"') else item.strip()
            for item in inner.split(",") if item.strip()
        ]
    if value == "true":
        return True
    if value == "false":
        return False
    try:
        return int(value)
    except ValueError:
        return value

