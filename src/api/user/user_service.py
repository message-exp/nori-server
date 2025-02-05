import grpc
from grpc.aio import ServicerContext

from google.protobuf.empty_pb2 import Empty
from proto_generated.nori.v0.user.user_pb2 import User
from proto_generated.nori.v0.user.user_login_pb2 import UserEmailPasswordLogin
from proto_generated.nori.v0.user.user_id_pb2 import UserId
from proto_generated.nori.v0.user.user_profile_pb2 import UserProfile
from proto_generated.nori.v0.user.user_connection_pb2 import UserConnection
from proto_generated.nori.v0.room.room_id_pb2 import RoomId
from proto_generated.nori.v0.room.room_list_pb2 import RoomList

from proto_generated.nori.v0.user.user_service_pb2_grpc import (
    UserServiceServicer,
)

from utils.db_helper import get_db
from repositories.user_repository import UserRepository


class UserServicer(UserServiceServicer):
    def GetUser(self, request: UserId, context: ServicerContext) -> User:
        # get user ID from request
        user_id = request.id

        # get user data from database
        user_repository = UserRepository(next(get_db()))
        user = user_repository.get_user(user_id)

        # check if user exists in database
        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {user_id} not found.")
            return User()

        # return user data
        return User(
            user_id=UserId(id=user.id),
            username=user.username,
            email=user.email,
            display_name=user.display_name,
            avatar_url=None,
            connected_accounts=[UserConnection()],
            rooms=[RoomId(room.id) for room in user.rooms],
        )

    def Login(self, request: UserEmailPasswordLogin, context: ServicerContext) -> Empty:
        # TODO: check email format
        # TODO: ...... (implement login logic)

        # context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        # context.set_details('Method not implemented!')
        return Empty()

    def Logout(self, request: UserId, context: ServicerContext) -> Empty:
        # TODO: ...... (implement logout logic)
        return Empty()

    def Signup(self, request: User, context: ServicerContext) -> Empty:
        # TODO: ...... (implement signup logic)
        return Empty()

    def DeleteUser(self, request: UserId, context: ServicerContext) -> Empty:
        # TODO: ...... (implement delete user logic)
        return Empty()

    def UpdateUserProfile(
        self, request: UserProfile, context: ServicerContext
    ) -> Empty:
        # TODO: ...... (implement update user profile logic)
        return Empty()

    def GetUserRoomList(self, request: UserId, context: ServicerContext) -> RoomList:
        # TODO: ...... (implement get user room list logic)
        return RoomList()
