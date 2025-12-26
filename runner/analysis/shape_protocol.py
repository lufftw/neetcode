# runner/analysis/shape_protocol.py
"""
Shape Protocol - Communication protocol for subprocess to report input shapes.

The subprocess (solution execution) has access to actual Python objects.
It can compute and report shapes back to the main process via a special
output format.

Protocol:
    Subprocess outputs: __SHAPE__:{"n": 1000, "k": 3}__END_SHAPE__
    Main process parses this from stderr or a separate channel.

This is similar to how profilers inject instrumentation code.
"""
import json
import sys
import re
from typing import Dict, Any, Optional

# Shape output markers (use unique strings unlikely to appear in normal output)
SHAPE_START = "__SHAPE__:"
SHAPE_END = "__END_SHAPE__"

# Pattern to extract shape from output
SHAPE_PATTERN = re.compile(rf'{re.escape(SHAPE_START)}(.+?){re.escape(SHAPE_END)}')


def emit_shape(shape_dict: Dict[str, Any], file=sys.stderr) -> None:
    """
    Emit shape information from subprocess.
    
    Called by solution wrapper after parsing input.
    Outputs to stderr to not interfere with stdout result.
    
    Example:
        # In solution wrapper
        nums = parse_input()  # e.g., [1, 2, 3, 4, 5]
        emit_shape({'n': len(nums)})
    """
    json_str = json.dumps(shape_dict, separators=(',', ':'))
    print(f"{SHAPE_START}{json_str}{SHAPE_END}", file=file, flush=True)


def parse_shape_from_output(output: str) -> Optional[Dict[str, Any]]:
    """
    Parse shape information from subprocess output.
    
    Called by main process after subprocess completes.
    
    Returns:
        Shape dict if found, None otherwise
    """
    match = SHAPE_PATTERN.search(output)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return None


def strip_shape_from_output(output: str) -> str:
    """Remove shape markers from output for clean display."""
    return SHAPE_PATTERN.sub('', output).strip()


__all__ = [
    'SHAPE_START',
    'SHAPE_END',
    'emit_shape',
    'parse_shape_from_output',
    'strip_shape_from_output',
]

