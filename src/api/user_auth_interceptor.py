import grpc
from api.utils.auth import get_token, Unauthenticated

from api.user.user_service import UserServicer
from api.room.room_service import RoomServicer
from api.message.message_service import MessageServicer

# NO_TOKEN = grpc.unary_unary_rpc_terminator(grpc.StatusCode.UNAUTHENTICATED, 'No token provided')
# INVALID_TOKEN = grpc.unary_unary_rpc_terminator(grpc.StatusCode.UNAUTHENTICATED, 'Invalid token')
# NO_PERMISSION = grpc.unary_unary_rpc_terminator(grpc.StatusCode.PERMISSION_DENIED, 'No permission to access this resource')

auth_config: dict[str, bool] = {}
auth_config.update(UserServicer.auth_config)
auth_config.update(RoomServicer.auth_config)
auth_config.update(MessageServicer.auth_config)

class UserAuthInterceptor(grpc.ServerInterceptor):

    def __init__(self) -> None:
        # def abort(ignored_request, context) -> None:
        #     context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Invalid token')
        # self._abortion = grpc.unary_unary_rpc_method_handler(abort)
        pass

    def intercept_service(self, continuation: grpc.ServerInterceptor, handler_call_details: grpc.HandlerCallDetails) -> grpc.RpcMethodHandler:
        metadata = dict(handler_call_details.invocation_metadata)
        method = handler_call_details.method  # /package.Service/Method
        
        # check if the endpoint needs authentication
        if (method not in auth_config) or (not auth_config[method]):
            return continuation(handler_call_details)

        # Grab token
        token = metadata.get('authorization')

        # Check if a token is provided
        if token is None:
            return grpc.unary_unary_rpc_terminator(grpc.StatusCode.UNAUTHENTICATED, 'No token provided')

        # Validate token
        try:
            get_token(token)
        except Unauthenticated as e:
            return grpc.unary_unary_rpc_terminator(e.status_code, e.details)
        
        return continuation(handler_call_details)
    
        # if expected_metadata in handler_call_details.invocation_metadata:
        #     return continuation(handler_call_details)
        # else:
        #     return self._abortion

