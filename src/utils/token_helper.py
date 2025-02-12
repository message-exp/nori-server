import jwt
import grpc
import secrets
from datetime import datetime
from typing import Any, Optional, Callable

from utils.config import config

SECRET_KEY = config.JWT_SECRET_KEY
ALGORITHM = config.JWT_ALGORITHM


def auth_required(func: Callable) -> Callable:
    """
    Decorator that ensures the request has a valid authorization token.
    Args:
        func (Callable): The function to be decorated.
    Returns:
        Callable: The wrapped function with authorization check.
    Raises:
        grpc.RpcError: If the token is missing, expired, or invalid, an appropriate gRPC error is raised.
    """

    def wrapper(
        self,  # noqa: ANN001
        request: grpc.aio.Call,
        context: grpc.aio.ServicerContext,
    ) -> grpc.aio.Call:
        metadata = dict(context.invocation_metadata())
        token = metadata.get("authorization")

        if not token:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Missing token")
            return

        try:
            if isinstance(token, (str, bytes)):
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            else:
                context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token type")
                return
            context.user_info = decoded_token
        except jwt.ExpiredSignatureError:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token expired")
            return
        except jwt.InvalidTokenError:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
            return

        return func(self, request, context)

    return wrapper


def generate_jwt_token(
    subject: Optional[str] = None,
    expire: Optional[datetime] = None,
    token_id: Optional[str] = secrets.token_urlsafe(8),
) -> str:
    """
    Generate a token with the user_id.
    Args:
        subject (str, optional): user_id to be encoded in the token
        expire (datetime, optional): expiration time of the token
        token_id (str, optional): unique identifier for the token
    Returns:
        str: encoded token
    """
    payload: dict[str, Any] = dict()

    if subject is not None:
        payload["sub"] = subject

    if expire is not None:
        payload["exp"] = expire

    if token_id is not None:
        payload["jti"] = token_id

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def generate_refresh_token() -> str:
    """
    Generate a random refresh token.
    Returns:
        str: refresh token
    """
    token = secrets.token_urlsafe(64)
    return token
