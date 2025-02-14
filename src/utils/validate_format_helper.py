import re


def is_valid_email(email: str) -> bool:
    EMAIL_REGEX = r"^[^@]+@[^@]+\.[^@]+$"
    return re.fullmatch(EMAIL_REGEX, email) is not None
