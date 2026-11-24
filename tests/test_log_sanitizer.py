import pytest

from log_sanitizer import sanitize_log


def test_sanitize_api_key():
    text = "ERROR api_key=example123"

    result = sanitize_log(text)

    assert result == "ERROR api_key=[REDACTED]"


def test_sanitize_multiple_credentials():
    text = "ERROR password=example123 token=abc456"

    result = sanitize_log(text)

    assert result == (
        "ERROR password=[REDACTED] "
        "token=[REDACTED]"
    )


def test_preserve_safe_log():
    text = "2026-11-24 10:00:00 PASS LoginTest"

    result = sanitize_log(text)

    assert result == text


def test_reject_non_string_input():
    with pytest.raises(TypeError):
        sanitize_log(None)


def test_sanitize_bearer_token():
    text = (
        "ERROR Authorization: Bearer "
        "eyJhbGciOiJIUzI1NiJ9.example.signature"
    )

    result = sanitize_log(text)

    assert result == (
        "ERROR Authorization: Bearer [REDACTED]"
    )
    assert "eyJhbGciOiJIUzI1NiJ9" not in result


def test_sanitize_email_address():
    text = "ERROR Login failed for user@example.com"

    result = sanitize_log(text)

    assert result == (
        "ERROR Login failed for [EMAIL_REDACTED]"
    )
    assert "user@example.com" not in result


def test_sanitize_multiple_email_addresses():
    text = (
        "INFO Notification from admin@example.com "
        "to customer@example.org"
    )

    result = sanitize_log(text)

    assert result.count("[EMAIL_REDACTED]") == 2
    assert "admin@example.com" not in result
    assert "customer@example.org" not in result


def test_sanitize_json_password():
    text = '{"username": "demo", "password": "secret123"}'

    result = sanitize_log(text)

    assert '"password": "[REDACTED]"' in result
    assert "secret123" not in result


def test_sanitize_json_multiple_credentials():
    text = (
        '{"api_key": "example123", '
        '"access_token": "abc456"}'
    )

    result = sanitize_log(text)

    assert '"api_key": "[REDACTED]"' in result
    assert '"access_token": "[REDACTED]"' in result
    assert "example123" not in result
    assert "abc456" not in result
