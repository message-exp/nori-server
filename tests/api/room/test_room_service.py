import pytest
import grpc
from unittest.mock import MagicMock
from typing import Generator, Tuple
from grpc import ServicerContext
from pytest_mock import MockerFixture

from src.proto_generated.nori.v0.room.general.room_basic_info_response_pb2 import (
    RoomBasicInfoResponse,
)
from src.proto_generated.nori.v0.room.room_pb2 import Room
from src.proto_generated.nori.v0.room.room_user_request_pb2 import RoomUserRequest
from src.utils.token_helper import generate_jwt_token
from src.api.room.room_service import RoomServicer, RoomMembers, Rooms
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from src.proto_generated.nori.v0.room.general.room_create_request_pb2 import (
    RoomCreateRequest,
)
from src.proto_generated.nori.v0.room.member.invite_user_to_room_request_pb2 import (
    InviteUserToRoomRequest,
)
from src.proto_generated.nori.v0.room.member.room_member_pb2 import RoomMemberStatus
from google.protobuf.empty_pb2 import Empty


@pytest.fixture
def mock_repositories(
    mocker: MockerFixture,
) -> Generator[Tuple[MagicMock, MagicMock, MagicMock], None, None]:
    """Mock UserRepository, RoomRepository, RoomMemberRepository"""
    mock_db_session = MagicMock()
    mocker.patch("src.api.room.room_service.get_db", return_value=mock_db_session)

    mock_user_repo: MagicMock = mocker.patch("src.api.room.room_service.UserRepo")
    mock_room_repo: MagicMock = mocker.patch("src.api.room.room_service.RoomRepo")
    mock_room_member_repo: MagicMock = mocker.patch(
        "src.api.room.room_service.RoomMemberRepo"
    )

    yield mock_user_repo, mock_room_repo, mock_room_member_repo


@pytest.fixture
def grpc_context() -> MagicMock:
    """Mock gRPC context with valid authorization metadata"""
    context: MagicMock = MagicMock(spec=ServicerContext)
    token = generate_jwt_token(subject="test")
    context.invocation_metadata.return_value = (("authorization", token),)
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
    grpc_context.set_details.assert_called_once_with("User with ID 2 not found.")
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
        "Users with some IDs in [3] not found."
    )
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
        room_id=RoomId(id=1),
        inviter=UserId(id=2),
        invitees=[UserId(id=3), UserId(id=4)],
    )
    response = service.InviteToRoom(request, grpc_context)

    mock_room_member_repo.return_value.create_room_members.assert_called_once_with(
        1, [3, 4]
    )
    assert isinstance(response, Empty)


def test_join_room_success(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, mock_room_member_repo = mock_repositories
    room_service = RoomServicer()

    mock_room_repo.return_value.exists_room.return_value = True
    mock_user_repo.return_value.exists_user.return_value = True

    request = RoomUserRequest(room_id=RoomId(id=123), user_id=UserId(id=1))
    response = room_service.JoinRoom(request, grpc_context)

    mock_room_member_repo.return_value.create_room_member.assert_called_once_with(
        RoomMembers(room_id=123, user_id=1)
    )

    assert isinstance(response, Empty)


def test_join_room_room_not_found(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    _, mock_room_repo, _ = mock_repositories
    room_service = RoomServicer()

    mock_room_repo.return_value.exists_room.return_value = False

    request = RoomUserRequest(room_id=RoomId(id=999), user_id=UserId(id=1))
    response = room_service.JoinRoom(request, grpc_context)

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("Room with ID 999 not found.")
    assert isinstance(response, Empty)


def test_join_room_user_not_found(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, _ = mock_repositories
    room_service = RoomServicer()

    mock_room_repo.return_value.exists_room.return_value = True
    mock_user_repo.return_value.exists_user.return_value = False

    request = RoomUserRequest(room_id=RoomId(id=123), user_id=UserId(id=1))
    response = room_service.JoinRoom(request, grpc_context)

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("User with ID 1 not found.")
    assert isinstance(response, Empty)


def test_get_room_success(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    _, mock_room_repo, _ = mock_repositories
    mock_room = MagicMock()
    mock_room.id = 123
    mock_room.name = "Test Room"
    mock_room.avatar_url = "https://example.com/avatar.png"
    mock_room.members = [
        MagicMock(user_id=999, user_name="User One"),
        MagicMock(user_id=998, user_name="User Two"),
    ]
    mock_room_repo.return_value.get_room.return_value = mock_room

    room_service = RoomServicer()
    request = RoomId(id=123)
    response = room_service.GetRoom(request, grpc_context)

    assert isinstance(response, Room)
    assert response.room_id.id == 123
    assert response.shared_name == "Test Room"
    assert response.shared_avatar_url == "https://example.com/avatar.png"
    assert len(response.members) == 2
    assert response.members[0].user_id.id == 999
    assert response.members[0].room_nickname == "User One"
    assert response.members[0].status == RoomMemberStatus.JOINED
    assert response.members[1].user_id.id == 998
    assert response.members[1].room_nickname == "User Two"
    assert response.members[1].status == RoomMemberStatus.JOINED


def test_get_room_not_found(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    _, mock_room_repo, _ = mock_repositories
    mock_room_repo.return_value.get_room.return_value = None

    room_service = RoomServicer()
    request = RoomId(id=1)
    response = room_service.GetRoom(request, grpc_context)

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("Room with ID 1 not found.")
    assert isinstance(response, Empty)


def test_get_room_basic_info_success(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, mock_room_member_repo = mock_repositories
    room_service = RoomServicer()

    mock_user_repo.return_value.exists_user.return_value = True
    mock_room_repo.return_value.get_room.return_value = Rooms(id=123, name="Test Room")
    mock_room_member_repo.return_value.get_single_user_room_member.return_value = (
        RoomMembers(
            room_id=123,
            user_id=1,
            room_name="Custom Room Name",
            room_avatar_url="Custom Avatar URL",
        )
    )

    request = RoomUserRequest(room_id=RoomId(id=123), user_id=UserId(id=1))
    response = room_service.GetRoomBasic(request, grpc_context)

    assert isinstance(response, RoomBasicInfoResponse)
    assert response.room_id.id == 123
    assert response.custom_name == "Custom Room Name"
    assert response.custom_avatar_url == "Custom Avatar URL"
    assert response.shared_name == ""
    assert response.shared_avatar_url == ""


def test_get_room_basic_info_user_not_found(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, _, _ = mock_repositories
    room_service = RoomServicer()

    mock_user_repo.return_value.exists_user.return_value = False

    request = RoomUserRequest(room_id=RoomId(id=123), user_id=UserId(id=1))
    response = room_service.GetRoomBasic(request, grpc_context)

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("User with ID 1 not found.")
    assert isinstance(response, Empty)


def test_get_room_basic_info_room_not_found(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, _ = mock_repositories
    room_service = RoomServicer()

    mock_user_repo.return_value.exists_user.return_value = True
    mock_room_repo.return_value.get_room.return_value = None

    request = RoomUserRequest(room_id=RoomId(id=123), user_id=UserId(id=1))
    response = room_service.GetRoomBasic(request, grpc_context)

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("Room with ID 123 not found.")
    assert isinstance(response, Empty)


def test_get_room_basic_info_user_not_in_room(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, mock_room_member_repo = mock_repositories
    room_service = RoomServicer()

    mock_user_repo.return_value.exists_user.return_value = True
    mock_room_repo.return_value.get_room.return_value = Rooms(id=123)
    mock_room_member_repo.return_value.get_single_user_room_member.return_value = None

    request = RoomUserRequest(room_id=RoomId(id=123), user_id=UserId(id=1))
    response = room_service.GetRoomBasic(request, grpc_context)

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with(
        "User with ID 1 not found in Room with ID 123"
    )
    assert isinstance(response, Empty)
