import jwt
import os
from jwt import ExpiredSignatureError, InvalidTokenError

from api.utils.grpc_exception import Unauthenticated

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret")
ALGORITHM = "HS512"

def get_token(token: str | bytes | None) -> dict:
    if token is None:
        raise Unauthenticated(details="No token provided")
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise Unauthenticated(details="Token has expired")
    except InvalidTokenError:
        raise Unauthenticated(details="Invalid token")

def generate_token(user_id: str) -> str:
    return jwt.encode({"sub": user_id}, SECRET_KEY, algorithm=ALGORITHM)
