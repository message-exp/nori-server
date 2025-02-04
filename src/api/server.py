import grpc

from api.user.user_service import UserServicer
from proto_generated.nori.v0.user.user_service_pb2_grpc import (
    add_UserServiceServicer_to_server,
)
# from api.room.room_service import RoomServicer
# from api.message.message_service import MessageServicer


# server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
def get_server() -> grpc.Server:
    server = grpc.aio.server()

    add_UserServiceServicer_to_server(servicer=UserServicer, server=server)
    # TODO: add other services
    return server
