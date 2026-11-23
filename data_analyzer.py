import pandas as pd

from log_parser import read_log_file, parse_log_lines


def create_dataframe(parsed_logs):
    """Convert parsed log entries into a DataFrame."""
    return pd.DataFrame(
        parsed_logs,
        columns=["date", "time", "status", "message"]
    )


def analyze_tests(df):
    """Calculate test statistics using Pandas."""

    # Select actual test results
    tests = df[df["status"].isin(["PASS", "FAIL"])]

    # Select passed and failed tests
    passed = tests[tests["status"] == "PASS"]
    failed = tests[tests["status"] == "FAIL"]

    # Extract error messages
    errors = df[df["status"] == "ERROR"]

    total_tests = len(tests)
    passed_count = len(passed)
    failed_count = len(failed)

    pass_rate = (
        round(passed_count / total_tests * 100, 2)
        if total_tests > 0 else 0
    )

    return {
        "total_tests": total_tests,
        "passed": passed_count,
        "failed": failed_count,
        "pass_rate": pass_rate,
        "failed_tests": failed["message"].tolist(),
        "errors": errors["message"].tolist()
    }


def main():
    lines = read_log_file("logs/sample.log")
    parsed_logs = parse_log_lines(lines)
    df = create_dataframe(parsed_logs)

    summary = analyze_tests(df)

    print("=== TEST ANALYSIS REPORT ===")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Pass Rate: {summary['pass_rate']}%")

    print("\nFailed Tests:")
    for test in summary["failed_tests"]:
        print(f"- {test}")

    print("\nError Messages:")
    for error in summary["errors"]:
        print(f"- {error}")


if __name__ == "__main__":
    main()
