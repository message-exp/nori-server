from grpc.aio import ServicerContext

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
)


class RoomServicer(RoomServiceServicer):
    def CreateRoom(self, request: RoomCreateRequest, context: ServicerContext) -> Empty:
        # TODO: ...... (implement create room logic)
        # context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        # context.set_details('Method not implemented!')
        return Empty()

    def InviteToRoom(self, request: RoomUserRequest, context: ServicerContext) -> Empty:
        # TODO: ...... (implement invite to room logic)
        return Empty()

    def JoinRoom(self, request: RoomUserRequest, context: ServicerContext) -> Empty:
        # TODO: ...... (implement join room logic)
        return Empty()

    def LeaveRoom(self, request: RoomUserRequest, context: ServicerContext) -> Empty:
        # TODO: ...... (implement leave room logic)
        return Empty()

    def GetRoom(self, request: RoomId, context: ServicerContext) -> Room:
        # TODO: ...... (implement get room logic)
        return Room()

    def UpdateRoomBasic(
        self, request: RoomBasicInfoRequest, context: ServicerContext
    ) -> Empty:
        # TODO: ...... (implement update room basic info logic)
        return Empty()
