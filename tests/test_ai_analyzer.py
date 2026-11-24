import json
from unittest.mock import patch

import pytest

from ai_analyzer import validate_ai_response, analyze_failure


def test_validate_ai_response_valid():
    # Arrange: Create a correctly structured AI response.
    response = {
        "explanation": "The payment service timed out.",
        "possible_causes": [
            "Network connectivity issue",
            "Payment gateway unavailable"
        ],
        "troubleshooting_steps": [
            "Check network connectivity",
            "Verify payment gateway status",
            "Retry the failed test"
        ]
    }

    # Act: Validate the response.
    result = validate_ai_response(response)

    # Assert: The validated response should match the input.
    assert result == response


def test_validate_ai_response_missing_field():
    response = {
        "explanation": "The payment service timed out.",
        "possible_causes": [
            "Network issue",
            "Service unavailable"
        ]
        # troubleshooting_steps is missing
    }

    with pytest.raises(ValueError):
        validate_ai_response(response)


def test_validate_ai_response_wrong_step_count():
    response = {
        "explanation": "The payment service timed out.",
        "possible_causes": [
            "Network issue",
            "Service unavailable"
        ],
        "troubleshooting_steps": [
            "Check connectivity"
        ]
    }

    with pytest.raises(ValueError):
        validate_ai_response(response)
    

def test_analyze_failure_with_mocked_groq():
    # Arrange: Create a failed test.
    failure = {
        "test_name": "CheckoutTest",
        "status": "FAIL",
        "error": "Payment gateway timeout"
    }

    # Arrange: Create a fake AI response.
    fake_analysis = {
        "explanation": "The payment service timed out.",
        "possible_causes": [
            "Network connectivity issue",
            "Payment gateway unavailable"
        ],
        "troubleshooting_steps": [
            "Check network connectivity",
            "Verify payment gateway status",
            "Retry the failed test"
        ]
    }

    # Replace the API key and Groq client during this test.
    with patch.dict("os.environ", {"GROQ_API_KEY": "fake-test-key"}):
        with patch("ai_analyzer.Groq") as mock_groq:
            # Configure the fake Groq response.
            mock_client = mock_groq.return_value

            mock_client.chat.completions.create.return_value.choices = [
                type(
                    "Choice",
                    (),
                    {
                        "message": type(
                            "Message",
                            (),
                            {"content": json.dumps(fake_analysis)}
                        )()
                    }
                )()
            ]

            # Act: Call the real function with a fake API client.
            result = analyze_failure(failure)

            # Assert: Verify the returned AI analysis.
            assert result == fake_analysis

            # Verify that the API method was called once.
            mock_client.chat.completions.create.assert_called_once()


def test_analyze_failure_empty_groq_response():
    failure = {
        "test_name": "CheckoutTest",
        "status": "FAIL",
        "error": "Payment gateway timeout"
    }

    with patch.dict("os.environ", {"GROQ_API_KEY": "fake-test-key"}):
        with patch("ai_analyzer.Groq") as mock_groq:
            mock_client = mock_groq.return_value

            # Simulate an empty response from Groq.
            mock_client.chat.completions.create.return_value.choices[
                0
            ].message.content = ""

            # The function should reject an empty response.
            with pytest.raises(
                RuntimeError,
                match="Groq returned an empty response"
            ):
                analyze_failure(failure)


def test_analyze_failure_invalid_json():
    failure = {
        "test_name": "CheckoutTest",
        "status": "FAIL",
        "error": "Payment gateway timeout"
    }

    with patch.dict("os.environ", {"GROQ_API_KEY": "fake-test-key"}):
        with patch("ai_analyzer.Groq") as mock_groq:
            mock_client = mock_groq.return_value

            # Simulate malformed JSON.
            mock_client.chat.completions.create.return_value.choices[
                0
            ].message.content = "This is not valid JSON"

            # json.loads() should reject malformed JSON.
            with pytest.raises(json.JSONDecodeError):
                analyze_failure(failure)
