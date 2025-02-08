import grpc
import pytest
from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from types import SimpleNamespace
from typing import Generator

from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from src.proto_generated.nori.v0.user.user_pb2 import User

# from src.model import Users, Rooms
from src.api.user.user_service import UserServicer


@pytest.fixture
def fake_context(mocker: MockerFixture) -> grpc.aio.ServicerContext:
    return mocker.MagicMock(spec=grpc.aio.ServicerContext)


@pytest.fixture
def fake_user() -> SimpleNamespace:
    # Create a fake user object with attributes expected by GetUser
    fake_room = SimpleNamespace(id=100)
    return SimpleNamespace(
        id=1,
        username="testuser",
        display_name="Test User",
        email="test@example.com",
        rooms=[fake_room],
    )


@pytest.fixture
def mock_user_repository(mocker: MockerFixture) -> Generator[MagicMock, None, None]:
    """Mock UserRepository"""
    mock_db_session = MagicMock()
    mocker.patch("src.api.user.user_service.get_db", return_value=mock_db_session)

    mock_user_repo: MagicMock = mocker.patch("src.api.user.user_service.UserRepository")

    yield mock_user_repo


def test_get_user_success(
    mock_user_repository: MagicMock,
    fake_context: grpc.aio.ServicerContext,
    fake_user: SimpleNamespace,
) -> None:
    # Arrange: Create a fake request with id=1
    request = UserId(id=fake_user.id)

    # Set the return value for get_user_only_ids on the patched UserRepository
    mock_user_repository.return_value.get_user_only_ids.return_value = fake_user

    service = UserServicer()

    # Act: Call GetUser
    response = service.GetUser(request, fake_context)

    # Assert: Ensure the repository method was called once with the correct argument.
    mock_user_repository.return_value.get_user_only_ids.assert_called_once_with(
        fake_user.id
    )
    assert isinstance(response, User)
    assert response.user_id.id == fake_user.id
    assert response.username == fake_user.username
    assert response.email == fake_user.email
    assert response.display_name == fake_user.display_name
    assert response.avatar_url == ""
    # Check connected_accounts: our code always returns one empty UserConnection.
    assert len(response.connected_accounts) == 1
    # Check rooms: each room is converted to a RoomId with the same id.
    assert len(response.rooms) == len(fake_user.rooms)
    for room_proto, room in zip(response.rooms, fake_user.rooms):
        assert room_proto.id == room.id


def test_get_user_not_found(
    mock_user_repository: MagicMock,
    fake_context: grpc.aio.ServicerContext,
) -> None:
    # Arrange: Create a request for a non-existent user (e.g., id 999)
    user_id = 999
    request = UserId(id=user_id)

    # Patch the repository method to return None.
    mock_user_repository.return_value.get_user_only_ids.return_value = None

    service = UserServicer()

    # Act: Call GetUser
    response = service.GetUser(request, fake_context)

    # Assert: Verify that context was updated with NOT_FOUND status.
    fake_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    fake_context.set_details.assert_called_once_with(
        f"User with ID {user_id} not found."
    )

    # Assert that the returned response is an empty User message.
    assert response.user_id.id == 0
    assert response.username == ""
    assert response.email == ""
    assert response.display_name == ""
    # Default empty message for avatar_url can be an empty string.
    assert response.avatar_url == ""
    assert len(response.connected_accounts) == 0
    assert len(response.rooms) == 0
