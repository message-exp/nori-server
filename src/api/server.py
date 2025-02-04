import grpc

from api.user.user_service import UserServicer
from api.room.room_service import RoomServicer
from proto_generated.nori.v0.user.user_service_pb2_grpc import (
    add_UserServiceServicer_to_server,
)
from proto_generated.nori.v0.room.room_service_pb2_grpc import (
    add_RoomServiceServicer_to_server,
)
from proto_generated.nori.v0.room import room_service_pb2
from grpc_reflection.v1alpha import reflection
# from api.room.room_service import RoomServicer
# from api.message.message_service import MessageServicer


# server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
def get_server() -> grpc.Server:
    server = grpc.aio.server()

    add_UserServiceServicer_to_server(servicer=UserServicer(), server=server)
    add_RoomServiceServicer_to_server(servicer=RoomServicer(), server=server)
    SERVICE_NAMES = (
        room_service_pb2.DESCRIPTOR.services_by_name["RoomService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    # TODO: add other services
    return server