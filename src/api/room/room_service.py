import grpc
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

from utils.db_helper import get_db
from model import Rooms, RoomMembers

from repositories.user_repository import UserRepository
from repositories.room_member_repository import RoomMemberRepository
from repositories.room_repostitory import RoomRepository


class RoomServicer(RoomServiceServicer):
    def CreateRoom(
        self, request: RoomCreateRequest, context: ServicerContext
    ) -> RoomId:
        user_id = request.user_id.user_id
        room_name = request.name
        user_repository = UserRepository(next(get_db()))
        user = user_repository.get_user(user_id=user_id)

        # check user exist
        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {user_id} not found.")
            return RoomId()

        # create room
        room_repository = RoomRepository(next(get_db()))
        room_id = room_repository.create_room(Rooms(name=room_name))

        # create room_member for user in the room
        room_member_repository = RoomMemberRepository(next(get_db()))
        room_member_repository.create_room_member(
            RoomMembers(
                room_id=room_id,
                user_id=user_id,
                user_name=user.display_name,
                room_name=room_name,
            )
        )
        return RoomId(room_id=room_id)

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
