from grpc.aio import Server, ServicerContext

from google.protobuf.empty_pb2 import Empty
from proto_generated.nori.v0.room.room_pb2 import Room
from proto_generated.nori.v0.room.room_id_pb2 import RoomId
from proto_generated.nori.v0.room.room_create_request_pb2 import RoomCreateRequest
from proto_generated.nori.v0.room.room_basic_info_request_pb2 import (
    RoomBasicInfoRequest,
)
from proto_generated.nori.v0.room.room_user_request_pb2 import RoomUserRequest
from proto_generated.nori.v0.room.room_service_pb2_grpc import (
    RoomServiceServicer,
    add_RoomServiceServicer_to_server,
)


class RoomServicer(RoomServiceServicer):
    service_namespace = "nori.v0.RoomService"
    auth_config: dict[str, bool] = dict()

    auth_config[f"/{service_namespace}/CreateRoom"] = True

    def CreateRoom(self, request: RoomCreateRequest, context: ServicerContext) -> Empty:
        # TODO: ...... (implement create room logic)
        # context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        # context.set_details('Method not implemented!')
        return Empty()

    auth_config[f"/{service_namespace}/InviteToRoom"] = True

    def InviteToRoom(self, request: RoomUserRequest, context: ServicerContext) -> Empty:
        # TODO: ...... (implement invite to room logic)
        return Empty()

    auth_config[f"/{service_namespace}/JoinRoom"] = True

    def JoinRoom(self, request: RoomUserRequest, context: ServicerContext) -> Empty:
        # TODO: ...... (implement join room logic)
        return Empty()

    auth_config[f"/{service_namespace}/LeaveRoom"] = True

    def LeaveRoom(self, request: RoomUserRequest, context: ServicerContext) -> Empty:
        # TODO: ...... (implement leave room logic)
        return Empty()

    auth_config[f"/{service_namespace}/GetRoom"] = True

    def GetRoom(self, request: RoomId, context: ServicerContext) -> Room:
        # TODO: ...... (implement get room logic)
        return Room()

    auth_config[f"/{service_namespace}/UpdateRoomBasic"] = True

    def UpdateRoomBasic(
        self, request: RoomBasicInfoRequest, context: ServicerContext
    ) -> Empty:
        # TODO: ...... (implement update room basic info logic)
        return Empty()


def add_service_to_server(server: Server) -> None:
    add_RoomServiceServicer_to_server(RoomServicer(), server)
