# .dev/tests/test_all_solutions.py
"""
Comprehensive test suite for all solutions.

Tests all solution files with:
- Static test cases (from tests/ directory)
- Generated test cases (if generator and JUDGE_FUNC available)
- Combined static + generated tests

Handles cases where:
- No static tests available
- No generator available
- No JUDGE_FUNC (generated tests skipped)
"""
import pytest
import os
import glob
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Ensure solutions directory is in path for _runner imports
SOLUTIONS_DIR = PROJECT_ROOT / "solutions"
if str(SOLUTIONS_DIR) not in sys.path:
    sys.path.insert(0, str(SOLUTIONS_DIR))

from runner import (
    load_solution_module,
    load_generator_module,
    run_one_case,
    run_generated_case,
    run_method_tests,
)


def get_all_solution_files() -> List[str]:
    """Get all solution file names (without .py extension)."""
    solutions_dir = PROJECT_ROOT / "solutions"
    if not solutions_dir.exists():
        return []
    
    solution_files = []
    for file_path in solutions_dir.glob("*.py"):
        # Skip _runner.py and __init__.py
        if file_path.name.startswith("_") or file_path.name == "__init__.py":
            continue
        # Extract problem name (e.g., "0023_merge_k_sorted_lists")
        problem_name = file_path.stem
        solution_files.append(problem_name)
    
    return sorted(solution_files)


def get_static_test_files(problem: str, tests_dir: str = "tests") -> List[str]:
    """Get all static test input files for a problem."""
    pattern = os.path.join(tests_dir, f"{problem}_*.in")
    all_files = sorted(glob.glob(pattern))
    # Exclude failed cases
    return [f for f in all_files if "_failed_" not in f]


def has_generator(problem: str) -> bool:
    """Check if generator exists for problem."""
    generator_path = os.path.join("generators", f"{problem}.py")
    return os.path.exists(generator_path)


def has_judge_func(module) -> bool:
    """Check if solution module has JUDGE_FUNC."""
    return hasattr(module, 'JUDGE_FUNC') if module else False


class TestAllSolutions:
    """Test suite for all solutions."""
    
    @pytest.fixture(scope="class")
    def all_problems(self):
        """Get list of all solution problems."""
        return get_all_solution_files()
    
    @pytest.mark.parametrize("problem", get_all_solution_files())
    def test_static_tests(self, problem):
        """Test all solutions with static test cases."""
        # Load solution module
        module, solutions_meta, compare_mode = load_solution_module(problem)
        
        if not module:
            pytest.skip(f"Could not load solution module: {problem}")
        
        # Get static test files
        input_files = get_static_test_files(problem)
        
        if not input_files:
            pytest.skip(f"No static test files found for {problem}")
        
        # Determine which methods to test
        if solutions_meta and "default" in solutions_meta:
            methods_to_test = ["default"]
        else:
            methods_to_test = [None]
        
        # Run tests for each method
        for method in methods_to_test:
            if method is None:
                # Legacy mode
                passed = 0
                total = 0
                skipped = 0
                
                for in_path in input_files:
                    out_path = in_path.replace(".in", ".out")
                    case_name = os.path.basename(in_path).replace(".in", "")
                    
                    ok, elapsed_ms, actual, expected, validation_mode = run_one_case(
                        problem, in_path, out_path, None, False, compare_mode, module
                    )
                    
                    if validation_mode == "skip":
                        skipped += 1
                        continue
                    
                    total += 1
                    if ok:
                        passed += 1
                    else:
                        pytest.fail(
                            f"{problem} (legacy): {case_name} failed\n"
                            f"Expected: {expected[:100] if expected else 'None'}...\n"
                            f"Actual: {actual[:100]}..."
                        )
                
                if total > 0:
                    assert passed == total, f"{problem}: {passed}/{total} static tests passed"
            else:
                # Multi-solution mode
                method_info = solutions_meta.get(method, {})
                result = run_method_tests(
                    problem, method, method_info, input_files,
                    benchmark=False, compare_mode=compare_mode, module=module,
                    generator_module=None, generate_count=0,
                    seed=None, save_failed=False, tests_dir="tests"
                )
                
                if result['total'] > 0:
                    assert result['passed'] == result['total'], (
                        f"{problem} ({method}): {result['passed']}/{result['total']} static tests passed"
                    )
    
    @pytest.mark.parametrize("problem", get_all_solution_files())
    def test_generated_tests(self, problem, request):
        """Test all solutions with generated test cases (if available)."""
        # Load solution module
        module, solutions_meta, compare_mode = load_solution_module(problem)
        
        if not module:
            pytest.skip(f"Could not load solution module: {problem}")
        
        # Check if generator exists
        if not has_generator(problem):
            pytest.skip(f"No generator found for {problem}")
        
        # Check if JUDGE_FUNC exists (required for generated tests)
        if not has_judge_func(module):
            pytest.skip(f"No JUDGE_FUNC for {problem} (generated tests require JUDGE_FUNC)")
        
        # Load generator module
        generator_module = load_generator_module(problem)
        if not generator_module:
            pytest.skip(f"Could not load generator module: {problem}")
        
        # Generate a small number of test cases for CI
        generate_count = 5
        
        # Determine which methods to test
        if solutions_meta and "default" in solutions_meta:
            methods_to_test = ["default"]
        else:
            methods_to_test = [None]
        
        # Run generated tests for each method
        for method in methods_to_test:
            generate_func = generator_module.generate
            gen_iter = generate_func(generate_count, seed=42)  # Fixed seed for reproducibility
            
            passed = 0
            total = 0
            
            for i, input_data in enumerate(gen_iter, 1):
                case_name = f"gen_{i}"
                
                ok, elapsed_ms, actual, input_used, peak_rss_bytes, input_bytes, input_scale = run_generated_case(
                    problem, input_data, case_name, method,
                    benchmark=False, compare_mode=compare_mode, module=module
                )
                
                if ok is None:
                    # Should not happen if we checked JUDGE_FUNC, but handle gracefully
                    continue
                
                total += 1
                if ok:
                    passed += 1
                else:
                    pytest.fail(
                        f"{problem} ({method or 'legacy'}): Generated case {i} failed\n"
                        f"Input: {input_data[:200]}...\n"
                        f"Actual: {actual[:200]}..."
                    )
            
            if total > 0:
                assert passed == total, (
                    f"{problem} ({method or 'legacy'}): {passed}/{total} generated tests passed"
                )
    
    @pytest.mark.parametrize("problem", get_all_solution_files())
    def test_combined_static_and_generated(self, problem):
        """Test solutions with both static and generated test cases."""
        # Load solution module
        module, solutions_meta, compare_mode = load_solution_module(problem)
        
        if not module:
            pytest.skip(f"Could not load solution module: {problem}")
        
        # Get static test files
        input_files = get_static_test_files(problem)
        
        # Check generator availability
        generator_module = None
        generate_count = 0
        if has_generator(problem) and has_judge_func(module):
            generator_module = load_generator_module(problem)
            if generator_module:
                generate_count = 3  # Small number for combined test
        
        # Skip if no tests available
        if not input_files and generate_count == 0:
            pytest.skip(f"No tests available for {problem} (no static tests, no generator/JUDGE_FUNC)")
        
        # Determine which methods to test
        if solutions_meta and "default" in solutions_meta:
            methods_to_test = ["default"]
        else:
            methods_to_test = [None]
        
        # Run combined tests for each method
        for method in methods_to_test:
            if method is None:
                # Legacy mode - run manually
                static_passed = 0
                static_total = 0
                gen_passed = 0
                gen_total = 0
                
                # Run static tests
                for in_path in input_files:
                    out_path = in_path.replace(".in", ".out")
                    ok, elapsed_ms, actual, expected, validation_mode = run_one_case(
                        problem, in_path, out_path, None, False, compare_mode, module
                    )
                    
                    if validation_mode == "skip":
                        continue
                    
                    static_total += 1
                    if ok:
                        static_passed += 1
                
                # Run generated tests
                if generator_module and generate_count > 0:
                    generate_func = generator_module.generate
                    gen_iter = generate_func(generate_count, seed=42)
                    
                    for input_data in gen_iter:
                        ok, elapsed_ms, actual, input_used = run_generated_case(
                            problem, input_data, "gen", None,
                            benchmark=False, compare_mode=compare_mode, module=module
                        )
                        
                        if ok is not None:
                            gen_total += 1
                            if ok:
                                gen_passed += 1
                
                total_passed = static_passed + gen_passed
                total_tests = static_total + gen_total
                
                if total_tests > 0:
                    assert total_passed == total_tests, (
                        f"{problem} (legacy): {total_passed}/{total_tests} tests passed "
                        f"(static: {static_passed}/{static_total}, "
                        f"generated: {gen_passed}/{gen_total})"
                    )
            else:
                # Multi-solution mode
                method_info = solutions_meta.get(method, {})
                result = run_method_tests(
                    problem, method, method_info, input_files,
                    benchmark=False, compare_mode=compare_mode, module=module,
                    generator_module=generator_module, generate_count=generate_count,
                    seed=42, save_failed=False, tests_dir="tests"
                )
                
                total_passed = result['passed'] + result.get('gen_passed', 0)
                total_tests = result['total'] + result.get('gen_total', 0)
                
                if total_tests > 0:
                    assert total_passed == total_tests, (
                        f"{problem} ({method}): {total_passed}/{total_tests} tests passed "
                        f"(static: {result['passed']}/{result['total']}, "
                        f"generated: {result.get('gen_passed', 0)}/{result.get('gen_total', 0)})"
                    )

