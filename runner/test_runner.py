# runner/test_runner.py
"""
Test Runner - 支援多解法測試與效能比較
Usage:
    python runner/test_runner.py 0001_two_sum                    # 執行預設解法
    python runner/test_runner.py 0023 --method heap              # 執行指定解法
    python runner/test_runner.py 0023 --all                      # 執行所有解法
    python runner/test_runner.py 0023 --all --benchmark          # 所有解法 + 效能比較
"""
import subprocess
import glob
import os
import sys
import time
import argparse
import importlib.util
from typing import Optional, Dict, List, Any

PYTHON_EXE = sys.executable


def normalize_output(s: str) -> str:
    """正規化輸出，避免多餘空白/換行造成比對失敗。"""
    lines = s.strip().splitlines()
    lines = [line.rstrip() for line in lines]
    return "\n".join(lines)


def load_solution_module(problem: str):
    """動態載入 solution 模組，取得 SOLUTIONS metadata"""
    solution_path = os.path.join("solutions", f"{problem}.py")
    if not os.path.exists(solution_path):
        return None, None
    
    spec = importlib.util.spec_from_file_location(f"solution_{problem}", solution_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"⚠️ 載入模組時發生錯誤: {e}")
        return None, None
    
    # 取得 SOLUTIONS metadata（如果有的話）
    solutions_meta = getattr(module, 'SOLUTIONS', None)
    return module, solutions_meta


def run_one_case(problem: str, input_path: str, output_path: str, 
                 method: Optional[str] = None, benchmark: bool = False) -> tuple[bool, float]:
    """
    執行單一測資
    Returns: (passed: bool, elapsed_ms: float)
    """
    with open(input_path, "r", encoding="utf-8") as f:
        input_data = f.read()
    
    with open(output_path, "r", encoding="utf-8") as f:
        expected = f.read()
    
    solution_path = os.path.join("solutions", f"{problem}.py")
    if not os.path.exists(solution_path):
        print(f"❌ 找不到解答檔案: {solution_path}")
        return False, 0.0
    
    # 準備環境變數傳遞 method 參數
    env = os.environ.copy()
    if method:
        env['SOLUTION_METHOD'] = method
    
    start_time = time.perf_counter()
    result = subprocess.run(
        [PYTHON_EXE, solution_path],
        input=input_data,
        text=True,
        capture_output=True,
        env=env
    )
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    
    actual = result.stdout
    exp_norm = normalize_output(expected)
    act_norm = normalize_output(actual)
    
    ok = (exp_norm == act_norm)
    return ok, elapsed_ms


def run_method_tests(problem: str, method_name: str, method_info: Dict[str, Any],
                     input_files: List[str], benchmark: bool = False) -> Dict[str, Any]:
    """執行某個解法的所有測資"""
    results = {
        "method": method_name,
        "display_name": method_info.get("method", method_name),
        "complexity": method_info.get("complexity", "Unknown"),
        "description": method_info.get("description", ""),
        "cases": [],
        "passed": 0,
        "total": 0,
        "times": []
    }
    
    print(f"\n📌 Method: {method_name}")
    if method_info.get("complexity"):
        print(f"   Complexity: {method_info['complexity']}")
    if method_info.get("description"):
        print(f"   Description: {method_info['description']}")
    print()
    
    for in_path in input_files:
        out_path = in_path.replace(".in", ".out")
        if not os.path.exists(out_path):
            print(f"   ⚠️ 找不到對應的 output 檔: {out_path}")
            continue
        
        case_name = os.path.basename(in_path).replace(".in", "")
        ok, elapsed_ms = run_one_case(problem, in_path, out_path, method_name, benchmark)
        
        results["total"] += 1
        results["times"].append(elapsed_ms)
        
        if ok:
            results["passed"] += 1
            if benchmark:
                print(f"   {case_name}: ✅ PASS ({elapsed_ms:.2f}ms)")
            else:
                print(f"   {case_name}: ✅ PASS")
        else:
            print(f"   {case_name}: ❌ FAIL")
        
        results["cases"].append({
            "name": case_name,
            "passed": ok,
            "time_ms": elapsed_ms
        })
    
    return results


def print_benchmark_summary(all_results: List[Dict[str, Any]]):
    """印出效能比較表"""
    print("\n" + "=" * 60)
    print("📊 Performance Comparison")
    print("=" * 60)
    
    # 表頭
    print(f"{'Method':<20} {'Avg Time':<12} {'Complexity':<15} {'Pass Rate'}")
    print("-" * 60)
    
    for result in all_results:
        method = result["method"]
        complexity = result["complexity"]
        avg_time = sum(result["times"]) / len(result["times"]) if result["times"] else 0
        pass_rate = f"{result['passed']}/{result['total']}"
        
        print(f"{method:<20} {avg_time:>8.2f}ms   {complexity:<15} {pass_rate}")
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="LeetCode Test Runner - 支援多解法測試",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python runner/test_runner.py 0001_two_sum
  python runner/test_runner.py 0023 --method heap
  python runner/test_runner.py 0023 --all
  python runner/test_runner.py 0023 --all --benchmark
        """
    )
    parser.add_argument("problem", help="題目名稱 (e.g., 0001_two_sum)")
    parser.add_argument("--method", "-m", help="指定要測試的解法名稱")
    parser.add_argument("--all", "-a", action="store_true", help="測試所有解法")
    parser.add_argument("--benchmark", "-b", action="store_true", help="顯示執行時間比較")
    parser.add_argument("--tests-dir", "-t", default="tests", help="測資目錄 (預設: tests)")
    
    args = parser.parse_args()
    
    problem = args.problem
    tests_dir = args.tests_dir
    
    # 找測資檔案
    pattern = os.path.join(tests_dir, f"{problem}_*.in")
    input_files = sorted(glob.glob(pattern))
    if not input_files:
        print(f"⚠️ 找不到測資檔案 (no test inputs): {pattern}")
        sys.exit(1)
    
    # 載入 solution 模組取得 SOLUTIONS metadata
    module, solutions_meta = load_solution_module(problem)
    
    print(f"\n{'=' * 60}")
    print(f"🧪 Testing: {problem}")
    print(f"{'=' * 60}")
    
    # 決定要測試哪些解法
    if args.all and solutions_meta:
        # 測試所有解法
        methods_to_test = list(solutions_meta.keys())
    elif args.method:
        # 測試指定解法
        methods_to_test = [args.method]
    elif solutions_meta and "default" in solutions_meta:
        # 有 SOLUTIONS 但沒指定，用 default
        methods_to_test = ["default"]
    else:
        # 沒有 SOLUTIONS metadata，使用傳統模式
        methods_to_test = [None]
    
    all_results = []
    
    for method in methods_to_test:
        if method is None:
            # 傳統模式：不指定 method
            print(f"\n📌 Running default solution...")
            print()
            passed = 0
            total = 0
            times = []
            
            for in_path in input_files:
                out_path = in_path.replace(".in", ".out")
                if not os.path.exists(out_path):
                    print(f"   ⚠️ 找不到對應的 output 檔: {out_path}")
                    continue
                
                case_name = os.path.basename(in_path).replace(".in", "")
                ok, elapsed_ms = run_one_case(problem, in_path, out_path, None, args.benchmark)
                total += 1
                times.append(elapsed_ms)
                
                if ok:
                    passed += 1
                    if args.benchmark:
                        print(f"   {case_name}: ✅ PASS ({elapsed_ms:.2f}ms)")
                    else:
                        print(f"   {case_name}: ✅ PASS")
                else:
                    print(f"   {case_name}: ❌ FAIL")
            
            print(f"\n測試結果 / Summary: {passed} / {total} cases passed.")
            
            if args.benchmark and times:
                avg_time = sum(times) / len(times)
                print(f"平均執行時間 / Avg Time: {avg_time:.2f}ms")
        else:
            # 多解法模式
            method_info = solutions_meta.get(method, {"method": method}) if solutions_meta else {"method": method}
            result = run_method_tests(problem, method, method_info, input_files, args.benchmark)
            all_results.append(result)
            print(f"\n   Result: {result['passed']} / {result['total']} cases passed.")
    
    # 如果是多解法 + benchmark，印出比較表
    if len(all_results) > 1 and args.benchmark:
        print_benchmark_summary(all_results)
    elif len(all_results) == 1:
        result = all_results[0]
        print(f"\n測試結果 / Summary: {result['passed']} / {result['total']} cases passed.")


if __name__ == "__main__":
    main()
