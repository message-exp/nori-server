import grpc
from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from typing import Tuple

from src.proto_generated.nori.v0.user.account.signup_request_pb2 import SignUpRequest

# from src.proto_generated.nori.v0.user.user_pb2 import User
from src.proto_generated.nori.v0.user.access.token_pairs_pb2 import TokenPair

from src.api.user.user_account_service import UserAccountServicer
from mock_repo import grpc_context,mock_repositories



def test_invalid_email(grpc_context: grpc.aio.ServicerContext) -> None:
    # Arrange: invalid email format
    request = SignUpRequest(username="user1", email="invalid", display_name="User One")
    servicer = UserAccountServicer()

    # Act: call Signup
    response = servicer.Signup(request, grpc_context)

    # Assert
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.INVALID_ARGUMENT)
    grpc_context.set_details.assert_called_once_with("Invalid email format")
    assert isinstance(response, TokenPair)


def test_email_already_exists(
    grpc_context: grpc.aio.ServicerContext,
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock,MagicMock],
) -> None:
    # Arrange: valid email, but email exists
    request = SignUpRequest(
        username="newuser", email="user@example.com", display_name="New User"
    )
    mock_user_repo, _, _ , _= mock_repositories
    instance = mock_user_repo.return_value
    instance.exists_user.side_effect = (
        lambda **kwargs: True if kwargs.get("email") else False
    )
    servicer = UserAccountServicer()

    # Act: call Signup
    response = servicer.Signup(request, grpc_context)

    # Assert
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.ALREADY_EXISTS)
    grpc_context.set_details.assert_called_once_with("Email already in use")
    assert isinstance(response, TokenPair)


def test_username_already_exists(
    grpc_context: grpc.aio.ServicerContext,
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock , MagicMock],
) -> None:
    # Arrange: valid email and username; email not used but username exists
    request = SignUpRequest(
        username="existinguser", email="new@example.com", display_name="New User"
    )
    mock_user_repo, _, _ , _ = mock_repositories
    instance = mock_user_repo.return_value

    def exists_side_effect(**kwargs: str) -> bool:
        if kwargs.get("email"):
            return False
        if kwargs.get("username"):
            return True
        return False

    instance.exists_user.side_effect = exists_side_effect
    servicer = UserAccountServicer()

    # Act: call Signup
    response = servicer.Signup(request, grpc_context)

    # Assert
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.ALREADY_EXISTS)
    grpc_context.set_details.assert_called_once_with("Username already in use")
    assert isinstance(response, TokenPair)


def test_successful_signup(
    mocker: MockerFixture,
    grpc_context: grpc.aio.ServicerContext,
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock , MagicMock]
) -> None:
    # Arrange: valid signup info
    request = SignUpRequest(
        username="user1", email="user@example.com", display_name="User One"
    )
    mock_user_repo, _, _ , mock_refresh_token_repo = mock_repositories
    user_repo_instance = mock_user_repo.return_value
    refresh_repo_instance = mock_refresh_token_repo.return_value

    # Simulate that neither email nor username exists, and creation returns new user id = 1
    user_repo_instance.exists_user.side_effect = lambda **kwargs: False
    user_repo_instance.create_user.return_value = 1
    refresh_repo_instance.save_refresh_token.return_value = 1

    # Patch token generators
    mocker.patch(
        "src.api.user.user_account_service.generate_refresh_token", return_value="refresh123"
    )
    mocker.patch(
        "src.api.user.user_account_service.generate_jwt_token", return_value="access123"
    )

    servicer = UserAccountServicer()

    # Act: call Signup
    response = servicer.Signup(request, grpc_context)

    # Assert
    assert response.access_token.access_token == "access123"
    assert response.refresh_token.refresh_token == "refresh123"
