from src.utils.validate_format_helper import is_valid_email

def test_valid_email() -> None:
    # List of valid email addresses
    valid_emails = [
        "test@example.com",
        "user.name+tag+sorting@example.com",
        "user_name@example.co.uk",
    ]
    for email in valid_emails:
        assert is_valid_email(email), f"Email {email} should be valid"

def test_invalid_email() -> None:
    # List of invalid email addresses
    invalid_emails = [
        "plainaddress",
        "missingatsign.com",
        "user@.com",
        "@nouser.com",
        "username@",
        "username@domain",
    ]
    for email in invalid_emails:
        assert not is_valid_email(email), f"Email {email} should be invalid"
