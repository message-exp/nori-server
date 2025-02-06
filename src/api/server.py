import grpc

from api.user.user_service import UserServicer
from api.room.room_service import RoomServicer
from api.message.message_service import MessageServicer
from proto_generated.nori.v0.user.user_service_pb2_grpc import (
    add_UserServiceServicer_to_server,
)
from proto_generated.nori.v0.room.room_service_pb2_grpc import (
    add_RoomServiceServicer_to_server,
)
from proto_generated.nori.v0.message.message_service_pb2_grpc import (
    add_MessageServiceServicer_to_server,
)
from proto_generated.nori.v0.room import room_service_pb2
from proto_generated.nori.v0.message import message_service_pb2
from proto_generated.nori.v0.user import user_service_pb2
from grpc_reflection.v1alpha import reflection




def get_server() -> grpc.Server:
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = grpc.aio.server()

    add_UserServiceServicer_to_server(servicer=UserServicer(), server=server)
    add_RoomServiceServicer_to_server(servicer=RoomServicer(), server=server)
    add_MessageServiceServicer_to_server(servicer=MessageServicer(), server=server)
    SERVICE_NAMES = (
        user_service_pb2.DESCRIPTOR.services_by_name["UserService"].full_name,
        room_service_pb2.DESCRIPTOR.services_by_name["RoomService"].full_name,
        message_service_pb2.DESCRIPTOR.services_by_name["MessageService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    # TODO: add other services
    return server
