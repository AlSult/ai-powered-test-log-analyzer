from log_parser import parse_log_lines


def test_parse_valid_log_line():
    # Arrange: Create a sample log line.
    lines = [
        "2026-11-23 12:00:01 PASS LoginTest"
    ]

    # Act: Parse the log line.
    result = parse_log_lines(lines)

    # Assert: Check the expected output.
    assert len(result) == 1
    assert result[0]["date"] == "2026-11-23"
    assert result[0]["time"] == "12:00:01"
    assert result[0]["status"] == "PASS"
    assert result[0]["message"] == "LoginTest"

def test_parse_invalid_log_lines():
    lines = [
        "This is not a valid log line",
        "Hello world",
        "2026-11-23 12:00:01 UNKNOWN LoginTest"
    ]

    result = parse_log_lines(lines)

    assert result == []

def test_parse_multiple_log_lines():
    lines = [
        "2026-11-23 12:00:01 PASS LoginTest",
        "2026-11-23 12:00:02 FAIL CheckoutTest",
        "2026-11-23 12:00:03 ERROR Payment gateway timeout",
        "2026-11-23 12:00:04 PASS LogoutTest"
    ]

    result = parse_log_lines(lines)

    assert len(result) == 4

    assert result[0]["status"] == "PASS"
    assert result[0]["message"] == "LoginTest"

    assert result[1]["status"] == "FAIL"
    assert result[1]["message"] == "CheckoutTest"

    assert result[2]["status"] == "ERROR"
    assert result[2]["message"] == "Payment gateway timeout"

    assert result[3]["status"] == "PASS"
    assert result[3]["message"] == "LogoutTest"