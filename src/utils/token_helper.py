import os
import jwt
from datetime import datetime
from typing import Any, Optional

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret")
ALGORITHM = "HS512"


def get_token(token: str | bytes) -> dict:
    """
    Decode the token and return the payload.
    
    Need to catch the exceptions from jwt.decode(), including jwt.ExpiredSignatureError, jwt.InvalidTokenError, etc.

    Parameters:
        token (str | bytes): encoded token

    Returns:
        dict: decoded payload
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def generate_token(
    subject: Optional[str] = None, expire: Optional[datetime] = None
) -> str:
    """
    Generate a token with the user_id.

    Parameters:
        subject (str, optional): user_id to be encoded in the token
        expire (datetime, optional): expiration time of the token

    Returns:
        str: encoded token
    """
    payload: dict[str, Any] = dict()

    if subject is not None:
        payload["sub"] = subject

    if expire is not None:
        payload["exp"] = expire

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
