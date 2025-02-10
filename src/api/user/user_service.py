import grpc
from grpc.aio import ServicerContext

from src.utils.token_helper import auth_required

from google.protobuf.empty_pb2 import Empty
from proto_generated.nori.v0.user.user_pb2 import User
from proto_generated.nori.v0.user.user_login_pb2 import UserEmailPasswordLogin
from proto_generated.nori.v0.user.user_id_pb2 import UserId
from proto_generated.nori.v0.user.token_pair_pb2 import TokenPair
from proto_generated.nori.v0.user.access_token_pb2 import AccessToken
from proto_generated.nori.v0.user.user_profile_update_request_pb2 import (
    UserProfileUpdateRequest,
)
from proto_generated.nori.v0.user.user_reset_password_request_pb2 import (
    UserResetPasswordRequest,
)
from proto_generated.nori.v0.user.user_connection_pb2 import UserConnection
from proto_generated.nori.v0.room.room_id_pb2 import RoomId
from proto_generated.nori.v0.room.room_list_pb2 import RoomList
from proto_generated.nori.v0.room.room_basic_info_response_pb2 import (
    RoomBasicInfoResponse,
)

from proto_generated.nori.v0.user.user_service_pb2_grpc import (
    UserServiceServicer,
)

from utils.db_helper import get_db
from repositories import UserRepo, RoomMemberRepo


class UserServicer(UserServiceServicer):
    """
    UserServicer implements the UserService interface from user_service.proto.

    Attributes:
        service_namespace (str): The namespace of the service.
        auth_config (dict[str, bool]): A dictionary that maps the RPC path to a boolean value indicating whether the RPC requires authentication.
    """

    @auth_required
    def GetUser(self, request: UserId, context: ServicerContext) -> User:
        # get user ID from request
        user_id = request.id

        # get user data from database
        user_repo = UserRepo(next(get_db()))
        user = user_repo.get_user_only_ids(user_id)

        # check if user exists in database
        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {user_id} not found.")
            return User()

        # return user data
        return User(
            user_id=UserId(id=user.id),
            username=str(user.username),
            email=str(user.email),
            display_name=str(user.display_name),
            avatar_url="",
            connected_accounts=[UserConnection()],
            rooms=[RoomId(id=room.id) for room in user.rooms],
        )

    def Signup(self, request: User, context: ServicerContext) -> Empty:
        # TODO: ...... (implement signup logic)
        return Empty()

    @auth_required
    def DeleteUser(self, request: UserId, context: ServicerContext) -> Empty:
        # TODO: ...... (implement delete user logic)
        return Empty()

    @auth_required
    def UpdateUserProfile(
        self, request: UserProfileUpdateRequest, context: ServicerContext
    ) -> Empty:
        # TODO: ...... (implement update user profile logic)
        return Empty()

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
            else:
                room_basic_info.shared_avatar_url = room_member.room.avatar_url

            rooms.append(room_basic_info)

        return RoomList(rooms=rooms)

    def Login(
        self, request: UserEmailPasswordLogin, context: ServicerContext
    ) -> TokenPair:
        # TODO: check email format
        # TODO: ...... (implement login logic)
        return TokenPair()

    @auth_required
    def Logout(self, request: TokenPair, context: ServicerContext) -> Empty:
        # TODO: ...... (implement logout logic)
        return Empty()

    @auth_required
    def RefreshToken(self, request: UserId, context: ServicerContext) -> AccessToken:
        # TODO: ...... (implement login logic)
        return AccessToken()

    @auth_required
    def ResetUserPassword(
        self, request: UserResetPasswordRequest, context: ServicerContext
    ) -> Empty:
        # TODO: ...... (implement login logic)
        return Empty()
