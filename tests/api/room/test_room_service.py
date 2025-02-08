import pytest
import grpc
from unittest.mock import MagicMock
from typing import Generator, Tuple
from grpc import ServicerContext
from pytest_mock import MockerFixture

from src.api.room.room_service import RoomServicer, RoomMembers, Rooms
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from src.proto_generated.nori.v0.room.room_create_request_pb2 import RoomCreateRequest
from src.proto_generated.nori.v0.room.invite_user_to_room_request_pb2 import InviteUserToRoomRequest
from google.protobuf.empty_pb2 import Empty


@pytest.fixture
def mock_repositories(
    mocker: MockerFixture,
) -> Generator[Tuple[MagicMock, MagicMock, MagicMock], None, None]:
    """Mock UserRepository, RoomRepository, RoomMemberRepository"""
    mock_db_session = MagicMock()
    mocker.patch("src.api.room.room_service.get_db",
                 return_value=mock_db_session)

    mock_user_repo: MagicMock = mocker.patch(
        "src.api.room.room_service.UserRepo")
    mock_room_repo: MagicMock = mocker.patch(
        "src.api.room.room_service.RoomRepo")
    mock_room_member_repo: MagicMock = mocker.patch(
        "src.api.room.room_service.RoomMemberRepo"
    )

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
    mock_user_repo.return_value.get_user.return_value = MagicMock(
        display_name="Test User"
    )
    mock_room_repo.return_value.create_room.return_value = 123

    servicer: RoomServicer = RoomServicer()
    request: RoomCreateRequest = RoomCreateRequest(
        creator=UserId(id=1), name="Test Room"
    )
    response: RoomId = servicer.CreateRoom(request, grpc_context)

    assert isinstance(response, RoomId)
    assert response.id == 123
    mock_user_repo.return_value.get_user.assert_called_once_with(1)
    mock_room_repo.return_value.create_room.assert_called_once_with(
        Rooms(name="Test Room")
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
    mock_user_repo.return_value.get_user.return_value = None

    servicer: RoomServicer = RoomServicer()
    request: RoomCreateRequest = RoomCreateRequest(
        creator=UserId(id=999), name="Test Room"
    )
    response: RoomId = servicer.CreateRoom(request, grpc_context)

    assert isinstance(response, RoomId)
    assert response.id == 0
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("User with ID 999 not found.")


def test_invite_to_room_room_not_found(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    _, mock_room_repo, _ = mock_repositories
    mock_room_repo.return_value.exists_room.return_value = False

    service = RoomServicer()
    request = InviteUserToRoomRequest(
        room_id=RoomId(id=1), inviter=UserId(id=2), invitees=[UserId(id=3)]
    )
    response = service.InviteToRoom(request, grpc_context)

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("Room with ID 1 not found.")
    assert isinstance(response, Empty)


def test_invite_to_room_inviter_not_found(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, _ = mock_repositories
    mock_room_repo.return_value.exists_room.return_value = True
    mock_user_repo.return_value.exists_user.return_value = False

    service = RoomServicer()
    request = InviteUserToRoomRequest(
        room_id=RoomId(id=1), inviter=UserId(id=2), invitees=[UserId(id=3)]
    )
    response = service.InviteToRoom(request, grpc_context)

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with(
        "User with ID 2 not found.")
    assert isinstance(response, Empty)


def test_invite_to_room_invitees_not_found(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, _ = mock_repositories
    mock_room_repo.return_value.exists_room.return_value = True
    mock_user_repo.return_value.exists_user.return_value = True
    mock_user_repo.return_value.exists_all_users.return_value = False

    service = RoomServicer()
    request = InviteUserToRoomRequest(
        room_id=RoomId(id=1), inviter=UserId(id=2), invitees=[UserId(id=3)]
    )
    response = service.InviteToRoom(request, grpc_context)

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with(
        "Users with some IDs in [3] not found.")
    assert isinstance(response, Empty)


def test_invite_to_room_success(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, mock_room_member_repo = mock_repositories
    mock_room_repo.return_value.exists_room.return_value = True
    mock_user_repo.return_value.exists_user.return_value = True
    mock_user_repo.return_value.exists_all_users.return_value = True
    mock_room_member_repo.return_value.create_room_members.return_value = None

    service = RoomServicer()
    request = InviteUserToRoomRequest(
        room_id=RoomId(id=1), inviter=UserId(id=2), invitees=[UserId(id=3), UserId(id=4)]
    )
    response = service.InviteToRoom(request, grpc_context)

    mock_room_member_repo.return_value.create_room_members.assert_called_once_with(1, [3, 4])
    assert isinstance(response, Empty)
