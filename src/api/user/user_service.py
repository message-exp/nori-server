import grpc
from grpc.aio import ServicerContext

from utils.token_helper import auth_required, generate_token
from utils.validate_format_helper import is_valid_email
from utils.db_helper import get_db

from google.protobuf.empty_pb2 import Empty
from proto_generated.nori.v0.user.user_pb2 import User
from proto_generated.nori.v0.user.user_login_pb2 import UserEmailPasswordLogin
from proto_generated.nori.v0.user.user_id_pb2 import UserId
from proto_generated.nori.v0.user.user_profile_pb2 import UserProfile
from proto_generated.nori.v0.room.room_list_pb2 import RoomList

from proto_generated.nori.v0.user.user_service_pb2_grpc import (
    UserServiceServicer,
)

from repositories import UserRepo


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
        email = request.email
        password = request.password

        # check email format
        if not is_valid_email(email):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid email format")
            return Empty()
        
        # check password format
        if not password:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Password cannot be empty")
            return Empty()

        # get user from database
        user_repo = UserRepo(next(get_db()))
        user = user_repo.get_user(email)

        # check if user exists
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return Empty()

        # create token
        token_id = "generated_device_id"  # TODO: Implement device ID generation
        token = generate_token(subject=user.id, token_id=token_id)

        # save token in database
        # TODO: implement this after the model of the database has been updated

        # put token into metadata
        context.send_initial_metadata([("authorization", token)])
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
