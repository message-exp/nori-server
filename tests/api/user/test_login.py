import grpc
import pytest
from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from typing import Generator

from src.proto_generated.nori.v0.user.access.user_login_pb2 import (
    UserEmailPasswordLogin,
)
from src.proto_generated.nori.v0.user.access.token_pairs_pb2 import TokenPair

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

    mock_user_repo: MagicMock = mocker.patch("src.api.user.user_service.UserRepo")

    yield mock_user_repo


@pytest.fixture
def mock_refresh_token_repo(mocker: MockerFixture) -> Generator[MagicMock, None, None]:
    """Mock RefreshTokenRepository"""
    mock_db_session = MagicMock()
    mocker.patch("src.api.user.user_service.get_db", return_value=mock_db_session)

    mock_refresh_token_repo: MagicMock = mocker.patch(
        "src.api.user.user_service.RefreshTokenRepo"
    )

    yield mock_refresh_token_repo


@pytest.fixture
def fake_user() -> MagicMock:
    return MagicMock(
        id=1,
        username="user1",
        email="user@example.com",
        display_name="User One",
        rooms=[],
    )


def test_invalid_email(fake_context: grpc.aio.ServicerContext) -> None:
    # Arrange: Create a fake request with invalid email
    request = UserEmailPasswordLogin(email="invalid", password="validpass")

    # Act: Call the Login method
    servicer = UserServicer()
    response = servicer.Login(request, fake_context)

    # Assert: Check the response
    fake_context.set_code.assert_called_once_with(grpc.StatusCode.INVALID_ARGUMENT)
    fake_context.set_details.assert_called_once_with("Invalid email format")
    assert isinstance(response, TokenPair)


def test_empty_password(fake_context: grpc.aio.ServicerContext) -> None:
    # Arrange: Create a fake request with empty password
    request = UserEmailPasswordLogin(email="user@example.com", password="")

    # Act: Call the Login method
    service = UserServicer()
    response = service.Login(request, fake_context)

    # Assert: Check the response
    fake_context.set_code.assert_called_once_with(grpc.StatusCode.INVALID_ARGUMENT)
    fake_context.set_details.assert_called_once_with("Password cannot be empty")
    assert isinstance(response, TokenPair)


def test_user_not_found(
    mock_user_repo: MagicMock, fake_context: grpc.aio.ServicerContext
) -> None:
    # Arrange: Create a fake request with a valid email and password
    request = UserEmailPasswordLogin(email="user@example.com", password="validpass")

    mocked_user_repo = mock_user_repo
    mocked_user_repo.return_value.get_user.return_value = None

    # Act: Call the Login method
    servicer = UserServicer()
    response = servicer.Login(request, fake_context)

    # Assert: Check the response
    fake_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    fake_context.set_details.assert_called_once_with("User not found")
    assert isinstance(response, TokenPair)


def test_successful_login(
    mocker: MockerFixture,
    mock_user_repo: MagicMock,
    mock_refresh_token_repo: MagicMock,
    fake_context: grpc.aio.ServicerContext,
    fake_user: MagicMock,
) -> None:
    # Arrange: Create a fake request with a valid email and password
    request = UserEmailPasswordLogin(email="user@example.com", password="validpass")

    mocked_user_repo = mock_user_repo
    mocked_user_repo.return_value.get_user.return_value = fake_user

    mocked_refresh_token_repo = mock_refresh_token_repo
    mocked_refresh_token_repo.return_value.save_refresh_token.return_value = 1

    mocker.patch(
        "src.api.user.user_service.generate_refresh_token", return_value="refresh123"
    )
    mocker.patch(
        "src.api.user.user_service.generate_jwt_token", return_value="access123"
    )

    # Act: Call the Login method
    servicer = UserServicer()
    response = servicer.Login(request, fake_context)

    # Assert: Check the response
    assert isinstance(response, TokenPair)
    assert response.access_token.access_token == "access123"
    assert response.refresh_token.refresh_token == "refresh123"
