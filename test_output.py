#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "tools"))

from generate_pattern_docs import add_section_numbers

test_content = """## Core Concepts

### The Sliding Window Invariant

Some text here.

### Universal Template Structure

More text.
"""

numbered, info = add_section_numbers(test_content, 1)

output_file = Path(__file__).parent / "test_result.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("=== NUMBERED CONTENT ===\n")
    f.write(numbered[:500])
    f.write("\n\n=== SECTIONS INFO ===\n")
    f.write(str(info))


