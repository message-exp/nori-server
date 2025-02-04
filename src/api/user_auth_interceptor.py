import grpc
import jwt

from src.utils.token_helper import get_token

from api.user.user_service import UserServicer
from api.room.room_service import RoomServicer
from api.message.message_service import MessageServicer

auth_config: dict[str, bool] = {}
auth_config.update(UserServicer.auth_config)
auth_config.update(RoomServicer.auth_config)
auth_config.update(MessageServicer.auth_config)


class UserAuthInterceptor(grpc.ServerInterceptor):
    def __init__(self) -> None:
        def abort(ignored_request, context) -> None:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Access denied")

        self._abortion = grpc.unary_unary_rpc_method_handler(abort)

    def intercept_service(
        self,
        continuation: grpc.ServerInterceptor,
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        metadata = dict(handler_call_details.invocation_metadata)
        method = handler_call_details.method  # /package.Service/Method

        # check if the endpoint needs authentication
        if (method not in auth_config) or (not auth_config[method]):
            return continuation(handler_call_details)

        # Grab token
        token = metadata.get("authorization")

        # Check if a token is provided
        if token is None:
            return self._abortion  # No token provided

        # Validate token
        try:
            get_token(token)
        except jwt.ExpiredSignatureError:
            return self._abortion  # Token expired
        except jwt.InvalidTokenError:
            return self._abortion  # Invalid token

        return continuation(handler_call_details)
