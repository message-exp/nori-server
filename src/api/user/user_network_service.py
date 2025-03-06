import grpc
from grpc import ServicerContext
from proto_generated.nori.v0.user.network.user_network_service_pb2_grpc import (
    UserNetworkServiceServicer,
)
from src.proto_generated.nori.v0.room.general.room_basic_info_response_pb2 import (
    RoomBasicInfoResponse,
)
from src.proto_generated.nori.v0.room.general.room_list_pb2 import RoomList
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from src.utils.db_helper import get_db
from utils.token_helper import auth_required
from src.repositories import RoomMemberRepo


class UserNetworkService(UserNetworkServiceServicer):
    @auth_required
    def GetUserRoomList(self, request: UserId, context: ServicerContext) -> RoomList:
        # get user ID from request
        user_id = request.id

        # get user room_member data from database
        room_member_repo = RoomMemberRepo(next(get_db()))
        user_room_members = room_member_repo.get_user_room_members(user_id)

        # check if user room_member object exists in database
        if user_room_members is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {user_id} has no associated rooms.")
            return RoomList()

        rooms = []
        for room_member in user_room_members:
            room_basic_info = RoomBasicInfoResponse(
                room_id=RoomId(id=room_member.room_id),
            )
            # For the name oneof, prioritize the custom name if provided.
            if room_member.room_name:
                room_basic_info.custom_name = room_member.room_name
            else:
                room_basic_info.shared_name = room_member.room.name
            # For the avatar oneof, prioritize the custom URL if provided.
            if room_member.room_avatar_url:
                room_basic_info.custom_avatar_url = room_member.room_avatar_url
            elif room_member.room.avatar_url:
                room_basic_info.shared_avatar_url = room_member.room.avatar_url
            else:
                room_basic_info.custom_avatar_url = ""
            rooms.append(room_basic_info)

        return RoomList(rooms=rooms)
