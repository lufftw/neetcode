# runner/complexity_estimator.py
"""
Complexity Estimator - Estimate time complexity using big_O methodology.

Design Philosophy:
- Complexity estimation requires controlled input sizes (big_O approach)
- Random test generation (for functional testing) is separate
- Uses Mock stdin to call solve() directly (no subprocess overhead, fully generic)

Feature Levels:
- Level 0: generate()                    - Random test generation (required)
- Level 1: + generate_for_complexity(n)  - Enable complexity estimation

Usage:
    from runner.complexity_estimator import ComplexityEstimator
    
    if ComplexityEstimator.can_estimate(generator_module):
        estimator = ComplexityEstimator(generator_module, problem, solution_module)
        result = estimator.estimate()
        print(f"Estimated: {result.complexity}")
"""
import os
import sys
import io
import time
from typing import Optional, List, Any
from dataclasses import dataclass

# Try to import big_O package
try:
    import big_o
    from big_o import complexities
    HAS_BIG_O = True
except ImportError:
    HAS_BIG_O = False


@dataclass
class ComplexityResult:
    """Result of complexity estimation."""
    complexity: str  # e.g., "O(n)", "O(n log n)"
    confidence: float  # R² or residual-based confidence (0.0 - 1.0)
    samples: int  # Number of samples used
    details: str = ""  # Additional details (e.g., fitted equation)
    
    def __str__(self) -> str:
        return self.complexity


class ComplexityEstimator:
    """
    Estimates time complexity using controlled input sizes.
    
    Uses Mock stdin approach:
    - Generic - works with any solution that has solve() function
    - No subprocess overhead
    - Maintains stdin abstraction design
    """
    
    # Default sizes for estimation
    DEFAULT_SIZES = [10, 20, 50, 100, 200, 500, 1000, 2000]
    
    # Number of times to run each size (for averaging)
    RUNS_PER_SIZE = 3
    
    def __init__(self, generator_module: Any, problem: str, 
                 solution_module: Any = None,
                 method: Optional[str] = None, 
                 sizes: Optional[List[int]] = None):
        """
        Initialize the estimator.
        
        Args:
            generator_module: Loaded generator module
            problem: Problem name (e.g., "0004_median_of_two_sorted_arrays")
            solution_module: Loaded solution module
            method: Solution method name (optional)
            sizes: Custom sizes to test (optional)
        """
        self.generator_module = generator_module
        self.problem = problem
        self.solution_module = solution_module
        self.method = method
        self.sizes = sizes or self.DEFAULT_SIZES
        
        # Get generator function
        self.gen_func = getattr(generator_module, 'generate_for_complexity', None)
        
    @staticmethod
    def is_available() -> bool:
        """Check if complexity estimation is available (big_O installed)."""
        return HAS_BIG_O
    
    @staticmethod
    def can_estimate(generator_module: Any) -> bool:
        """Check if generator supports complexity estimation."""
        return (
            HAS_BIG_O and 
            generator_module is not None and
            hasattr(generator_module, 'generate_for_complexity')
        )
    
    @staticmethod
    def get_unavailable_reason(generator_module: Any) -> str:
        """Get reason why estimation is not available."""
        if not HAS_BIG_O:
            return "big-O package not installed (pip install big-O)"
        if generator_module is None:
            return "Generator module not found"
        if not hasattr(generator_module, 'generate_for_complexity'):
            return "Generator does not provide generate_for_complexity(n) function"
        return "Unknown reason"
    
    def estimate(self) -> Optional[ComplexityResult]:
        """
        Run complexity estimation using Mock stdin approach.
        
        Returns:
            ComplexityResult or None if estimation fails
        """
        if not self.can_estimate(self.generator_module):
            return None
        
        # Check if solution module has solve() function
        if self.solution_module and hasattr(self.solution_module, 'solve'):
            return self._estimate_mock_stdin()
        else:
            print(f"      ⚠️ Solution module missing solve() function")
            return None
    
    def _estimate_mock_stdin(self) -> Optional[ComplexityResult]:
        """
        Estimate using Mock stdin approach.
        
        - Generic: works with any solution that has solve()
        - No subprocess overhead
        - Maintains stdin abstraction
        """
        print(f"\n   📈 Running complexity estimation...")
        print(f"      Mode: Direct call (Mock stdin, no subprocess overhead)")
        print(f"      Sizes: {self.sizes}")
        print(f"      Runs per size: {self.RUNS_PER_SIZE}")
        
        solve_func = self.solution_module.solve
        
        sizes = []
        times = []
        
        for size in self.sizes:
            try:
                # Generate input for this size
                input_data = self.gen_func(size)
                
                # Run multiple times and average
                run_times = []
                for _ in range(self.RUNS_PER_SIZE):
                    elapsed_ms = self._run_with_mock_stdin(solve_func, input_data)
                    if elapsed_ms is not None:
                        run_times.append(elapsed_ms)
                
                if run_times:
                    avg_time = sum(run_times) / len(run_times)
                    sizes.append(size)
                    times.append(avg_time)
                    print(f"      n={size:>5}: {avg_time:.4f}ms (avg of {len(run_times)} runs)")
                
            except Exception as e:
                print(f"      ⚠️ Failed at size {size}: {e}")
                continue
        
        if len(sizes) < 3:
            print(f"      ❌ Not enough data points ({len(sizes)}/3 minimum)")
            return None
        
        return self._fit_complexity(sizes, times)
    
    def _run_with_mock_stdin(self, solve_func, input_data: str) -> Optional[float]:
        """
        Run solve() with mocked stdin and capture execution time.
        
        Args:
            solve_func: The solve() function to call
            input_data: Input string to feed via stdin
        
        Returns:
            Execution time in milliseconds, or None on error
        """
        original_stdin = sys.stdin
        original_stdout = sys.stdout
        
        try:
            # Mock stdin with input data
            sys.stdin = io.StringIO(input_data)
            # Capture stdout to avoid output interference
            sys.stdout = io.StringIO()
            
            # Measure execution time
            start_time = time.perf_counter()
            solve_func()
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            
            return elapsed_ms
            
        except Exception:
            return None
        finally:
            # Restore original stdin/stdout
            sys.stdin = original_stdin
            sys.stdout = original_stdout
    
    def _fit_complexity(self, sizes: List[int], times: List[float]) -> Optional[ComplexityResult]:
        """Use big_O to fit complexity class."""
        try:
            import numpy as np
            
            ns = np.array(sizes)
            ts = np.array(times)
            
            # Define complexity classes to test
            classes = [
                complexities.Constant,
                complexities.Logarithmic,
                complexities.Linear,
                complexities.Linearithmic,
                complexities.Quadratic,
                complexities.Cubic,
            ]
            
            # Only test exponential for small max size
            if max(sizes) <= 30:
                classes.append(complexities.Exponential)
            
            # Fit using big_O
            best, fitted = big_o.infer_big_o_class(ns, ts, classes=classes)
            
            # Map class name to O notation
            complexity_map = {
                'Constant': 'O(1)',
                'Logarithmic': 'O(log n)',
                'Linear': 'O(n)',
                'Linearithmic': 'O(n log n)',
                'Quadratic': 'O(n²)',
                'Cubic': 'O(n³)',
                'Exponential': 'O(2^n)',
            }
            
            class_name = best.__class__.__name__
            complexity_str = complexity_map.get(class_name, str(best))
            
            # Calculate confidence from residual
            residual = getattr(best, 'residual', 0)
            mean_time = sum(times) / len(times)
            if mean_time > 0:
                confidence = max(0.0, min(1.0, 1.0 - (residual / mean_time) * 0.1))
            else:
                confidence = 0.5
            
            return ComplexityResult(
                complexity=complexity_str,
                confidence=confidence,
                samples=len(sizes),
                details=str(best)
            )
            
        except Exception as e:
            print(f"      ❌ Fitting failed: {e}")
            return None


def format_complexity_result(result: Optional[ComplexityResult], 
                            user_complexity: str = "Unknown") -> str:
    """
    Format complexity for display.
    
    Args:
        result: ComplexityResult from estimation (or None)
        user_complexity: User-defined complexity from SOLUTIONS metadata
    
    Returns:
        Formatted string
    """
    user = user_complexity.strip() if user_complexity else ""
    has_user = user and user.lower() not in ["unknown", "o(?)", "?", ""]
    
    if result:
        estimated = result.complexity
        if has_user:
            user_norm = user.lower().replace(" ", "")
            est_norm = estimated.lower().replace(" ", "").replace("²", "2").replace("³", "3")
            if user_norm == est_norm:
                return user  # Match
            return f"{user} (估算: {estimated})"
        else:
            return f"{estimated} (估算)"
    else:
        return user if has_user else "Unknown"
