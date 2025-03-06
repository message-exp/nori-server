import grpc
from grpc.aio import ServicerContext

from utils.token_helper import auth_required, generate_jwt_token, generate_refresh_token
from utils.validate_format_helper import is_valid_email
from utils.db_helper import get_db

from google.protobuf.empty_pb2 import Empty
from proto_generated.nori.v0.user.access.user_login_pb2 import UserEmailPasswordLogin
from proto_generated.nori.v0.user.user_id_pb2 import UserId
from proto_generated.nori.v0.user.access.token_pairs_pb2 import (
    UserTokenPair,
    UserRefreshToken,
)
from proto_generated.nori.v0.user.access.access_token_pb2 import AccessToken
from proto_generated.nori.v0.user.access.refresh_token_pb2 import RefreshToken
from proto_generated.nori.v0.user.access.user_reset_password_request_pb2 import (
    UserResetPasswordRequest,
)

from proto_generated.nori.v0.user.access.user_access_service_pb2_grpc import (
    UserAccessServiceServicer,
)

from model import RefreshToken as DBRefreshToken
from repositories import UserRepo, RefreshTokenRepo


class UserServicer(UserAccessServiceServicer):
    def Login(
        self, request: UserEmailPasswordLogin, context: ServicerContext
    ) -> UserTokenPair:
        # TODO: response type has changed
        email = request.email
        password = request.password

        # check email format
        if not is_valid_email(email):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid email format")
            return UserTokenPair()

        # check password format
        if not password:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Password cannot be empty")
            return UserTokenPair()

        # get user from database
        user_repo = UserRepo(next(get_db()))
        user = user_repo.get_user(email=email)

        # check if user exists
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return UserTokenPair()

        # create refresh token and save in database
        refresh_token = generate_refresh_token()
        refresh_token_db_obj = DBRefreshToken(
            user_id=user.id, refresh_token=refresh_token
        )
        refresh_token_repo = RefreshTokenRepo(next(get_db()))
        refresh_token_repo.save_refresh_token(refresh_token_db_obj)

        # create access token
        access_token = generate_jwt_token(subject=user.id)

        # return tokens
        return UserTokenPair(
            user_id=UserId(id=user.id),
            access_token=AccessToken(access_token=access_token),
            refresh_token=RefreshToken(refresh_token=refresh_token),
        )

    @auth_required
    def Logout(self, request: UserTokenPair, context: ServicerContext) -> Empty:
        # TODO: ...... (implement logout logic)
        return Empty()

    @auth_required
    def RefreshUserToken(
        self, request: UserRefreshToken, context: ServicerContext
    ) -> AccessToken:
        # TODO: ...... (implement login logic)
        return AccessToken()

    @auth_required
    def ResetUserPassword(
        self, request: UserResetPasswordRequest, context: ServicerContext
    ) -> Empty:
        # TODO: ...... (implement login logic)
        return Empty()
