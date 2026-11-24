import re


def sanitize_log(text):

    # Redact credentials in JSON-style key/value pairs.
    text = re.sub(
        r'(?i)("(?:api_key|apikey|token|access_token|'
        r'secret|password|passwd)"\s*:\s*)"[^"]*"',
        r'\g<1>"[REDACTED]"',
        text
    )

    # Redact common email address formats.
    text = re.sub(
        r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        "[EMAIL_REDACTED]",
        text
    )

    # Redact HTTP Bearer authorization tokens.
    text = re.sub(
        r"(?i)(\bAuthorization\s*:\s*Bearer\s+)\S+",
        r"\g<1>[REDACTED]",
        text
    )

    """Redact common credentials from log text."""

    if not isinstance(text, str):
        raise TypeError("Log content must be a string.")

    # Match common key=value credential patterns.
    credential_pattern = (
        r"(?i)\b"
        r"(api_key|apikey|token|access_token|"
        r"secret|password|passwd)"
        r"(\s*[:=]\s*)"
        r"(\"[^\"]*\"|'[^']*'|[^\s,;]+)"
    )

    def replace_credential(match):
        key = match.group(1)
        separator = match.group(2)

        return f"{key}{separator}[REDACTED]"

    return re.sub(
        credential_pattern,
        replace_credential,
        text
    )
