# tools/shared/toml_parser.py
"""
Simple TOML parser for NeetCode tools.

This is a minimal TOML parser that handles our specific use cases:
- Basic key-value pairs
- Arrays of tables [[array]]
- Table sections [table]
- String, boolean, integer, and array values

For more complex TOML needs, consider using the `tomllib` standard library (Python 3.11+).
"""

from __future__ import annotations

from typing import Any


def parse_toml_simple(content: str) -> dict[str, Any]:
    """
    Simple TOML parser for our use case.
    
    Handles:
    - [[array]] syntax for arrays of tables
    - [table] syntax for nested tables
    - key = value pairs
    - Quoted strings, booleans, integers, arrays
    
    Args:
        content: TOML file content as string
    
    Returns:
        Parsed dictionary
    """
    result: dict[str, Any] = {}
    current_array_name: str | None = None
    current_table_name: str | None = None
    current_item: dict[str, Any] = {}

    for line in content.splitlines():
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue

        # Array header: [[array_name]]
        if line.startswith("[[") and line.endswith("]]"):
            if current_array_name and current_item:
                if current_array_name not in result:
                    result[current_array_name] = []
                result[current_array_name].append(current_item)

            current_array_name = line[2:-2].strip()
            current_table_name = None
            current_item = {}
            continue

        # Table header: [table_name]
        if line.startswith("[") and line.endswith("]") and not line.startswith("[["):
            if current_array_name and current_item:
                if current_array_name not in result:
                    result[current_array_name] = []
                result[current_array_name].append(current_item)
                current_item = {}
                current_array_name = None

            current_table_name = line[1:-1].strip()
            if current_table_name not in result:
                result[current_table_name] = {}
            continue

        # Key-value pair
        if "=" in line:
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()

            # Parse value
            parsed_value = parse_toml_value(value)

            if current_array_name:
                current_item[key] = parsed_value
            elif current_table_name:
                result[current_table_name][key] = parsed_value
            else:
                result[key] = parsed_value

    # Don't forget the last item
    if current_array_name and current_item:
        if current_array_name not in result:
            result[current_array_name] = []
        result[current_array_name].append(current_item)

    return result


def parse_toml_value(value: str) -> Any:
    """
    Parse a TOML value string into Python type.
    
    Handles:
    - Quoted strings: "hello" -> "hello"
    - Arrays: ["a", "b"] -> ["a", "b"]
    - Booleans: true/false -> True/False
    - Integers: 123 -> 123
    - Unquoted values: returned as-is
    
    Args:
        value: TOML value string
    
    Returns:
        Parsed Python value
    """
    # String
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]

    # Array
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        items = []
        for item in inner.split(","):
            item = item.strip()
            if item.startswith('"') and item.endswith('"'):
                items.append(item[1:-1])
            elif item:
                items.append(item)
        return items

    # Boolean
    if value == "true":
        return True
    if value == "false":
        return False

    # Number
    try:
        return int(value)
    except ValueError:
        pass

    return value

