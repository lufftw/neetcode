# tools/patterndocs/toml_parser.py
"""Simple TOML parser for pattern documentation."""

from __future__ import annotations
from typing import Any


def parse_toml_simple(content: str) -> dict[str, Any]:
    """Parse TOML content into a dictionary."""
    result: dict[str, Any] = {}
    current_array_name: str | None = None
    current_item: dict[str, str] = {}
    current_array_key: str | None = None
    current_array_items: list[str] = []
    in_multiline_array = False

    lines = content.splitlines()
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines and comments
        if not line or line.startswith("#"):
            i += 1
            continue

        # Array header: [[array_name]]
        if line.startswith("[[") and line.endswith("]]"):
            if current_array_name and current_item:
                result.setdefault(current_array_name, []).append(current_item)
            current_array_name = line[2:-2].strip()
            current_item = {}
            in_multiline_array = False
            i += 1
            continue

        # Key-value pair
        if "=" in line:
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            
            # Check if this is a multiline array start: key = [
            if value == "[":
                current_array_key = key
                current_array_items = []
                in_multiline_array = True
                i += 1
                continue
            
            # Parse TOML array format: ["item1", "item2"] (single line)
            if value.startswith("[") and value.endswith("]"):
                # Extract array items
                items_str = value[1:-1].strip()
                if not items_str:
                    parsed_value = []
                else:
                    # Split by comma and clean up items
                    items = []
                    for item in items_str.split(","):
                        item = item.strip()
                        # Remove quotes
                        if item.startswith('"') and item.endswith('"'):
                            item = item[1:-1]
                        elif item.startswith("'") and item.endswith("'"):
                            item = item[1:-1]
                        if item:
                            items.append(item)
                    parsed_value = items
            # Remove quotes for single string values
            elif value.startswith('"') and value.endswith('"'):
                parsed_value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                parsed_value = value[1:-1]
            else:
                parsed_value = value
            
            if current_array_name:
                current_item[key] = parsed_value
            else:
                result[key] = parsed_value
            i += 1
            continue
        
        # Handle multiline array items
        if in_multiline_array:
            # Check for array end: ]
            if line == "]":
                if current_array_key:
                    result[current_array_key] = current_array_items
                current_array_key = None
                in_multiline_array = False
                i += 1
                continue
            
            # Parse array item (remove quotes and comma)
            item = line.rstrip(",").strip()
            if item.startswith('"') and item.endswith('"'):
                item = item[1:-1]
            elif item.startswith("'") and item.endswith("'"):
                item = item[1:-1]
            if item:
                current_array_items.append(item)
            i += 1
            continue
        
        i += 1

    # Last item
    if current_array_name and current_item:
        result.setdefault(current_array_name, []).append(current_item)

    return result

