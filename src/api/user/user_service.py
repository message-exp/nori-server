from grpc.aio import ServicerContext

from src.utils.token_helper import auth_required

from google.protobuf.empty_pb2 import Empty
from proto_generated.nori.v0.user.user_pb2 import User
from proto_generated.nori.v0.user.user_login_pb2 import UserEmailPasswordLogin
from proto_generated.nori.v0.user.user_id_pb2 import UserId
from proto_generated.nori.v0.user.user_profile_pb2 import UserProfile
from proto_generated.nori.v0.room.room_list_pb2 import RoomList

from proto_generated.nori.v0.user.user_service_pb2_grpc import (
    UserServiceServicer,
)


class UserServicer(UserServiceServicer):
    """
    UserServicer implements the UserService interface from user_service.proto.

    Attributes:
        service_namespace (str): The namespace of the service.
        auth_config (dict[str, bool]): A dictionary that maps the RPC path to a boolean value indicating whether the RPC requires authentication.
    """

    @auth_required
    def GetUser(self, request: UserId, context: ServicerContext) -> User:
        # TODO: check user_id format
        # TODO: get user data from database
        # TODO: return user data
        return User()

    def Login(self, request: UserEmailPasswordLogin, context: ServicerContext) -> Empty:
        # TODO: check email format
        # TODO: ...... (implement login logic)

        # context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        # context.set_details('Method not implemented!')
        return Empty()

    @auth_required
    def Logout(self, request: UserId, context: ServicerContext) -> Empty:
        # TODO: ...... (implement logout logic)
        return Empty()

    def Signup(self, request: User, context: ServicerContext) -> Empty:
        # TODO: ...... (implement signup logic)
        return Empty()

    @auth_required
    def DeleteUser(self, request: UserId, context: ServicerContext) -> Empty:
        # TODO: ...... (implement delete user logic)
        return Empty()

    @auth_required
    def UpdateUserProfile(
        self, request: UserProfile, context: ServicerContext
    ) -> Empty:
        # TODO: ...... (implement update user profile logic)
        return Empty()

    @auth_required
    def GetUserRoomList(self, request: UserId, context: ServicerContext) -> RoomList:
        # TODO: ...... (implement get user room list logic)
        return RoomList()
