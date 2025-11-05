import sys
from io import StringIO
from typing import List, Dict, Any
import ast

def check_code_syntax(code: str) -> tuple[bool, str]:
    try:
        ast.parse(code)
        return True, "Syntax OK"
    except SyntaxError as e:
        return False, f"Syntax Error: {str(e)}"

def run_test_case(code: str, test_input: str, expected_output: str) -> Dict[str, Any]:
    result = {
        "passed": False,
        "input": test_input,
        "expected": expected_output,
        "actual": "",
        "error": None
    }
    
    try:
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        
        sys.stdin = StringIO(test_input)
        sys.stdout = StringIO()
        
        namespace = {}
        exec(code, namespace)
        
        output = sys.stdout.getvalue().strip()
        result["actual"] = output
        
        if output == expected_output.strip():
            result["passed"] = True
        
    except Exception as e:
        result["error"] = str(e)
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
    
    return result

def check_code(code: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    syntax_ok, syntax_msg = check_code_syntax(code)
    if not syntax_ok:
        return {
            "success": False,
            "message": syntax_msg,
            "test_results": []
        }
    
    test_results = []
    passed_count = 0
    
    for test_case in test_cases:
        result = run_test_case(
            code,
            test_case.get("input", ""),
            test_case.get("expected_output", "")
        )
        test_results.append(result)
        if result["passed"]:
            passed_count += 1

    all_passed = passed_count == len(test_cases)
    message = f"Passed {passed_count}/{len(test_cases)} tests"
    
    return {
        "success": all_passed,
        "message": message,
        "test_results": test_results
    }