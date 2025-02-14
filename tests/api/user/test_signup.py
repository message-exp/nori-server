import grpc
import pytest
from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from typing import Generator

from src.proto_generated.nori.v0.user.signup_request_pb2 import SignUpRequest
# from src.proto_generated.nori.v0.user.user_pb2 import User
from src.proto_generated.nori.v0.user.token_pair_pb2 import TokenPair

from src.utils.token_helper import generate_jwt_token
from src.api.user.user_service import UserServicer


@pytest.fixture
def fake_context(mocker: MockerFixture) -> grpc.aio.ServicerContext:
    context: MagicMock = mocker.MagicMock(grpc.aio.ServicerContext)
    token = generate_jwt_token(subject="test")
    context.invocation_metadata.return_value = (("authorization", token),)
    return context


@pytest.fixture
def mock_user_repo(mocker: MockerFixture) -> Generator[MagicMock, None, None]:
    """Mock UserRepository"""
    mock_db_session = MagicMock()
    mocker.patch("src.api.user.user_service.get_db", return_value=mock_db_session)
    
    mock_user_repo = mocker.patch("src.api.user.user_service.UserRepo")
    
    yield mock_user_repo


@pytest.fixture
def mock_refresh_token_repo(mocker: MockerFixture) -> Generator[MagicMock, None, None]:
    """Mock RefreshTokenRepository"""
    mock_db_session = MagicMock()
    mocker.patch("src.api.user.user_service.get_db", return_value=mock_db_session)
    
    mock_refresh_token_repo = mocker.patch("src.api.user.user_service.RefreshTokenRepo")
    
    yield mock_refresh_token_repo


def test_invalid_email(fake_context: grpc.aio.ServicerContext) -> None:
    # Arrange: invalid email format
    request = SignUpRequest(username="user1", email="invalid", display_name="User One")
    servicer = UserServicer()

    # Act: call Signup
    response = servicer.Signup(request, fake_context)

    # Assert
    fake_context.set_code.assert_called_once_with(grpc.StatusCode.INVALID_ARGUMENT)
    fake_context.set_details.assert_called_once_with("Invalid email format")
    assert isinstance(response, TokenPair)


def test_email_already_exists(
    fake_context: grpc.aio.ServicerContext,
    mock_user_repo: MagicMock,
) -> None:
    # Arrange: valid email, but email exists
    request = SignUpRequest(
        username="newuser", email="user@example.com", display_name="New User"
    )
    instance = mock_user_repo.return_value
    instance.exists_user.side_effect = (
        lambda **kwargs: True if kwargs.get("email") else False
    )
    servicer = UserServicer()

    # Act: call Signup
    response = servicer.Signup(request, fake_context)

    # Assert
    fake_context.set_code.assert_called_once_with(grpc.StatusCode.ALREADY_EXISTS)
    fake_context.set_details.assert_called_once_with("Email already in use")
    assert isinstance(response, TokenPair)


def test_username_already_exists(
    fake_context: grpc.aio.ServicerContext,
    mock_user_repo: MagicMock,
) -> None:
    # Arrange: valid email and username; email not used but username exists
    request = SignUpRequest(
        username="existinguser", email="new@example.com", display_name="New User"
    )
    instance = mock_user_repo.return_value

    def exists_side_effect(**kwargs: str) -> bool:
        if kwargs.get("email"):
            return False
        if kwargs.get("username"):
            return True
        return False

    instance.exists_user.side_effect = exists_side_effect
    servicer = UserServicer()

    # Act: call Signup
    response = servicer.Signup(request, fake_context)

    # Assert
    fake_context.set_code.assert_called_once_with(grpc.StatusCode.ALREADY_EXISTS)
    fake_context.set_details.assert_called_once_with("Username already in use")
    assert isinstance(response, TokenPair)


def test_successful_signup(
    mocker: MockerFixture,
    fake_context: grpc.aio.ServicerContext,
    mock_user_repo: MagicMock,
    mock_refresh_token_repo: MagicMock,
) -> None:
    # Arrange: valid signup info
    request = SignUpRequest(username="user1", email="user@example.com", display_name="User One")
    user_repo_instance = mock_user_repo.return_value
    refresh_repo_instance = mock_refresh_token_repo.return_value

    # Simulate that neither email nor username exists, and creation returns new user id = 1
    user_repo_instance.exists_user.side_effect = lambda **kwargs: False
    user_repo_instance.create_user.return_value = 1
    refresh_repo_instance.save_refresh_token.return_value = 1

    # Patch token generators
    mocker.patch(
        "src.api.user.user_service.generate_refresh_token", return_value="refresh123"
    )
    mocker.patch(
        "src.api.user.user_service.generate_jwt_token", return_value="access123"
    )

    servicer = UserServicer()

    # Act: call Signup
    response = servicer.Signup(request, fake_context)

    # Assert
    assert response.access_token.access_token == b"access123"
    assert response.refresh_token.refresh_token == b"refresh123"
