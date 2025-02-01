from grpc.aio import Server, ServicerContext

from google.protobuf.empty_pb2 import Empty
from proto_generated.nori.v0.user.user_pb2 import User
from proto_generated.nori.v0.user.user_login_pb2 import UserEmailPasswordLogin
from proto_generated.nori.v0.user.user_id_pb2 import UserId
from proto_generated.nori.v0.user.user_profile_pb2 import UserProfile
from proto_generated.nori.v0.room.room_list_pb2 import RoomList

from proto_generated.nori.v0.user.user_service_pb2_grpc import (
    UserServiceServicer,
    add_UserServiceServicer_to_server,
)


class UserServicer(UserServiceServicer):
    service_namespace = "nori.v0.UserService"
    auth_config: dict[str, bool] = dict()

    auth_config[f"/{service_namespace}/GetUser"] = True

    def GetUser(self, request: UserId, context: ServicerContext) -> User:
        # TODO: check user_id format
        # TODO: get user data from database
        # TODO: return user data
        return User()

    auth_config[f"/{service_namespace}/Login"] = False

    def Login(self, request: UserEmailPasswordLogin, context: ServicerContext) -> Empty:
        # TODO: check email format
        # TODO: ...... (implement login logic)

        # context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        # context.set_details('Method not implemented!')
        return Empty()

    auth_config[f"/{service_namespace}/Logout"] = True

    def Logout(self, request: UserId, context: ServicerContext) -> Empty:
        # TODO: ...... (implement logout logic)
        return Empty()

    auth_config[f"/{service_namespace}/Signup"] = False

    def Signup(self, request: User, context: ServicerContext) -> Empty:
        # TODO: ...... (implement signup logic)
        return Empty()

    auth_config[f"/{service_namespace}/DeleteUser"] = True

    def DeleteUser(self, request: UserId, context: ServicerContext) -> Empty:
        # TODO: ...... (implement delete user logic)
        return Empty()

    auth_config[f"/{service_namespace}/UpdateUserProfile"] = True

    def UpdateUserProfile(
        self, request: UserProfile, context: ServicerContext
    ) -> Empty:
        # TODO: ...... (implement update user profile logic)
        return Empty()

    auth_config[f"/{service_namespace}/GetUserRoomList"] = True

    def GetUserRoomList(self, request: UserId, context: ServicerContext) -> RoomList:
        # TODO: ...... (implement get user room list logic)
        return RoomList()


def add_service_to_server(server: Server) -> None:
    add_UserServiceServicer_to_server(UserServicer(), server)
