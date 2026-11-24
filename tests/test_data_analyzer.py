from log_parser import parse_log_lines
from data_analyzer import (
    create_dataframe,
    analyze_tests,
    associate_errors,
)

def test_analyze_tests_with_passes_and_failures():
    # Arrange: Create sample test logs.
    lines = [
        "2026-11-23 12:00:01 PASS LoginTest",
        "2026-11-23 12:00:02 FAIL CheckoutTest",
        "2026-11-23 12:00:03 ERROR Payment gateway timeout",
        "2026-11-23 12:00:04 PASS LogoutTest"
    ]

    # Act: Parse the logs and calculate statistics.
    parsed_logs = parse_log_lines(lines)
    df = create_dataframe(parsed_logs)
    result = analyze_tests(df)

    # Assert: Verify the calculated statistics.
    assert result["total_tests"] == 3
    assert result["passed"] == 2
    assert result["failed"] == 1
    assert result["pass_rate"] == 66.67
    assert result["failed_tests"] == ["CheckoutTest"]
    assert result["errors"] == ["Payment gateway timeout"]

def test_analyze_tests_all_passed():
    lines = [
        "2026-11-23 12:00:01 PASS LoginTest",
        "2026-11-23 12:00:02 PASS RegistrationTest",
        "2026-11-23 12:00:03 PASS LogoutTest"
    ]

    parsed_logs = parse_log_lines(lines)
    df = create_dataframe(parsed_logs)
    result = analyze_tests(df)

    assert result["total_tests"] == 3
    assert result["passed"] == 3
    assert result["failed"] == 0
    assert result["pass_rate"] == 100.0
    assert result["failed_tests"] == []
    assert result["errors"] == []

def test_analyze_tests_empty_logs():
    parsed_logs = parse_log_lines([])
    df = create_dataframe(parsed_logs)
    result = analyze_tests(df)

    assert result["total_tests"] == 0
    assert result["passed"] == 0
    assert result["failed"] == 0
    assert result["pass_rate"] == 0
    assert result["failed_tests"] == []
    assert result["errors"] == []


def test_associate_single_error():
    lines = [
        "2026-11-23 12:00:01 FAIL CheckoutTest",
        "2026-11-23 12:00:02 ERROR Payment gateway timeout"
    ]

    parsed_logs = parse_log_lines(lines)
    df = create_dataframe(parsed_logs)

    result = associate_errors(df)

    assert len(result) == 1
    assert result[0]["test_name"] == "CheckoutTest"
    assert result[0]["status"] == "FAIL"
    assert result[0]["error"] == "Payment gateway timeout"


def test_associate_multiple_errors():
    lines = [
        "2026-11-23 12:00:01 FAIL DatabaseTest",
        "2026-11-23 12:00:02 ERROR Connection timeout",
        "2026-11-23 12:00:03 ERROR Database unavailable"
    ]

    parsed_logs = parse_log_lines(lines)
    df = create_dataframe(parsed_logs)

    result = associate_errors(df)

    assert len(result) == 1
    assert result[0]["test_name"] == "DatabaseTest"
    assert result[0]["error"] == (
        "Connection timeout; Database unavailable"
    )

def test_associate_failure_without_error():
    lines = [
        "2026-11-23 12:00:01 FAIL PaymentTest",
        "2026-11-23 12:00:02 INFO Test execution completed"
    ]

    parsed_logs = parse_log_lines(lines)
    df = create_dataframe(parsed_logs)

    result = associate_errors(df)

    assert len(result) == 1
    assert result[0]["test_name"] == "PaymentTest"
    assert result[0]["status"] == "FAIL"
    assert result[0]["error"] is None
