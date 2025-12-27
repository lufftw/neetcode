# =============================================================================
# Data Sources Loader
# =============================================================================
# Loads data from configured sources: ontology, problems, patterns, roadmaps.
# Sources are defined in config/config.yaml under data_sources section.
# =============================================================================

from __future__ import annotations

import glob
from pathlib import Path
from typing import Any

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Fallback for Python < 3.11

from .config_loader import ConfigLoader


class DataSourcesLoader:
    """
    Loads data from configured sources based on config.yaml settings.
    
    Supports:
    - Ontology TOML files (algorithms, patterns, etc.)
    - Problem metadata TOML files
    - Pattern documentation directories
    - Roadmap learning paths
    """
    
    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize the data sources loader.
        
        Args:
            config: Configuration dict. If None, loads from ConfigLoader.
        """
        self.config = config or ConfigLoader.get_config()
        self.data_sources_config = self.config.get("data_sources", {})
        
        # Resolve base paths relative to the config file location
        config_dir = Path(__file__).parent.parent / "config"
        self.base_paths = {}
        
        for key, rel_path in self.data_sources_config.get("base_paths", {}).items():
            self.base_paths[key] = (config_dir / rel_path).resolve()
        
        # Loaded data storage
        self._ontology: dict[str, Any] = {}
        self._problems: dict[str, Any] = {}
        self._patterns: dict[str, Any] = {}
        self._roadmaps: dict[str, Any] = {}
    
    def load_all(self) -> dict[str, Any]:
        """
        Load all enabled data sources.
        
        Returns:
            Dictionary with all loaded data organized by source type
        """
        result = {
            "ontology": self.load_ontology(),
            "problems": self.load_problems(),
            "patterns": self.load_patterns(),
            "roadmaps": self.load_roadmaps(),
        }
        return result
    
    def load_ontology(self) -> dict[str, Any]:
        """
        Load ontology files (algorithms, patterns, etc.).
        
        Returns:
            Dictionary mapping ontology name to parsed TOML content
        """
        config = self.data_sources_config.get("ontology", {})
        
        if not config.get("enabled", False):
            return {}
        
        base_path = self.base_paths.get("ontology")
        if not base_path or not base_path.exists():
            print(f"Warning: Ontology base path not found: {base_path}")
            return {}
        
        self._ontology = {}
        
        for file_config in config.get("files", []):
            if not file_config.get("enabled", True):
                continue
            
            name = file_config.get("name")
            file_path = base_path / file_config.get("path", "")
            
            if file_path.exists():
                self._ontology[name] = self._load_toml(file_path)
                print(f"  ✓ Loaded ontology: {name}")
            else:
                print(f"  ⚠ Ontology file not found: {file_path}")
        
        return self._ontology
    
    def load_problems(self) -> dict[str, Any]:
        """
        Load problem metadata files.
        
        Returns:
            Dictionary mapping problem slug to parsed TOML content
        """
        config = self.data_sources_config.get("problems", {})
        
        if not config.get("enabled", False):
            return {}
        
        base_path = self.base_paths.get("problems")
        if not base_path or not base_path.exists():
            print(f"Warning: Problems base path not found: {base_path}")
            return {}
        
        self._problems = {}
        load_mode = config.get("load_mode", "all")
        exclude_patterns = config.get("exclude", [])
        
        if load_mode == "list":
            # Load specific files
            for file_name in config.get("files", []):
                file_path = base_path / file_name
                if file_path.exists():
                    slug = file_path.stem
                    self._problems[slug] = self._load_toml(file_path)
        
        elif load_mode == "pattern":
            # Load files matching glob patterns
            patterns = config.get("patterns", ["*.toml"])
            for pattern in patterns:
                for file_path in base_path.glob(pattern):
                    # Check exclusions
                    if any(file_path.name == exc for exc in exclude_patterns):
                        continue
                    slug = file_path.stem
                    self._problems[slug] = self._load_toml(file_path)
        
        else:  # load_mode == "all"
            for file_path in base_path.glob("*.toml"):
                if any(file_path.name == exc for exc in exclude_patterns):
                    continue
                slug = file_path.stem
                self._problems[slug] = self._load_toml(file_path)
        
        print(f"  ✓ Loaded {len(self._problems)} problem files")
        return self._problems
    
    def load_patterns(self) -> dict[str, Any]:
        """
        Load pattern documentation directories.
        
        Returns:
            Dictionary mapping pattern name to its documentation files
        """
        config = self.data_sources_config.get("patterns", {})
        
        if not config.get("enabled", False):
            return {}
        
        base_path = self.base_paths.get("patterns")
        if not base_path or not base_path.exists():
            print(f"Warning: Patterns base path not found: {base_path}")
            return {}
        
        self._patterns = {}
        
        for dir_config in config.get("directories", []):
            if not dir_config.get("enabled", True):
                continue
            
            name = dir_config.get("name")
            dir_path = base_path / dir_config.get("path", "")
            config_file = dir_config.get("config_file", "_config.toml")
            
            if not dir_path.exists():
                print(f"  ⚠ Pattern directory not found: {dir_path}")
                continue
            
            pattern_data = {
                "name": name,
                "path": str(dir_path),
                "files": {},
                "config": None,
            }
            
            # Load the pattern config file
            config_path = dir_path / config_file
            if config_path.exists():
                pattern_data["config"] = self._load_toml(config_path)
            
            # Load all markdown files
            for md_file in dir_path.glob("*.md"):
                pattern_data["files"][md_file.stem] = md_file.read_text(encoding="utf-8")
            
            self._patterns[name] = pattern_data
            print(f"  ✓ Loaded pattern: {name} ({len(pattern_data['files'])} files)")
        
        return self._patterns
    
    def load_roadmaps(self) -> dict[str, Any]:
        """
        Load roadmap learning paths.
        
        Returns:
            Dictionary mapping roadmap name to parsed TOML content
        """
        config = self.data_sources_config.get("roadmaps", {})
        
        if not config.get("enabled", False):
            return {}
        
        base_path = self.base_paths.get("roadmaps")
        if not base_path or not base_path.exists():
            print(f"Warning: Roadmaps base path not found: {base_path}")
            return {}
        
        self._roadmaps = {}
        
        for file_config in config.get("files", []):
            if not file_config.get("enabled", True):
                continue
            
            name = file_config.get("name")
            file_path = base_path / file_config.get("path", "")
            
            if file_path.exists():
                self._roadmaps[name] = self._load_toml(file_path)
                print(f"  ✓ Loaded roadmap: {name}")
            else:
                print(f"  ⚠ Roadmap file not found: {file_path}")
        
        return self._roadmaps
    
    def _load_toml(self, file_path: Path) -> dict[str, Any]:
        """
        Load and parse a TOML file.
        
        Args:
            file_path: Path to the TOML file
            
        Returns:
            Parsed TOML content as dictionary
        """
        with open(file_path, "rb") as f:
            return tomllib.load(f)
    
    @property
    def ontology(self) -> dict[str, Any]:
        """Get loaded ontology data."""
        return self._ontology
    
    @property
    def problems(self) -> dict[str, Any]:
        """Get loaded problem data."""
        return self._problems
    
    @property
    def patterns(self) -> dict[str, Any]:
        """Get loaded pattern documentation."""
        return self._patterns
    
    @property
    def roadmaps(self) -> dict[str, Any]:
        """Get loaded roadmap data."""
        return self._roadmaps
    
    def get_summary(self) -> dict[str, Any]:
        """
        Get a summary of loaded data sources.
        
        Returns:
            Dictionary with counts and status of each data source
        """
        return {
            "ontology": {
                "enabled": self.data_sources_config.get("ontology", {}).get("enabled", False),
                "loaded_count": len(self._ontology),
                "items": list(self._ontology.keys()),
            },
            "problems": {
                "enabled": self.data_sources_config.get("problems", {}).get("enabled", False),
                "loaded_count": len(self._problems),
            },
            "patterns": {
                "enabled": self.data_sources_config.get("patterns", {}).get("enabled", False),
                "loaded_count": len(self._patterns),
                "items": list(self._patterns.keys()),
            },
            "roadmaps": {
                "enabled": self.data_sources_config.get("roadmaps", {}).get("enabled", False),
                "loaded_count": len(self._roadmaps),
                "items": list(self._roadmaps.keys()),
            },
        }


def load_data_sources(config: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Convenience function to load all configured data sources.
    
    Args:
        config: Optional configuration dict
        
    Returns:
        Dictionary with all loaded data
    """
    loader = DataSourcesLoader(config)
    return loader.load_all()

