import os
import jwt

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret")
ALGORITHM = "HS512"

def get_token(token: str | bytes) -> dict:
    """
    Decode the token and return the payload.
    Need to catch the exceptions from jwt.decode(), including jwt.ExpiredSignatureError, jwt.InvalidTokenError, etc.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def generate_token(user_id: str) -> str:
    return jwt.encode({"sub": user_id}, SECRET_KEY, algorithm=ALGORITHM)
