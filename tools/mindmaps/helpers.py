# tools/mindmaps/helpers.py
"""Helper functions for mind map generation."""

from __future__ import annotations
import re
from .data import ProblemData


def markmap_frontmatter(title: str, color_freeze_level: int = 2) -> str:
    """Generate YAML frontmatter for markmap."""
    return f"""---
title: {title}
markmap:
  colorFreezeLevel: {color_freeze_level}
  maxWidth: 400
---
"""


def format_problem_entry(prob: ProblemData, show_complexity: bool = False) -> str:
    """Format a problem entry with link and metadata."""
    entry = prob.markdown_link(include_difficulty=True)
    if show_complexity and prob.solutions:
        complexity = prob.solutions[0].get("complexity", "")
        if complexity:
            entry += f" — `{complexity}`"
    return entry


def table_to_markmap_tree(markdown_content: str) -> str:
    """
    Convert Markdown tables to Markmap tree structure.
    
    Markmap doesn't support tables as structured nodes - they're rendered as plain text.
    This function converts tables into a hierarchical tree structure that Markmap can visualize.
    
    Example conversion:
    
    Input:
    | Problem | Invariant | State |
    |---------|-----------|-------|
    | LC 3    | Unique    | freq  |
    | LC 76   | Cover     | maps  |
    
    Output:
    - **Problem**: LC 3
      - **Invariant**: Unique
      - **State**: freq
    - **Problem**: LC 76
      - **Invariant**: Cover
      - **State**: maps
    
    Args:
        markdown_content: Markdown content that may contain tables
        
    Returns:
        Markdown content with tables converted to tree structure
    """
    lines = markdown_content.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts a table (has | characters and looks like a header)
        if '|' in line and not line.strip().startswith('```'):
            # Try to parse a table starting from this line
            table_lines = []
            table_start = i
            
            # Collect table lines (until we hit a non-table line or empty line)
            while i < len(lines) and ('|' in lines[i] or lines[i].strip() == ''):
                if lines[i].strip() and not lines[i].strip().startswith('```'):
                    table_lines.append(lines[i])
                elif lines[i].strip().startswith('```'):
                    # Stop if we hit a code block marker
                    break
                i += 1
            
            # Check if we have a valid table (at least header + separator + one row)
            if len(table_lines) >= 2:
                # Parse header
                header_line = table_lines[0]
                # Skip separator line (|----|----|)
                if len(table_lines) >= 2 and re.match(r'^\|[\s\-:]+\|', table_lines[1]):
                    separator_idx = 1
                    data_start = 2
                else:
                    separator_idx = -1
                    data_start = 1
                
                # Extract column headers
                headers = [cell.strip() for cell in header_line.split('|')[1:-1]]
                
                # Convert table to tree structure
                if headers and len(table_lines) > data_start:
                    # Add a comment to indicate this was converted from a table
                    result_lines.append("<!-- Converted from Markdown table -->")
                    
                    # Process each data row
                    for row_idx in range(data_start, len(table_lines)):
                        row_line = table_lines[row_idx]
                        if not row_line.strip() or row_line.strip().startswith('```'):
                            break
                        
                        # Extract row cells
                        cells = [cell.strip() for cell in row_line.split('|')[1:-1]]
                        
                        # Use first column as the main node, others as children
                        if cells and cells[0]:
                            # Main node (first column)
                            main_node = cells[0]
                            indent_level = 0
                            
                            # Add main node
                            result_lines.append(f"{'  ' * indent_level}- {main_node}")
                            
                            # Add other columns as child nodes
                            for col_idx in range(1, min(len(headers), len(cells))):
                                if col_idx < len(cells) and cells[col_idx]:
                                    header = headers[col_idx] if col_idx < len(headers) else f"Column {col_idx + 1}"
                                    value = cells[col_idx]
                                    result_lines.append(f"{'  ' * (indent_level + 1)}- **{header}**: {value}")
                    
                    # Skip the lines we just processed
                    continue
            
            # If not a valid table, just add the line as-is
            result_lines.append(line)
            i += 1
        else:
            result_lines.append(line)
            i += 1
    
    return '\n'.join(result_lines)


def convert_tables_in_markmap(markdown_content: str) -> str:
    """
    Convert all Markdown tables in Markmap content to tree structure.
    
    This is a wrapper that handles edge cases like tables inside code blocks.
    The function preserves code blocks and only converts tables outside of them.
    
    Args:
        markdown_content: Markmap Markdown content
        
    Returns:
        Content with tables converted to tree structure
    """
    lines = markdown_content.split('\n')
    result_lines = []
    i = 0
    in_code_block = False
    
    while i < len(lines):
        line = lines[i]
        
        # Track code block state
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result_lines.append(line)
            i += 1
            continue
        
        # Don't process tables inside code blocks
        if in_code_block:
            result_lines.append(line)
            i += 1
            continue
        
        # Check if this line starts a table (has | characters)
        if '|' in line:
            # Try to parse a table starting from this line
            table_lines = [line]
            table_start = i
            i += 1
            
            # Collect table lines (until we hit a non-table line or empty line)
            while i < len(lines):
                next_line = lines[i]
                
                # Stop if we hit a code block
                if next_line.strip().startswith('```'):
                    break
                
                # Stop if line doesn't contain | and is not empty
                if '|' not in next_line and next_line.strip():
                    break
                
                # Add table line (including empty lines within table)
                if '|' in next_line or (not next_line.strip() and table_lines):
                    table_lines.append(next_line)
                    i += 1
                else:
                    break
            
            # Check if we have a valid table (at least header + separator + one row)
            if len(table_lines) >= 2:
                # Parse header
                header_line = table_lines[0]
                # Check for separator line (|----|----|)
                separator_found = False
                data_start = 1
                
                if len(table_lines) >= 2:
                    second_line = table_lines[1]
                    if re.match(r'^\|[\s\-:]+\|', second_line):
                        separator_found = True
                        data_start = 2
                
                # Extract column headers
                headers = [cell.strip() for cell in header_line.split('|')[1:-1]]
                
                # Convert table to tree structure
                if headers and len(table_lines) > data_start:
                    # Process each data row
                    for row_idx in range(data_start, len(table_lines)):
                        row_line = table_lines[row_idx]
                        if not row_line.strip():
                            continue
                        
                        # Extract row cells
                        cells = [cell.strip() for cell in row_line.split('|')[1:-1]]
                        
                        # Use first column as the main node, others as children
                        if cells and cells[0]:
                            # Main node (first column)
                            main_node = cells[0]
                            indent_level = 0
                            
                            # Add main node
                            result_lines.append(f"{'  ' * indent_level}- {main_node}")
                            
                            # Add other columns as child nodes
                            for col_idx in range(1, min(len(headers), len(cells))):
                                if col_idx < len(cells) and cells[col_idx]:
                                    header = headers[col_idx] if col_idx < len(headers) else f"Column {col_idx + 1}"
                                    value = cells[col_idx]
                                    result_lines.append(f"{'  ' * (indent_level + 1)}- **{header}**: {value}")
                    
                    # Skip the lines we just processed (already handled)
                    continue
            
            # If not a valid table, add lines as-is
            result_lines.extend(table_lines)
        else:
            result_lines.append(line)
            i += 1
    
    return '\n'.join(result_lines)

