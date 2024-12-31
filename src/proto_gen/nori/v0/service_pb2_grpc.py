"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from ...nori.v0 import message_pb2 as nori_dot_v0_dot_message__pb2
from ...nori.v0 import room_pb2 as nori_dot_v0_dot_room__pb2
from ...nori.v0 import service_pb2 as nori_dot_v0_dot_service__pb2
from ...nori.v0 import user_pb2 as nori_dot_v0_dot_user__pb2
GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in nori/v0/service_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class ServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateUser = channel.unary_unary('/nori.v0.Service/CreateUser', request_serializer=nori_dot_v0_dot_service__pb2.UserRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)
        self.GetUser = channel.unary_unary('/nori.v0.Service/GetUser', request_serializer=nori_dot_v0_dot_service__pb2.UserRequest.SerializeToString, response_deserializer=nori_dot_v0_dot_user__pb2.User.FromString, _registered_method=True)
        self.CreateRoom = channel.unary_unary('/nori.v0.Service/CreateRoom', request_serializer=nori_dot_v0_dot_room__pb2.Room.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)
        self.JoinRoom = channel.unary_unary('/nori.v0.Service/JoinRoom', request_serializer=nori_dot_v0_dot_service__pb2.JoinRoomRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)
        self.GetRoom = channel.unary_unary('/nori.v0.Service/GetRoom', request_serializer=nori_dot_v0_dot_service__pb2.RoomRequest.SerializeToString, response_deserializer=nori_dot_v0_dot_room__pb2.Room.FromString, _registered_method=True)
        self.SendMessage = channel.unary_unary('/nori.v0.Service/SendMessage', request_serializer=nori_dot_v0_dot_message__pb2.Message.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)
        self.GetMessages = channel.unary_stream('/nori.v0.Service/GetMessages', request_serializer=nori_dot_v0_dot_service__pb2.UserRequest.SerializeToString, response_deserializer=nori_dot_v0_dot_message__pb2.Message.FromString, _registered_method=True)

class ServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateRoom(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def JoinRoom(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRoom(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMessages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_ServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'CreateUser': grpc.unary_unary_rpc_method_handler(servicer.CreateUser, request_deserializer=nori_dot_v0_dot_service__pb2.UserRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'GetUser': grpc.unary_unary_rpc_method_handler(servicer.GetUser, request_deserializer=nori_dot_v0_dot_service__pb2.UserRequest.FromString, response_serializer=nori_dot_v0_dot_user__pb2.User.SerializeToString), 'CreateRoom': grpc.unary_unary_rpc_method_handler(servicer.CreateRoom, request_deserializer=nori_dot_v0_dot_room__pb2.Room.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'JoinRoom': grpc.unary_unary_rpc_method_handler(servicer.JoinRoom, request_deserializer=nori_dot_v0_dot_service__pb2.JoinRoomRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'GetRoom': grpc.unary_unary_rpc_method_handler(servicer.GetRoom, request_deserializer=nori_dot_v0_dot_service__pb2.RoomRequest.FromString, response_serializer=nori_dot_v0_dot_room__pb2.Room.SerializeToString), 'SendMessage': grpc.unary_unary_rpc_method_handler(servicer.SendMessage, request_deserializer=nori_dot_v0_dot_message__pb2.Message.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'GetMessages': grpc.unary_stream_rpc_method_handler(servicer.GetMessages, request_deserializer=nori_dot_v0_dot_service__pb2.UserRequest.FromString, response_serializer=nori_dot_v0_dot_message__pb2.Message.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('nori.v0.Service', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('nori.v0.Service', rpc_method_handlers)

class Service(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateUser(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nori.v0.Service/CreateUser', nori_dot_v0_dot_service__pb2.UserRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetUser(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nori.v0.Service/GetUser', nori_dot_v0_dot_service__pb2.UserRequest.SerializeToString, nori_dot_v0_dot_user__pb2.User.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def CreateRoom(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nori.v0.Service/CreateRoom', nori_dot_v0_dot_room__pb2.Room.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def JoinRoom(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nori.v0.Service/JoinRoom', nori_dot_v0_dot_service__pb2.JoinRoomRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetRoom(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nori.v0.Service/GetRoom', nori_dot_v0_dot_service__pb2.RoomRequest.SerializeToString, nori_dot_v0_dot_room__pb2.Room.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def SendMessage(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nori.v0.Service/SendMessage', nori_dot_v0_dot_message__pb2.Message.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetMessages(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_stream(request, target, '/nori.v0.Service/GetMessages', nori_dot_v0_dot_service__pb2.UserRequest.SerializeToString, nori_dot_v0_dot_message__pb2.Message.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)