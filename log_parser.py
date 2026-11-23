import re
from pathlib import Path


def read_log_file(file_path):
    """Read a log file and return its lines."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        return file.readlines()


def parse_log_lines(lines):
    """Extract structured information from log lines."""

    parsed_logs = []

    pattern = (
        r"^(\d{4}-\d{2}-\d{2}) "
        r"(\d{2}:\d{2}:\d{2}) "
        r"(INFO|PASS|FAIL|ERROR) "
        r"(.+)$"
    )

    for line in lines:
        match = re.match(pattern, line.strip())

        if match:
            parsed_logs.append({
                "date": match.group(1),
                "time": match.group(2),
                "status": match.group(3),
                "message": match.group(4)
            })

    return parsed_logs


def summarize_tests(parsed_logs):
    """Calculate basic test execution statistics."""

    passed = sum(
        log["status"] == "PASS"
        for log in parsed_logs
    )

    failed = sum(
        log["status"] == "FAIL"
        for log in parsed_logs
    )

    errors = [
        log["message"]
        for log in parsed_logs
        if log["status"] == "ERROR"
    ]

    total = passed + failed

    return {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "pass_rate": round(
            (passed / total) * 100, 2
        ) if total > 0 else 0
    }


def main():
    lines = read_log_file("logs/sample.log")
    parsed_logs = parse_log_lines(lines)
    summary = summarize_tests(parsed_logs)

    print("=== AI TEST LOG ANALYZER ===")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Pass Rate: {summary['pass_rate']}%")

    print("\nDetected Errors:")

    for error in summary["errors"]:
        print(f"- {error}")


if __name__ == "__main__":
    main()
