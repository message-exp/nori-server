import grpc
from grpc.aio import ServicerContext

from google.protobuf.empty_pb2 import Empty
from proto_generated.nori.v0.room.room_pb2 import Room
from proto_generated.nori.v0.room.room_id_pb2 import RoomId
from proto_generated.nori.v0.room.general.room_create_request_pb2 import (
    RoomCreateRequest,
)
from proto_generated.nori.v0.room.general.room_basic_info_request_pb2 import (
    RoomBasicInfoRequest,
)
from proto_generated.nori.v0.room.general.room_basic_info_response_pb2 import(
    RoomBasicInfoResponse
)
from proto_generated.nori.v0.room.room_user_request_pb2 import RoomUserRequest
from proto_generated.nori.v0.room.room_service_pb2_grpc import RoomServiceServicer
from proto_generated.nori.v0.room.member.room_member_pb2 import (
    RoomMember,
    RoomMemberStatus,
)
from proto_generated.nori.v0.room.member.invite_user_to_room_request_pb2 import (
    InviteUserToRoomRequest,
)
from proto_generated.nori.v0.room.member.room_join_invite_reply_pb2 import (
    RoomJoinInviteReply,
)
from proto_generated.nori.v0.room.member.room_join_request_reply_pb2 import (
    RoomJoinRequestReply,
)
from proto_generated.nori.v0.user.user_id_pb2 import UserId
from utils.token_helper import auth_required
from utils.db_helper import get_db
from model import Rooms, RoomMembers

from repositories import RoomRepo, RoomMemberRepo, UserRepo


class RoomServicer(RoomServiceServicer):
    @auth_required
    def CreateRoom(
        self, request: RoomCreateRequest, context: ServicerContext
    ) -> RoomId:
        user_id = request.creator.id
        room_name = request.name
        user_repo = UserRepo(next(get_db()))
        user = user_repo.get_user(user_id)

        # check user exist
        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {user_id} not found.")
            return RoomId()

        # create room
        room_repo = RoomRepo(next(get_db()))
        room_id = room_repo.create_room(Rooms(name=room_name))

        # create room_member for user in the room
        room_member_repo = RoomMemberRepo(next(get_db()))
        room_member_repo.create_room_member(
            RoomMembers(
                room_id=room_id,
                user_id=user_id,
                user_name=user.display_name,
                room_name=room_name,
            )
        )
        return RoomId(id=room_id)

    @auth_required
    def GetRoom(self, request: RoomUserRequest, context: ServicerContext) -> Room:
        # TODO: fix the braking changes in protos 0.3
        room_id = request.id

        # check room exist
        room_repo = RoomRepo(next(get_db()))
        room = room_repo.get_room(room_id)
        if room is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Room with ID {room_id} not found.")
            return Empty()

        room = Room(
            room_id=RoomId(id=room.id),
            shared_name=room.name,
            custom_name="",
            shared_avatar_url=room.avatar_url,
            custom_avatar_url="",
            members=[
                RoomMember(
                    user_id=UserId(id=member.user_id),
                    room_nickname=member.user_name,
                    status=RoomMemberStatus.JOINED,
                )
                for member in room.members
            ],
        )

        return room
    @auth_required
    def GetRoomBasic(self,request : RoomUserRequest ,context : ServicerContext) -> RoomBasicInfoResponse:
        room_id = request.room_id.id
        user_id = request.user_id.id
        room_repo =RoomRepo(get_db())
        room_exist = room_repo.exists_room(room_id= room_id)
        if not room_exist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Room with ID {room_id} not found.")
            return Empty()
        user_repo = UserRepo(get_db())
        user_exist = user_repo.exists_user(user_id = user_id)
        if not user_exist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {user_id} not found.")
            return Empty()
        
        return RoomBasicInfoResponse()
        

    @auth_required
    def UpdateRoomBasic(
        self, request: RoomBasicInfoRequest, context: ServicerContext
    ) -> Empty:
        # TODO: ...... (implement update room basic info logic)
        return Empty()

    @auth_required
    def InviteToRoom(
        self, request: InviteUserToRoomRequest, context: ServicerContext
    ) -> Empty:
        room_id = request.room_id.id
        inviter_id = request.inviter.id
        invitees_id: list[int] = [invitees_id.id for invitees_id in request.invitees]  # noqa: F841

        # check room exist
        room_repo = RoomRepo(next(get_db()))
        if not room_repo.exists_room(room_id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Room with ID {room_id} not found.")
            return Empty()

        # check inviter exist
        user_repo = UserRepo(next(get_db()))
        if not user_repo.exists_user(inviter_id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {inviter_id} not found.")
            return Empty()

        # check all invitees exist
        if not user_repo.exists_all_users(invitees_id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Users with some IDs in {invitees_id} not found.")
            return Empty()
        # TODO let invitees can refuse Invited
        # create room_members for all invitees in the room
        room_member_repo = RoomMemberRepo(next(get_db()))
        room_member_repo.create_room_members(room_id, invitees_id)

        return Empty()

    @auth_required
    def InviteRoomReply(
        self, request: RoomJoinInviteReply, context: ServicerContext
    ) -> Empty:
        # TODO: ...... (implement invite room reply logic)
        return Empty()

    @auth_required
    def JoinRoom(self, request: RoomUserRequest, context: ServicerContext) -> Empty:
        room_id = request.room_id.id
        user_id = request.user_id.id

        # check room exist
        room_repo = RoomRepo(next(get_db()))
        if not room_repo.exists_room(room_id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Room with ID {room_id} not found.")
            return Empty()

        # check user exist
        user_repo = UserRepo(next(get_db()))
        if not user_repo.exists_user(user_id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {user_id} not found.")
            return Empty()

        # TODO let room owner can refuse joining room
        # create room_member for user in the room
        room_member_repo = RoomMemberRepo(next(get_db()))
        room_member_repo.create_room_member(
            RoomMembers(room_id=room_id, user_id=user_id)
        )
        return Empty()

    @auth_required
    def JoinRoomReply(
        self, request: RoomJoinRequestReply, context: ServicerContext
    ) -> Empty:
        # TODO: ...... (implement join room reply logic)
        return Empty()

    @auth_required
    def LeaveRoom(self, request: RoomUserRequest, context: ServicerContext) -> Empty:
        # TODO: ...... (implement leave room logic)
        return Empty()d
