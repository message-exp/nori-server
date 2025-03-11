import grpc
from grpc.aio import ServicerContext

from google.protobuf.empty_pb2 import Empty
from proto_generated.nori.v0.room.room_user_request_pb2 import RoomUserRequest

from proto_generated.nori.v0.room.member.invite_user_to_room_request_pb2 import (
    InviteUserToRoomRequest,
)
from proto_generated.nori.v0.room.member.room_join_invite_reply_pb2 import (
    RoomJoinInviteReply,
)
from proto_generated.nori.v0.room.member.room_join_request_reply_pb2 import (
    RoomJoinRequestReply,
)
from proto_generated.nori.v0.room.member.room_member_pb2 import (
    RoomMember,
    RoomMemberList,
    RoomMemberStatus,
)
from proto_generated.nori.v0.user.user_id_pb2 import UserId
from utils.token_helper import auth_required
from utils.db_helper import get_db
from model import RoomMembers

from repositories import RoomRepo, RoomMemberRepo, UserRepo


from proto_generated.nori.v0.room.member.room_member_service_pb2_grpc import (
    RoomMemberServiceServicer,
)


class RoomMemberServicer(RoomMemberServiceServicer):
    @auth_required
    def GetRoomMembers(
        self, request: RoomUserRequest, context: ServicerContext
    ) -> RoomMemberList:
        user_id = request.user_id.id
        room_id = request.room_id.id

        # check room exist
        room_repo = RoomRepo(next(get_db()))
        if not room_repo.exists_room(room_id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Room with ID {room_id} not found.")
            return RoomMemberList()

        # check user exist
        user_repo = UserRepo(next(get_db()))
        if not user_repo.exists_user(user_id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {user_id} not found.")
            return RoomMemberList()

        # get room members
        room_member_repo = RoomMemberRepo(next(get_db()))
        room_members = room_member_repo.get_room_room_members(room_id=room_id)
        result = []
        for room_member in room_members:
            appendResult = RoomMember(
                user_id=UserId(id=room_member.user_id),
                room_nickname=room_member.room_name,
                status=RoomMemberStatus.JOINED,  # TODO: implement status
            )
            result.append(appendResult)
        return RoomMemberList(members=result)

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
        return Empty()
