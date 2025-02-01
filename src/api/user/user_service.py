import grpc
from grpc.aio import Server, ServicerContext

# from api.utils.auth import get_token, generate_token
# from api.utils.grpc_exception import GrpcException

from google.protobuf.empty_pb2 import Empty
from proto_generated.nori.v0.user.user_pb2 import User
from proto_generated.nori.v0.user.user_login_pb2 import UserEmailPasswordLogin
from proto_generated.nori.v0.user.user_id_pb2 import UserId
from proto_generated.nori.v0.user.user_profile_pb2 import UserProfile
from proto_generated.nori.v0.room.room_list_pb2 import RoomList

from proto_generated.nori.v0.user.user_service_pb2_grpc import UserServiceServicer, add_UserServiceServicer_to_server

class UserServicer(UserServiceServicer):
    service_namespace = "nori.v0.UserService"
    auth_list = {
        f"/{service_namespace}/GetUser": True,
        f"/{service_namespace}/Login": False,
        f"/{service_namespace}/Logout": True,
        f"/{service_namespace}/Signup": False,
        f"/{service_namespace}/DeleteUser": True,
        f"/{service_namespace}/UpdateUserProfile": True,
        f"/{service_namespace}/GetUserRoomList": True,
    }

    def GetUser(self, request: UserId, context: ServicerContext) -> User:
        # TODO: check user_id format
        # TODO: get user data from database
        # TODO: return user data
        return User()

    def Login(self, request: UserEmailPasswordLogin, context: ServicerContext) -> Empty:
        """Login with email and password.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Logout(self, request: UserId, context: ServicerContext) -> Empty:
        """Authentication: Required. Log out the user.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Signup(self, request: User, context: ServicerContext) -> Empty:
        """Authentication: Not required. Sign up a new user.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteUser(self, request: UserId, context: ServicerContext) -> Empty:
        """Authentication: Required. Delete a user.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateUserProfile(self, request: UserProfile, context: ServicerContext) -> Empty:
        """Authentication: Required. Update user profile information.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserRoomList(self, request: UserId, context: ServicerContext) -> RoomList:
        """Authentication: Required. Get user room list.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')
    
def add_service_to_server(server: Server) -> None:
    add_UserServiceServicer_to_server(UserServicer(), server)
