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
    
    # State for multiline arrays
    multiline_key: str | None = None
    multiline_value_lines: list[str] = []
    multiline_target: dict | None = None

    for line in content.splitlines():
        stripped = line.strip()
        
        # Skip empty lines and comments (but not when inside multiline array)
        if not stripped or stripped.startswith("#"):
            if multiline_key is None:
                continue
            # Inside multiline array, skip comment lines but continue
            if stripped.startswith("#"):
                continue
        
        # Handle multiline array continuation
        if multiline_key is not None:
            multiline_value_lines.append(stripped)
            # Check if array is closed
            joined = " ".join(multiline_value_lines)
            if joined.count("[") <= joined.count("]"):
                # Array complete, parse it
                full_value = strip_inline_comment(joined)
                parsed_value = parse_toml_value(full_value)
                multiline_target[multiline_key] = parsed_value
                multiline_key = None
                multiline_value_lines = []
                multiline_target = None
            continue

        # Array header: [[array_name]]
        if stripped.startswith("[[") and stripped.endswith("]]"):
            if current_array_name and current_item:
                result.setdefault(current_array_name, []).append(current_item)
            current_array_name = stripped[2:-2].strip()
            current_table_name = None
            current_item = {}
            continue

        # Table header: [table_name]
        if stripped.startswith("[") and stripped.endswith("]") and not stripped.startswith("[["):
            if current_array_name and current_item:
                result.setdefault(current_array_name, []).append(current_item)
                current_item = {}
                current_array_name = None
            current_table_name = stripped[1:-1].strip()
            result.setdefault(current_table_name, {})
            continue

        # Key-value pair
        if "=" in stripped:
            key, _, value = stripped.partition("=")
            key, value = key.strip(), value.strip()
            # Remove inline comments (but not inside strings or arrays)
            value = strip_inline_comment(value)
            
            # Check for multiline array (starts with [ but doesn't end with ])
            if value.startswith("[") and not value.endswith("]"):
                # Start of multiline array
                multiline_key = key
                multiline_value_lines = [value]
                if current_array_name:
                    multiline_target = current_item
                elif current_table_name:
                    multiline_target = result[current_table_name]
                else:
                    multiline_target = result
                continue
            
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


def strip_inline_comment(value: str) -> str:
    """Strip inline comment from a TOML value, respecting strings and arrays."""
    result = []
    in_string = False
    string_char = None
    in_array = 0
    
    i = 0
    while i < len(value):
        char = value[i]
        
        # Handle string boundaries
        if char in ('"', "'") and not in_string:
            in_string = True
            string_char = char
            result.append(char)
        elif char == string_char and in_string:
            in_string = False
            string_char = None
            result.append(char)
        # Handle array boundaries
        elif char == '[' and not in_string:
            in_array += 1
            result.append(char)
        elif char == ']' and not in_string:
            in_array -= 1
            result.append(char)
        # Handle comment outside strings and arrays
        elif char == '#' and not in_string and in_array == 0:
            # Found comment, stop here
            break
        else:
            result.append(char)
        
        i += 1
    
    return ''.join(result).strip()


def parse_toml_value(value: str) -> Any:
    """Parse a TOML value string."""
    value = value.strip()
    
    # String value
    if value.startswith('"') and value.endswith('"'):
        result = value[1:-1]
        # Handle escape sequences
        result = result.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
        result = result.replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
        return result
    if value.startswith("'") and value.endswith("'"):
        # Literal strings (single quotes) don't process escapes
        return value[1:-1]
    
    # Array value
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        
        items = []
        current_item = ""
        in_quotes = False
        quote_char = None
        
        for char in inner:
            if char in ('"', "'") and (not in_quotes or char == quote_char):
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                else:
                    in_quotes = False
                    quote_char = None
                current_item += char
            elif char == "," and not in_quotes:
                if current_item.strip():
                    item = current_item.strip()
                    # Remove quotes if present
                    if (item.startswith('"') and item.endswith('"')) or (item.startswith("'") and item.endswith("'")):
                        item = item[1:-1]
                    items.append(item)
                current_item = ""
            else:
                current_item += char
        
        # Add last item
        if current_item.strip():
            item = current_item.strip()
            if (item.startswith('"') and item.endswith('"')) or (item.startswith("'") and item.endswith("'")):
                item = item[1:-1]
            items.append(item)
        
        return items
    
    # Boolean values
    if value == "true":
        return True
    if value == "false":
        return False
    
    # Try integer
    try:
        return int(value)
    except ValueError:
        pass
    
    # Try float
    try:
        return float(value)
    except ValueError:
        pass
    
    # Return as string
    return value

