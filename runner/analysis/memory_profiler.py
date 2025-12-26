# runner/analysis/memory_profiler.py
"""
Memory Profiler - RSS measurement and memory metrics for benchmarking.

Design Principles (from memory-metrics.md):
1. Theory ≠ Measurement: Big-O space complexity is separate from measured RSS
2. Method-level by Default: Aggregate memory at method level
3. Explicit Debugging: Case-level memory via --memory-per-case only
4. Graceful Degradation: Missing measurements reported explicitly

Metrics:
- Aux Space (Big-O): Theoretical auxiliary memory (declared in solution)
- Peak RSS: Maximum resident set size observed (MB/KB)
- P95 RSS: 95th percentile of per-case peak RSS (MB/KB)
"""
import sys
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field

# Try to import psutil for RSS measurement
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# Try to import sparklines for memory trace visualization
try:
    from sparklines import sparklines as _sparklines
    HAS_SPARKLINES = True
except ImportError:
    HAS_SPARKLINES = False


@dataclass
class CaseMemoryMetrics:
    """Memory metrics for a single test case."""
    case_name: str
    peak_rss_bytes: Optional[int] = None  # Peak RSS in bytes (subprocess) or Peak Alloc (tracemalloc)
    input_bytes: int = 0  # Raw input size in bytes
    input_scale: Optional[Dict[str, Any]] = None  # Derived scale metrics (n, m, etc.)
    signature_payload_bytes: Optional[int] = None  # Deep size of input objects
    elapsed_ms: float = 0.0  # Execution time
    measurement_type: str = "rss"  # "rss" (subprocess/psutil) or "alloc" (in-process/tracemalloc)


@dataclass
class MethodMemoryMetrics:
    """Aggregated memory metrics for a method across all test cases."""
    method_name: str
    aux_space: str = "Undeclared"  # Declared Big-O space complexity
    peak_rss_bytes: Optional[int] = None  # max(case_peak_rss)
    p95_rss_bytes: Optional[int] = None  # 95th percentile
    case_metrics: List[CaseMemoryMetrics] = field(default_factory=list)
    
    def add_case(self, metrics: CaseMemoryMetrics) -> None:
        """Add case-level metrics and update aggregates."""
        self.case_metrics.append(metrics)
        self._update_aggregates()
    
    def _update_aggregates(self) -> None:
        """Recalculate Peak RSS and P95 RSS from case metrics."""
        valid_rss = [m.peak_rss_bytes for m in self.case_metrics 
                     if m.peak_rss_bytes is not None]
        
        if not valid_rss:
            self.peak_rss_bytes = None
            self.p95_rss_bytes = None
            return
        
        # Peak RSS = max
        self.peak_rss_bytes = max(valid_rss)
        
        # P95 RSS = 95th percentile
        sorted_rss = sorted(valid_rss)
        p95_idx = int(len(sorted_rss) * 0.95)
        p95_idx = min(p95_idx, len(sorted_rss) - 1)
        self.p95_rss_bytes = sorted_rss[p95_idx]
    
    @property
    def stability_percent(self) -> Optional[float]:
        """Calculate stability metric: (Peak - P95) / P95 * 100."""
        if self.peak_rss_bytes is None or self.p95_rss_bytes is None:
            return None
        if self.p95_rss_bytes == 0:
            return None
        return (self.peak_rss_bytes - self.p95_rss_bytes) / self.p95_rss_bytes * 100
    
    @property
    def stability_classification(self) -> str:
        """Classify stability: stable (<5%), moderate (5-15%), spiky (>15%)."""
        stability = self.stability_percent
        if stability is None:
            return "N/A"
        if stability < 5:
            return "stable"
        elif stability <= 15:
            return "moderate"
        else:
            return "spiky"
    
    def get_top_cases(self, k: int = 5) -> List[CaseMemoryMetrics]:
        """Get top K cases by peak RSS for debugging."""
        sorted_cases = sorted(
            [m for m in self.case_metrics if m.peak_rss_bytes is not None],
            key=lambda m: m.peak_rss_bytes or 0,
            reverse=True
        )
        return sorted_cases[:k]


class MemoryProfiler:
    """
    Measures process RSS during test execution.
    
    Uses psutil for cross-platform RSS measurement.
    Falls back gracefully when psutil is unavailable.
    """
    
    def __init__(self):
        self._process: Optional[Any] = None
        self._baseline_rss: int = 0
        
        if HAS_PSUTIL:
            try:
                self._process = psutil.Process()
                self._baseline_rss = self._get_current_rss()
            except Exception:
                self._process = None
    
    @staticmethod
    def is_available() -> bool:
        """Check if memory profiling is available."""
        return HAS_PSUTIL
    
    def _get_current_rss(self) -> int:
        """Get current RSS in bytes."""
        if self._process is None:
            return 0
        try:
            return self._process.memory_info().rss
        except Exception:
            return 0
    
    def get_peak_rss(self) -> Optional[int]:
        """
        Get peak RSS since profiler creation.
        
        Note: This returns current RSS as an approximation.
        For true peak tracking, we'd need continuous sampling.
        """
        if self._process is None:
            return None
        try:
            return self._get_current_rss()
        except Exception:
            return None
    
    def measure_subprocess_rss(self, pid: int) -> Optional[int]:
        """
        Measure RSS of a subprocess by PID.
        
        Args:
            pid: Process ID to measure
        
        Returns:
            RSS in bytes, or None if unavailable
        """
        if not HAS_PSUTIL:
            return None
        try:
            proc = psutil.Process(pid)
            return proc.memory_info().rss
        except Exception:
            return None


# --- Formatting Utilities ---

def format_bytes(bytes_val: Optional[int]) -> str:
    """
    Format bytes as human-readable string.
    
    Rules (from cli-output-contract.md):
    - ≥ 1 MB -> display in MB (e.g., 25.4MB)
    - ≥ 1 KB -> display in KB (e.g., 512KB)
    - < 1 KB -> display in B (e.g., 256B)
    - Zero -> 0B
    - None -> Unavailable
    """
    if bytes_val is None:
        return "Unavailable"
    if bytes_val == 0:
        return "0B"
    
    mb = bytes_val / (1024 * 1024)
    if mb >= 1.0:
        return f"{mb:.1f}MB"
    
    kb = bytes_val / 1024
    if kb >= 1.0:
        return f"{kb:.0f}KB"
    
    return f"{bytes_val}B"


# --- Memory Trace Visualization ---

def generate_memory_trace(rss_samples: List[int], width: int = 20, 
                          min_width: int = 10) -> str:
    """
    Generate ASCII sparkline for memory trace.
    
    Uses sparklines package if available, falls back to custom implementation.
    
    Args:
        rss_samples: List of RSS values in bytes
        width: Maximum width of sparkline
        min_width: Minimum width (pads with interpolation if fewer samples)
    
    Returns:
        Sparkline string, e.g., "▁▂▅▇█▆▃▂▁"
    """
    if not rss_samples:
        return "N/A"
    
    # Determine target width
    target_width = max(min_width, min(width, len(rss_samples)))
    
    # Resample to target width if needed
    if len(rss_samples) != target_width:
        sampled = _resample_data(rss_samples, target_width)
    else:
        sampled = list(rss_samples)
    
    # Use sparklines package if available
    if HAS_SPARKLINES:
        result = _sparklines(sampled)
        return result[0] if result else "N/A"
    
    # Fallback to custom implementation
    return _generate_sparkline_custom(sampled)


def _resample_data(data: List[int], target_width: int) -> List[float]:
    """Resample data to target width using linear interpolation."""
    if len(data) == 1:
        return [float(data[0])] * target_width
    
    sampled = []
    for i in range(target_width):
        src_idx = i * (len(data) - 1) / (target_width - 1)
        lower_idx = int(src_idx)
        upper_idx = min(lower_idx + 1, len(data) - 1)
        frac = src_idx - lower_idx
        val = data[lower_idx] * (1 - frac) + data[upper_idx] * frac
        sampled.append(val)
    return sampled


def _generate_sparkline_custom(data: List[float]) -> str:
    """Custom sparkline generation (fallback when sparklines package unavailable)."""
    blocks = '▁▂▃▄▅▆▇█'
    
    min_val = min(data)
    max_val = max(data)
    
    result = []
    for val in data:
        if max_val == min_val:
            idx = 4  # Middle block for uniform data
        else:
            idx = int((val - min_val) / (max_val - min_val) * 7)
            idx = max(0, min(7, idx))
        result.append(blocks[idx])
    
    return ''.join(result)


__all__ = [
    'HAS_PSUTIL',
    'HAS_SPARKLINES',
    'CaseMemoryMetrics',
    'MethodMemoryMetrics',
    'MemoryProfiler',
    'format_bytes',
    'generate_memory_trace',
]

