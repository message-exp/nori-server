import grpc
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class LoggingInterceptor(grpc.aio.ServerInterceptor):

    def __init__(self) -> None:

        # def abort(ignored_request: grpc.RpcMethodHandler, context: grpc.ServicerContext) -> None:
        #     context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Invalid signature')

        # self._abortion = grpc.unary_unary_rpc_method_handler(abort)
        pass

    def intercept_service(self, continuation: grpc.ServerInterceptor, handler_call_details: grpc.HandlerCallDetails) -> grpc.RpcMethodHandler:
        # get the method name
        method_name = handler_call_details.method.split('/')[-1]
        metadata = handler_call_details.invocation_metadata
        
        # Log the incoming request details
        logger.info("Incoming call to method: %s", method_name)
        logger.info("Invocation metadata: %s", metadata)

        return continuation(handler_call_details)
