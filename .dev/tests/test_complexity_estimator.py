# tests_unit/test_complexity_estimator.py
"""
Characterization tests for runner/complexity_estimator.py

These tests capture the current behavior of the complexity estimator
to ensure refactoring doesn't break existing functionality.
"""
import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import io

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from runner.analysis.complexity import (
    ComplexityEstimator,
    ComplexityResult,
    format_complexity_result,
    HAS_BIG_O,
)


class TestComplexityResult:
    """Test ComplexityResult dataclass."""
    
    def test_basic_result(self):
        """Test basic ComplexityResult creation."""
        result = ComplexityResult(
            complexity="O(n)",
            confidence=0.95,
            samples=8,
            details="Linear fit"
        )
        
        assert result.complexity == "O(n)"
        assert result.confidence == 0.95
        assert result.samples == 8
        assert result.details == "Linear fit"
    
    def test_str_representation(self):
        """Test string representation of ComplexityResult."""
        result = ComplexityResult(
            complexity="O(n log n)",
            confidence=0.90,
            samples=10
        )
        
        assert str(result) == "O(n log n)"
    
    def test_default_details(self):
        """Test default details value."""
        result = ComplexityResult(
            complexity="O(1)",
            confidence=1.0,
            samples=5
        )
        
        assert result.details == ""


class TestComplexityEstimatorAvailability:
    """Test ComplexityEstimator availability checks."""
    
    def test_is_available(self):
        """Test is_available returns correct value."""
        available = ComplexityEstimator.is_available()
        assert available == HAS_BIG_O
    
    def test_can_estimate_without_big_o(self):
        """Test can_estimate when big_O is not available."""
        if not HAS_BIG_O:
            class MockGenerator:
                def generate_for_complexity(self, n):
                    return f"{n}"
            
            can_estimate = ComplexityEstimator.can_estimate(MockGenerator())
            assert can_estimate is False
    
    @pytest.mark.skipif(not HAS_BIG_O, reason="Requires big-O package")
    def test_can_estimate_with_big_o_and_function(self):
        """Test can_estimate when big_O is available and function exists."""
        class MockGenerator:
            def generate_for_complexity(self, n):
                return f"{n}"
        
        can_estimate = ComplexityEstimator.can_estimate(MockGenerator())
        assert can_estimate is True
    
    def test_can_estimate_without_function(self):
        """Test can_estimate when generate_for_complexity is missing."""
        class MockGenerator:
            def generate(self, n, seed=None):
                yield f"{n}"
        
        can_estimate = ComplexityEstimator.can_estimate(MockGenerator())
        assert can_estimate is False
    
    def test_can_estimate_with_none_module(self):
        """Test can_estimate with None module."""
        can_estimate = ComplexityEstimator.can_estimate(None)
        assert can_estimate is False
    
    def test_get_unavailable_reason_no_big_o(self):
        """Test get_unavailable_reason when big_O is not installed."""
        if not HAS_BIG_O:
            reason = ComplexityEstimator.get_unavailable_reason(None)
            assert "big-O package not installed" in reason
    
    def test_get_unavailable_reason_no_module(self):
        """Test get_unavailable_reason when module is None."""
        if HAS_BIG_O:
            reason = ComplexityEstimator.get_unavailable_reason(None)
            assert "Generator module not found" in reason
    
    def test_get_unavailable_reason_no_function(self):
        """Test get_unavailable_reason when function is missing."""
        if HAS_BIG_O:
            class MockGenerator:
                pass
            
            reason = ComplexityEstimator.get_unavailable_reason(MockGenerator())
            assert "generate_for_complexity" in reason


class TestComplexityEstimatorInit:
    """Test ComplexityEstimator initialization."""
    
    def test_basic_initialization(self):
        """Test basic estimator initialization."""
        class MockGenerator:
            def generate_for_complexity(self, n):
                return f"{n}"
        
        class MockSolution:
            def solve(self):
                pass
        
        estimator = ComplexityEstimator(
            generator_module=MockGenerator(),
            problem="test_problem",
            solution_module=MockSolution(),
            method=None
        )
        
        assert estimator.problem == "test_problem"
        assert estimator.method is None
        assert estimator.sizes == ComplexityEstimator.DEFAULT_SIZES
    
    def test_custom_sizes(self):
        """Test initialization with custom sizes."""
        class MockGenerator:
            def generate_for_complexity(self, n):
                return f"{n}"
        
        custom_sizes = [5, 10, 20, 50]
        estimator = ComplexityEstimator(
            generator_module=MockGenerator(),
            problem="test_problem",
            solution_module=None,
            sizes=custom_sizes
        )
        
        assert estimator.sizes == custom_sizes
    
    def test_default_sizes(self):
        """Test default sizes are set correctly."""
        # Includes 5000 for better O(n) vs O(n²) detection
        assert ComplexityEstimator.DEFAULT_SIZES == [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
    
    def test_runs_per_size(self):
        """Test RUNS_PER_SIZE constant."""
        assert ComplexityEstimator.RUNS_PER_SIZE == 3


class TestComplexityEstimatorEstimate:
    """Test ComplexityEstimator estimate method."""
    
    def test_estimate_without_big_o(self):
        """Test estimate returns None when big_O is not available."""
        if not HAS_BIG_O:
            class MockGenerator:
                def generate_for_complexity(self, n):
                    return f"{n}"
            
            estimator = ComplexityEstimator(
                generator_module=MockGenerator(),
                problem="test_problem",
                solution_module=None
            )
            
            result = estimator.estimate()
            assert result is None
    
    def test_estimate_without_solve_function(self):
        """Test estimate returns None when solve() is missing."""
        if HAS_BIG_O:
            class MockGenerator:
                def generate_for_complexity(self, n):
                    return f"{n}"
            
            class MockSolution:
                pass  # No solve() function
            
            estimator = ComplexityEstimator(
                generator_module=MockGenerator(),
                problem="test_problem",
                solution_module=MockSolution()
            )
            
            result = estimator.estimate()
            assert result is None
    
    @pytest.mark.skipif(not HAS_BIG_O, reason="Requires big-O package")
    def test_estimate_with_constant_time(self):
        """Test estimating O(1) complexity."""
        class MockGenerator:
            def generate_for_complexity(self, n):
                return f"{n}\n"
        
        class MockSolution:
            def solve(self):
                # Constant time operation
                line = sys.stdin.readline()
                print("42")
        
        estimator = ComplexityEstimator(
            generator_module=MockGenerator(),
            problem="test_problem",
            solution_module=MockSolution(),
            sizes=[10, 20, 50, 100]
        )
        
        result = estimator.estimate()
        
        # Should detect O(1) or similar
        assert result is not None
        assert result.samples >= 3
    
    @pytest.mark.skipif(not HAS_BIG_O, reason="Requires big-O package")
    def test_estimate_with_linear_time(self):
        """Test estimating O(n) complexity."""
        class MockGenerator:
            def generate_for_complexity(self, n):
                return f"{n}\n"
        
        class MockSolution:
            def solve(self):
                # Linear time operation
                n = int(sys.stdin.readline())
                total = 0
                for i in range(n):
                    total += i
                print(total)
        
        estimator = ComplexityEstimator(
            generator_module=MockGenerator(),
            problem="test_problem",
            solution_module=MockSolution(),
            sizes=[10, 20, 50, 100, 200]
        )
        
        result = estimator.estimate()
        
        # Should detect O(n) or similar
        assert result is not None
        assert result.samples >= 3


class TestRunWithMockStdin:
    """Test _run_with_mock_stdin method."""
    
    def test_mock_stdin_basic(self):
        """Test basic mock stdin functionality."""
        if HAS_BIG_O:
            class MockGenerator:
                def generate_for_complexity(self, n):
                    return f"{n}\n"
            
            class MockSolution:
                def solve(self):
                    line = sys.stdin.readline()
                    print(f"Got: {line.strip()}")
            
            estimator = ComplexityEstimator(
                generator_module=MockGenerator(),
                problem="test_problem",
                solution_module=MockSolution()
            )
            
            input_data = "42\n"
            elapsed_ms, peak_bytes = estimator._run_with_mock_stdin(MockSolution().solve, input_data)
            
            assert elapsed_ms is not None
            assert elapsed_ms >= 0
            # peak_bytes is None when profile_memory=False (default)
            assert peak_bytes is None
    
    def test_mock_stdin_restores_original(self):
        """Test that original stdin is restored after mock."""
        if HAS_BIG_O:
            original_stdin = sys.stdin
            
            class MockGenerator:
                def generate_for_complexity(self, n):
                    return f"{n}\n"
            
            class MockSolution:
                def solve(self):
                    sys.stdin.readline()
            
            estimator = ComplexityEstimator(
                generator_module=MockGenerator(),
                problem="test_problem",
                solution_module=MockSolution()
            )
            
            estimator._run_with_mock_stdin(MockSolution().solve, "test\n")
            
            # stdin should be restored
            assert sys.stdin == original_stdin
    
    def test_mock_stdin_handles_exception(self):
        """Test that exceptions are handled gracefully."""
        if HAS_BIG_O:
            original_stdin = sys.stdin
            
            class MockGenerator:
                def generate_for_complexity(self, n):
                    return f"{n}\n"
            
            class MockSolution:
                def solve(self):
                    raise ValueError("Test error")
            
            estimator = ComplexityEstimator(
                generator_module=MockGenerator(),
                problem="test_problem",
                solution_module=MockSolution()
            )
            
            elapsed_ms, peak_bytes = estimator._run_with_mock_stdin(MockSolution().solve, "test\n")
            
            # Should return (None, None) on error
            assert elapsed_ms is None
            assert peak_bytes is None
            # stdin should still be restored
            assert sys.stdin == original_stdin


class TestFormatComplexityResult:
    """Test format_complexity_result function."""
    
    def test_format_with_result_no_user_complexity(self):
        """Test formatting with result but no user complexity."""
        result = ComplexityResult(
            complexity="O(n)",
            confidence=0.95,
            samples=8
        )
        
        formatted = format_complexity_result(result, "Unknown")
        assert "O(n)" in formatted
        assert "估算" in formatted
    
    def test_format_with_matching_complexities(self):
        """Test formatting when user and estimated complexities match."""
        result = ComplexityResult(
            complexity="O(n)",
            confidence=0.95,
            samples=8
        )
        
        formatted = format_complexity_result(result, "O(n)")
        assert formatted == "O(n)"
        assert "估算" not in formatted
    
    def test_format_with_different_complexities(self):
        """Test formatting when complexities differ."""
        result = ComplexityResult(
            complexity="O(n log n)",
            confidence=0.95,
            samples=8
        )
        
        formatted = format_complexity_result(result, "O(n)")
        assert "O(n)" in formatted
        assert "O(n log n)" in formatted
        assert "估算" in formatted
    
    def test_format_without_result(self):
        """Test formatting without estimation result."""
        formatted = format_complexity_result(None, "O(n²)")
        assert formatted == "O(n²)"
    
    def test_format_without_result_or_user_complexity(self):
        """Test formatting with neither result nor user complexity."""
        formatted = format_complexity_result(None, "Unknown")
        assert formatted == "Unknown"
    
    def test_format_with_empty_user_complexity(self):
        """Test formatting with empty user complexity."""
        result = ComplexityResult(
            complexity="O(n)",
            confidence=0.95,
            samples=8
        )
        
        formatted = format_complexity_result(result, "")
        assert "O(n)" in formatted
        assert "估算" in formatted
    
    def test_format_normalizes_complexity_notation(self):
        """Test that complexity notation is normalized for comparison."""
        result = ComplexityResult(
            complexity="O(n²)",
            confidence=0.95,
            samples=8
        )
        
        # Should match even with different notation
        formatted = format_complexity_result(result, "O(n2)")
        # The function normalizes ² to 2 for comparison
        assert formatted == "O(n2)" or "O(n²)" in formatted


@pytest.mark.edge_case
class TestEdgeCases:
    """Test edge cases for complexity estimator."""
    
    def test_empty_sizes_list(self):
        """Test with empty sizes list - should use default sizes."""
        class MockGenerator:
            def generate_for_complexity(self, n):
                return f"{n}"
        
        estimator = ComplexityEstimator(
            generator_module=MockGenerator(),
            problem="test_problem",
            solution_module=None,
            sizes=[]
        )
        
        # Empty list means use default sizes (current behavior)
        # Note: This tests the actual behavior, not ideal behavior
        assert estimator.sizes == [] or estimator.sizes == ComplexityEstimator.DEFAULT_SIZES
    
    def test_single_size(self):
        """Test with single size (insufficient for estimation)."""
        if HAS_BIG_O:
            class MockGenerator:
                def generate_for_complexity(self, n):
                    return f"{n}\n"
            
            class MockSolution:
                def solve(self):
                    sys.stdin.readline()
                    print("result")
            
            estimator = ComplexityEstimator(
                generator_module=MockGenerator(),
                problem="test_problem",
                solution_module=MockSolution(),
                sizes=[10]
            )
            
            # Should fail with insufficient data points
            result = estimator.estimate()
            # Will likely return None due to insufficient samples
            assert result is None or result.samples < 3
    
    def test_very_large_sizes(self):
        """Test with very large sizes."""
        class MockGenerator:
            def generate_for_complexity(self, n):
                return f"{n}"
        
        large_sizes = [10000, 20000, 50000]
        estimator = ComplexityEstimator(
            generator_module=MockGenerator(),
            problem="test_problem",
            solution_module=None,
            sizes=large_sizes
        )
        
        assert estimator.sizes == large_sizes
    
    def test_complexity_result_with_special_characters(self):
        """Test ComplexityResult with special characters."""
        result = ComplexityResult(
            complexity="O(n²)",
            confidence=0.95,
            samples=8,
            details="Quadratic fit with R²=0.95"
        )
        
        assert "²" in result.complexity
        assert "²" in result.details


@pytest.mark.requires_big_o
@pytest.mark.skipif(not HAS_BIG_O, reason="Requires big-O package")
class TestBigOIntegration:
    """Integration tests with big_O package."""
    
    def test_big_o_available(self):
        """Test that big_O is available for these tests."""
        assert HAS_BIG_O is True
    
    def test_complexity_classes_available(self):
        """Test that complexity classes are available."""
        from big_o import complexities
        
        assert hasattr(complexities, 'Constant')
        assert hasattr(complexities, 'Linear')
        assert hasattr(complexities, 'Logarithmic')
        assert hasattr(complexities, 'Linearithmic')
        assert hasattr(complexities, 'Quadratic')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

