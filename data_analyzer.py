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


def associate_errors(df):
    """
    Associate ERROR messages with the preceding FAIL test.

    Assumption:
    ERROR lines immediately follow their failed test.
    """

    failures = []
    current_failure = None

    for _, row in df.iterrows():
        status = row["status"]
        message = row["message"]

        if status == "FAIL":
            current_failure = {
                "test_name": message,
                "status": "FAIL",
                "error": None
            }

            failures.append(current_failure)

        elif status == "ERROR" and current_failure is not None:
            if current_failure["error"] is None:
                current_failure["error"] = message
            else:
                current_failure["error"] += "; " + message

        else:
            current_failure = None

    return failures



def main():
    lines = read_log_file("logs/sample.log")
    parsed_logs = parse_log_lines(lines)
    df = create_dataframe(parsed_logs)

    summary = analyze_tests(df)
    failures = associate_errors(df)

    print("=== TEST ANALYSIS REPORT ===")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Pass Rate: {summary['pass_rate']}%")

    print("\n=== FAILURE DETAILS ===")

    for failure in failures:
        print(f"\nTest: {failure['test_name']}")
        print(f"Status: {failure['status']}")
        print(f"Error: {failure['error'] or 'No error details available'}")


if __name__ == "__main__":
    main()