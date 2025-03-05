import grpc
import pytest
from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from types import SimpleNamespace
from typing import Generator

from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from src.proto_generated.nori.v0.room.general.room_list_pb2 import RoomList
from src.proto_generated.nori.v0.room.general.room_basic_info_response_pb2 import (
    RoomBasicInfoResponse,
)

from src.utils.token_helper import generate_jwt_token
from src.api.user.user_service import UserServicer


@pytest.fixture
def fake_context(mocker: MockerFixture) -> grpc.aio.ServicerContext:
    context: MagicMock = mocker.MagicMock(grpc.aio.ServicerContext)
    token = generate_jwt_token(subject="test")
    context.invocation_metadata.return_value = (("authorization", token),)
    return context


@pytest.fixture
def fake_room_member() -> SimpleNamespace:
    # Create a fake room member object with expected attributes for custom case
    fake_room = SimpleNamespace(
        name="Test Room",
        avatar_url="SharedUrl",
    )
    return SimpleNamespace(
        user_id=1,
        room_id=10,
        room=fake_room,
        room_name="Custom Room",
        room_avatar_url="CustomUrl",
    )


@pytest.fixture
def fake_room_member_shared() -> SimpleNamespace:
    # Create a fake room member object with empty custom values, so shared values are used
    fake_room = SimpleNamespace(
        name="Test Room Shared",
        avatar_url="SharedAvatarUrl",
    )
    return SimpleNamespace(
        user_id=2,
        room_id=20,
        room=fake_room,
        room_name="",  # empty custom name
        room_avatar_url="",  # empty custom avatar URL
    )


@pytest.fixture
def mock_room_member_repo(
    mocker: MockerFixture,
) -> Generator[MagicMock, None, None]:
    """Mock RoomMemberRepository"""
    mock_db_session = MagicMock()
    mocker.patch("src.api.user.user_service.get_db", return_value=mock_db_session)

    mock_room_member_repo: MagicMock = mocker.patch(
        "src.api.user.user_service.RoomMemberRepo"
    )

    yield mock_room_member_repo


def test_get_user_room_list_success(
    mock_room_member_repo: MagicMock,
    fake_context: grpc.aio.ServicerContext,
    fake_room_member: SimpleNamespace,
) -> None:
    # Arrange: setup fake request and patch RoomMemberRepository to return a fake room member with custom values
    user_id = fake_room_member.user_id
    request = UserId(id=user_id)
    fake_room_members = [fake_room_member]

    mock_room_member_repo.return_value.get_user_room_members.return_value = (
        fake_room_members
    )

    service = UserServicer()

    # Act
    response: RoomList = service.GetUserRoomList(request, fake_context)

    # Assert
    mock_room_member_repo.return_value.get_user_room_members.assert_called_once_with(
        user_id
    )
    assert len(response.rooms) == 1
    response_first: RoomBasicInfoResponse = response.rooms[0]

    # For oneof "name", the custom name is prioritized.
    assert response_first.WhichOneof("name") == "custom_name"
    assert response_first.custom_name == fake_room_member.room_name

    # For oneof "avatar_url", the custom avatar URL is prioritized.
    assert response_first.WhichOneof("avatar_url") == "custom_avatar_url"
    assert response_first.custom_avatar_url == fake_room_member.room_avatar_url


def test_get_user_room_list_success_shared_values(
    mock_room_member_repo: MagicMock,
    fake_context: grpc.aio.ServicerContext,
    fake_room_member_shared: SimpleNamespace,
) -> None:
    # Arrange: setup fake request and patch RoomMemberRepository to return a fake room member without custom values
    user_id = fake_room_member_shared.user_id
    request = UserId(id=user_id)
    fake_room_members = [fake_room_member_shared]

    mock_room_member_repo.return_value.get_user_room_members.return_value = (
        fake_room_members
    )

    service = UserServicer()

    # Act
    response: RoomList = service.GetUserRoomList(request, fake_context)

    # Assert
    mock_room_member_repo.return_value.get_user_room_members.assert_called_once_with(
        user_id
    )
    assert len(response.rooms) == 1
    response_first: RoomBasicInfoResponse = response.rooms[0]

    # For oneof "name", since custom value is empty, the shared name should be used.
    assert response_first.WhichOneof("name") == "shared_name"
    assert response_first.shared_name == fake_room_member_shared.room.name

    # For oneof "avatar_url", since custom value is empty, the shared avatar URL should be used.
    assert response_first.WhichOneof("avatar_url") == "shared_avatar_url"
    assert response_first.shared_avatar_url == fake_room_member_shared.room.avatar_url


def test_get_user_room_list_not_found(
    mock_room_member_repo: MagicMock, fake_context: grpc.aio.ServicerContext
) -> None:
    # Arrange: simulate no room members found
    user_id = 999
    request = UserId(id=user_id)

    mock_room_member_repo.return_value.get_user_room_members.return_value = None

    service = UserServicer()

    # Act
    response: RoomList = service.GetUserRoomList(request, fake_context)

    # Assert: context updated with error codes and response is empty
    fake_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    fake_context.set_details.assert_called_once_with(
        f"User with ID {user_id} has no associated rooms."
    )
    assert len(response.rooms) == 0
