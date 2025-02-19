import jwt
import grpc
import secrets
import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Optional, Callable

from utils.config import config

logger = logging.getLogger(__name__)

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
            logger.error("Missing token in metadata: %s", metadata)
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Missing token")
            return

        # Remove the "Bearer" prefix
        token = str(token).split("Bearer ")[-1]
        logger.debug("Extracted token: %s", token)

        try:
            if isinstance(token, (str, bytes)):
                logger.debug(
                    "Attempting to decode token using secret key and algorithm %s",
                    ALGORITHM,
                )
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                logger.debug("Decoded token payload: %s", decoded_token)
            else:
                logger.error("Invalid token type: %s", type(token))
                context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token type")
                return
            # context.user_info = decoded_token
        except jwt.ExpiredSignatureError:
            logger.error("Token expired: %s", token)
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token expired")
            return
        except jwt.InvalidTokenError as e:
            logger.error("Invalid token: %s | error: %s", token, e)
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
            return
        except Exception as e:
            logger.error("Unknown error while decoding token: %s | error: %s", token, e)
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Unknown error")
            return

        return func(self, request, context)

    return wrapper


def generate_jwt_token(
    subject: Optional[str] = None,
    expire: Optional[datetime] = datetime.now(timezone.utc) + timedelta(minutes=30),
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
        payload["sub"] = str(subject)

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
