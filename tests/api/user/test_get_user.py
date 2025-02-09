import grpc
import pytest
from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from types import SimpleNamespace
from typing import Generator

from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from src.proto_generated.nori.v0.user.user_pb2 import User

from src.utils.token_helper import generate_token
from src.api.user import user_service


@pytest.fixture
def fake_context(mocker: MockerFixture) -> grpc.aio.ServicerContext:
    context: MagicMock = mocker.MagicMock(grpc.aio.ServicerContext)
    token = generate_token(subject="test")
    context.invocation_metadata.return_value = (("authorization", token),)
    return context


@pytest.fixture
def fake_user_only_ids() -> SimpleNamespace:
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
def mock_user_repo(mocker: MockerFixture) -> Generator[MagicMock, None, None]:
    """Mock UserRepository"""
    mock_db_session = MagicMock()
    mocker.patch("src.api.user.user_service.get_db", return_value=mock_db_session)

    mock_user_repo: MagicMock = mocker.patch("src.api.user.user_service.UserRepo")

    yield mock_user_repo


# @pytest.fixture(autouse=True)
# def bypass_auth_required(monkeypatch: pytest.MonkeyPatch) -> None:
#     # Patch the auth_required decorator so future imports use our no‑op.
#     monkeypatch.setattr("src.utils.token_helper.auth_required", lambda f: f)

#     # Reload the user_service module so that the new decorator is applied.
#     importlib.reload(user_service)

#     # Unwrap already decorated methods.
#     for attr_name in dir(user_service.UserServicer):
#         attr = getattr(user_service.UserServicer, attr_name, None)
#         if callable(attr) and hasattr(attr, "__wrapped__"):
#             setattr(user_service.UserServicer, attr_name, attr.__wrapped__)


def test_get_user_success(
    mock_user_repo: MagicMock,
    fake_context: grpc.aio.ServicerContext,
    fake_user_only_ids: SimpleNamespace,
) -> None:
    # Arrange: Create a fake request with id=1
    request = UserId(id=fake_user_only_ids.id)

    # Set the return value for get_user_only_ids on the patched UserRepository
    mocked_user_repo = mock_user_repo
    mocked_user_repo.return_value.get_user_only_ids.return_value = fake_user_only_ids

    service = user_service.UserServicer()

    # Act: Call GetUser
    response = service.GetUser(request, fake_context)

    # Assert: Ensure the repository method was called once with the correct argument.
    mocked_user_repo.return_value.get_user_only_ids.assert_called_once_with(
        fake_user_only_ids.id
    )
    assert isinstance(response, User)
    assert response.user_id.id == fake_user_only_ids.id
    assert response.username == fake_user_only_ids.username
    assert response.email == fake_user_only_ids.email
    assert response.display_name == fake_user_only_ids.display_name
    assert response.avatar_url == ""
    # Check connected_accounts: our code always returns one empty UserConnection.
    assert len(response.connected_accounts) == 1
    # Check rooms: each room is converted to a RoomId with the same id.
    assert len(response.rooms) == len(fake_user_only_ids.rooms)
    for room_proto, room in zip(response.rooms, fake_user_only_ids.rooms):
        assert room_proto.id == room.id


def test_get_user_not_found(
    mock_user_repo: MagicMock,
    fake_context: grpc.aio.ServicerContext,
) -> None:
    # Arrange: Create a request for a non-existent user (e.g., id 999)
    user_id = 999
    request = UserId(id=user_id)

    # Patch the repository method to return None.
    mocked_user_repo = mock_user_repo
    mocked_user_repo.return_value.get_user_only_ids.return_value = None

    service = user_service.UserServicer()

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
