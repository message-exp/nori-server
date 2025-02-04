import pytest
import grpc
from unittest.mock import MagicMock
from typing import Generator, Tuple
from grpc import ServicerContext
from pytest_mock import MockerFixture

from src.api.room.room_service import RoomServicer,RoomMembers, Rooms
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from src.proto_generated.nori.v0.room.room_create_request_pb2 import RoomCreateRequest


@pytest.fixture
def mock_repositories(
    mocker: MockerFixture,
) -> Generator[Tuple[MagicMock, MagicMock, MagicMock], None, None]:
    """Mock UserRepository, RoomRepository, RoomMemberRepository"""
    mock_db_session = MagicMock()
    mocker.patch("src.api.room.room_service.get_db",
                 return_value=mock_db_session)

    mock_user_repo: MagicMock = mocker.patch(
        "src.api.room.room_service.UserRepository")
    mock_room_repo: MagicMock = mocker.patch(
        "src.api.room.room_service.RoomRepository")
    mock_room_member_repo: MagicMock = mocker.patch(
        "src.api.room.room_service.RoomMemberRepository"
    )

    mock_user_repo.return_value.get_user.return_value = MagicMock(
        display_name="Test User"
    )

    mock_room_repo.return_value.create_room.return_value = 123

    yield mock_user_repo, mock_room_repo, mock_room_member_repo


@pytest.fixture
def grpc_context() -> MagicMock:
    """Mock gRPC context"""
    context: MagicMock = MagicMock(spec=ServicerContext)
    context.set_code = MagicMock()
    context.set_details = MagicMock()
    return context


def test_create_room_success(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, mock_room_member_repo = mock_repositories
    servicer: RoomServicer = RoomServicer()

    request: RoomCreateRequest = RoomCreateRequest(
        user_id=UserId(user_id=1), name="Test Room"
    )

    response: RoomId = servicer.CreateRoom(request, grpc_context)

    assert isinstance(response, RoomId)
    assert response.room_id == 123

    mock_user_repo.return_value.get_user.assert_called_once_with(user_id=1)
    mock_room_repo.return_value.create_room.assert_called_once_with(
        Rooms(
            name="Test Room"
        )
    )
    mock_room_member_repo.return_value.create_room_member.assert_called_once_with(
        RoomMembers(
            room_id=123,
            user_id=1,
            user_name="Test User",
            room_name="Test Room",
        )
    )


def test_create_room_user_not_found(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, _, _ = mock_repositories
    servicer: RoomServicer = RoomServicer()

    mock_user_repo.return_value.get_user.return_value = None

    request: RoomCreateRequest = RoomCreateRequest(
        user_id=UserId(user_id=999), name="Test Room"
    )
    response: RoomId = servicer.CreateRoom(request, grpc_context)

    assert isinstance(response, RoomId)
    assert response.room_id == 0

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with(
        "User with ID 999 not found.")
