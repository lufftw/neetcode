# tools/patterndocs/kernel_extractor.py
"""Extract API Kernel ID from _header.md file."""

from __future__ import annotations
import re
from pathlib import Path


def extract_kernel_from_header(header_file: Path) -> str | None:
    """
    Extract API Kernel ID from _header.md file.
    
    Looks for pattern: > **API Kernel**: `KernelID`
    
    Returns:
        Kernel ID string if found, None otherwise
    """
    if not header_file.exists():
        return None
    
    try:
        content = header_file.read_text(encoding="utf-8")
        
        # Pattern: > **API Kernel**: `KernelID`
        pattern = r'>\s*\*\*API Kernel\*\*:\s*`([^`]+)`'
        match = re.search(pattern, content)
        
        if match:
            return match.group(1)
        
        # Alternative pattern: **API Kernel**: `KernelID` (without >)
        pattern2 = r'\*\*API Kernel\*\*:\s*`([^`]+)`'
        match2 = re.search(pattern2, content)
        
        if match2:
            return match2.group(1)
        
        return None
    except Exception as e:
        print(f"Warning: Failed to extract kernel from {header_file}: {e}")
        return None

