# tools/patterndocs/files.py
"""File collection for pattern documentation."""

from __future__ import annotations
from pathlib import Path

from .toml_parser import parse_toml_simple

# Default file ordering (fallback if config not found)
# These can be overridden by generate_pattern_docs.toml
def get_default_file_order() -> tuple[list[str], list[str]]:
    """Get default file ordering from config or return defaults."""
    from .config import load_generator_config
    
    try:
        config = load_generator_config()
        default_order = config.get("default_file_order", {})
        
        header_files = default_order.get("header_files", ["_header.md"])
        footer_files = default_order.get("footer_files", [
            "_comparison.md",
            "_decision.md",
            "_mapping.md",
            "_templates.md"
        ])
        
        return header_files, footer_files
    except Exception:
        # Fallback to hardcoded defaults if config loading fails
        return ["_header.md"], ["_comparison.md", "_decision.md", "_mapping.md", "_templates.md"]


# For backward compatibility
STRUCTURAL_FILES_ORDER = ["_header.md"]
STRUCTURAL_FILES_FOOTER = ["_comparison.md", "_decision.md", "_mapping.md", "_templates.md"]


def load_config(source_dir: Path) -> dict:
    """
    Load file ordering configuration from _config.toml if it exists.
    
    Returns:
        Dictionary with 'header_files', 'problem_files', 'footer_files' lists,
        and optionally 'output' configuration,
        or empty dict if config file doesn't exist.
    """
    config_path = source_dir / "_config.toml"
    if not config_path.exists():
        return {}
    
    try:
        content = config_path.read_text(encoding="utf-8")
        config = parse_toml_simple(content)
        
        # Extract file lists
        result = {}
        if "header_files" in config:
            result["header_files"] = config["header_files"]
        if "problem_files" in config:
            result["problem_files"] = config["problem_files"]
        if "footer_files" in config:
            result["footer_files"] = config["footer_files"]
        if "output" in config:
            result["output"] = config["output"]
        
        return result
    except Exception as e:
        print(f"Warning: Failed to parse {config_path}: {e}")
        return {}


def collect_source_files(source_dir: Path) -> tuple[list[Path], list[Path], list[Path]]:
    """
    Collect and categorize source files.
    
    If _config.toml exists, uses the order specified there.
    Otherwise, falls back to default ordering.
    
    Returns:
        (header_files, problem_files, footer_files)
    """
    if not source_dir.exists():
        return [], [], []

    # Load configuration
    config = load_config(source_dir)
    
    # Collect all markdown files
    all_files = {f.name: f for f in source_dir.glob("*.md") if f.name != "_config.toml"}
    
    header_files, footer_files, problem_files = [], [], []

    # Get default file order from config
    default_header_order, default_footer_order = get_default_file_order()
    
    # Categorize files
    for name, file_path in all_files.items():
        if name in default_header_order or name.startswith("_header"):
            header_files.append(file_path)
        elif name in default_footer_order or (name.startswith("_") and name != "_config.toml"):
            footer_files.append(file_path)
        else:
            problem_files.append(file_path)

    # Sort using config if available, otherwise use defaults
    def sort_by_config(files: list[Path], config_key: str, default_order: list[str]) -> list[Path]:
        """Sort files according to config order, or default order."""
        if config_key in config:
            # Use config order
            config_order = config[config_key]
            file_dict = {f.name: f for f in files}
            ordered = []
            seen = set()
            
            # Add files in config order
            for filename in config_order:
                if filename in file_dict:
                    ordered.append(file_dict[filename])
                    seen.add(filename)
            
            # Add any remaining files not in config (shouldn't happen, but be safe)
            for f in files:
                if f.name not in seen:
                    ordered.append(f)
            
            return ordered
        else:
            # Use default order
            return sorted(files, key=lambda f: (
                default_order.index(f.name) if f.name in default_order else 999,
                f.name
            ))
    
    header_files = sort_by_config(header_files, "header_files", default_header_order)
    footer_files = sort_by_config(footer_files, "footer_files", default_footer_order)
    
    # Problem files: use config order if available, otherwise sort by name
    if "problem_files" in config:
        file_dict = {f.name: f for f in problem_files}
        ordered = []
        seen = set()
        
        # Add files in config order
        for filename in config["problem_files"]:
            if filename in file_dict:
                ordered.append(file_dict[filename])
                seen.add(filename)
        
        # Add any remaining files not in config (sorted by name)
        remaining = sorted([f for f in problem_files if f.name not in seen], key=lambda f: f.name)
        problem_files = ordered + remaining
    else:
        problem_files.sort(key=lambda f: f.name)

    return header_files, problem_files, footer_files

