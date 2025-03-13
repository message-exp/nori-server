import grpc
import pytest
from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from typing import Generator, Tuple

from src.proto_generated.nori.v0.user.access.user_login_pb2 import (
    UserEmailPasswordLogin,
)
from src.proto_generated.nori.v0.user.access.token_pairs_pb2 import TokenPair

from src.utils.token_helper import generate_jwt_token
from src.api.user.user_access_service import UserAccessServicer
from mock_repo import grpc_context, mock_refresh_token_repo ,mock_repositories






@pytest.fixture
def fake_user() -> MagicMock:
    return MagicMock(
        id=1,
        username="user1",
        email="user@example.com",
        display_name="User One",
        rooms=[],
    )


def test_invalid_email(grpc_context: grpc.aio.ServicerContext) -> None:
    # Arrange: Create a fake request with invalid email
    request = UserEmailPasswordLogin(email="invalid", password="validpass")

    # Act: Call the Login method
    servicer = UserAccessServicer()
    response = servicer.Login(request, grpc_context)

    # Assert: Check the response
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.INVALID_ARGUMENT)
    grpc_context.set_details.assert_called_once_with("Invalid email format")
    assert isinstance(response, TokenPair)


def test_empty_password(grpc_context: grpc.aio.ServicerContext) -> None:
    # Arrange: Create a fake request with empty password
    request = UserEmailPasswordLogin(email="user@example.com", password="")

    # Act: Call the Login method
    service = UserAccessServicer()
    response = service.Login(request, grpc_context)

    # Assert: Check the response
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.INVALID_ARGUMENT)
    grpc_context.set_details.assert_called_once_with("Password cannot be empty")
    assert isinstance(response, TokenPair)


def test_user_not_found(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: grpc.aio.ServicerContext
) -> None:
    # Arrange: Create a fake request with a valid email and password
    request = UserEmailPasswordLogin(email="user@example.com", password="validpass")

    mocked_user_repo , _ , _= mock_repositories
    mocked_user_repo.return_value.get_user.return_value = None

    # Act: Call the Login method
    servicer = UserAccessServicer()
    response = servicer.Login(request, grpc_context)

    # Assert: Check the response
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("User not found")
    assert isinstance(response, TokenPair)


def test_successful_login(
    mocker: MockerFixture,
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock],
    mock_refresh_token_repo: MagicMock,
    grpc_context: grpc.aio.ServicerContext,
    fake_user: MagicMock,
) -> None:
    # Arrange: Create a fake request with a valid email and password
    request = UserEmailPasswordLogin(email="user@example.com", password="validpass")

    mocked_user_repo , _ , _ = mock_repositories
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
    servicer = UserAccessServicer()
    response = servicer.Login(request, grpc_context)

    # Assert: Check the response
    assert isinstance(response, TokenPair)
    assert response.access_token.access_token == "access123"
    assert response.refresh_token.refresh_token == "refresh123"
