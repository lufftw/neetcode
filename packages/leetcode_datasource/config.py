"""
Configuration for LeetCodeDataSource.

Priority order for data directory:
    1. Explicit: DataSourceConfig(data_dir=Path("/custom"))
    2. Environment: NEETCODE_DATA_DIR
    3. Repo local: .neetcode/ in repo root
    4. Fallback: platformdirs or ~/.neetcode/
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TYPE_CHECKING
import os

if TYPE_CHECKING:
    from .fetchers import BaseFetcher


@dataclass
class DataSourceConfig:
    """Configuration for LeetCodeDataSource."""
    
    # Data directory (where .neetcode/ lives)
    data_dir: Optional[Path] = None
    
    # Cache settings
    cache_enabled: bool = True
    cache_ttl_hours: int = 24 * 7  # 1 week default
    
    # Network settings
    fetch_timeout: int = 30  # seconds
    rate_limit_delay: float = 0.5  # seconds between requests
    
    # Fetcher (pluggable) - None means use default LeetscrapeFecher
    fetcher: Optional["BaseFetcher"] = None
    
    def __post_init__(self):
        if self.data_dir is None:
            self.data_dir = self._resolve_data_dir()
        elif isinstance(self.data_dir, str):
            self.data_dir = Path(self.data_dir)
    
    def _resolve_data_dir(self) -> Path:
        """Resolve data directory with priority order."""
        # Priority 1: Environment variable
        env_dir = os.environ.get("NEETCODE_DATA_DIR")
        if env_dir:
            return Path(env_dir)
        
        # Priority 2: Repo local .neetcode/
        repo_root = self._find_repo_root()
        if repo_root:
            return repo_root / ".neetcode"
        
        # Priority 3: platformdirs (fallback)
        try:
            import platformdirs
            return Path(platformdirs.user_data_dir("neetcode"))
        except ImportError:
            pass
        
        # Priority 4: Home directory fallback
        return Path.home() / ".neetcode"
    
    def _find_repo_root(self) -> Optional[Path]:
        """Find repo root by looking for pyproject.toml."""
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            if (parent / "pyproject.toml").exists():
                return parent
        return None
    
    @property
    def leetcode_datasource_dir(self) -> Path:
        """Get the leetcode_datasource data directory."""
        return self.data_dir / "leetcode_datasource"
    
    @property
    def cache_dir(self) -> Path:
        """Get the cache directory."""
        return self.leetcode_datasource_dir / "cache"
    
    @property
    def store_dir(self) -> Path:
        """Get the store directory."""
        return self.leetcode_datasource_dir / "store"
    

