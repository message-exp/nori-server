import grpc
from grpc import ServerInterceptor, HandlerCallDetails, RpcMethodHandler
from api.utils.auth import get_token, Unauthenticated

from api.user.user_service import UserServicer

# NO_TOKEN = grpc.unary_unary_rpc_terminator(grpc.StatusCode.UNAUTHENTICATED, 'No token provided')
# INVALID_TOKEN = grpc.unary_unary_rpc_terminator(grpc.StatusCode.UNAUTHENTICATED, 'Invalid token')
# NO_PERMISSION = grpc.unary_unary_rpc_terminator(grpc.StatusCode.PERMISSION_DENIED, 'No permission to access this resource')

auth_list: dict[str, bool] = {}
auth_list.update(UserServicer.auth_list)
# TODO: add other services

class UserAuthInterceptor(grpc.ServerInterceptor):

    def __init__(self) -> None:
        # def abort(ignored_request, context) -> None:
        #     context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Invalid token')
        # self._abortion = grpc.unary_unary_rpc_method_handler(abort)
        pass

    def intercept_service(self, continuation: ServerInterceptor, handler_call_details: HandlerCallDetails) -> RpcMethodHandler:
        metadata = dict(handler_call_details.invocation_metadata)
        method = handler_call_details.method  # /package.Service/Method
        
        # check if the endpoint needs authentication
        if (method not in auth_list) or (not auth_list[method]):
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

