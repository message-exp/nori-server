import grpc
from grpc.aio import ServicerContext

from utils.token_helper import auth_required, generate_jwt_token, generate_refresh_token
from utils.validate_format_helper import is_valid_email
from utils.db_helper import get_db

from google.protobuf.empty_pb2 import Empty
from proto_generated.nori.v0.user.user_id_pb2 import UserId
from proto_generated.nori.v0.user.account.user_pb2 import User
from proto_generated.nori.v0.user.account.signup_request_pb2 import SignUpRequest
from proto_generated.nori.v0.user.account.user_profile_update_request_pb2 import (
    UserProfileUpdateRequest,
)
from proto_generated.nori.v0.user.access.token_pairs_pb2 import UserTokenPair
from proto_generated.nori.v0.user.access.access_token_pb2 import AccessToken
from proto_generated.nori.v0.user.access.refresh_token_pb2 import RefreshToken
from proto_generated.nori.v0.user.network.user_connection_pb2 import UserConnection
from proto_generated.nori.v0.room.room_id_pb2 import RoomId

from proto_generated.nori.v0.user.account.user_account_service_pb2_grpc import (
    UserAccountServiceServicer,
)

from model import RefreshToken as DBRefreshToken, Users
from repositories import UserRepo, RefreshTokenRepo


class UserAccountServicer(UserAccountServiceServicer):    
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
    

    def Signup(self, request: SignUpRequest, context: ServicerContext) -> UserTokenPair:
        # TODO: request and response type has changed
        # get request content
        username = request.username
        email = request.email
        display_name = request.display_name

        # check email format
        if not is_valid_email(email):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid email format")
            return UserTokenPair()

        # check if email already exists
        user_repo = UserRepo(next(get_db()))
        if user_repo.exists_user(email=email):
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Email already in use")
            return UserTokenPair()

        # check if username already exists
        if user_repo.exists_user(username=username):
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Username already in use")
            return UserTokenPair()

        # create user object
        try:
            new_user_id = user_repo.create_user(
                Users(username=username, email=email, display_name=display_name)
            )
        except Exception:  # catch exceptions
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to create user")
            return UserTokenPair()

        # create refresh tokens
        refresh_token = generate_refresh_token()
        refresh_token_db_obj = DBRefreshToken(
            user_id=new_user_id, refresh_token=refresh_token
        )
        refresh_token_repo = RefreshTokenRepo(next(get_db()))
        refresh_token_repo.save_refresh_token(refresh_token_db_obj)

        # create access token
        access_token = generate_jwt_token(subject=new_user_id)

        return UserTokenPair(
            user_id=UserId(id=new_user_id),
            access_token=AccessToken(access_token=access_token),
            refresh_token=RefreshToken(refresh_token=refresh_token),
        )

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
