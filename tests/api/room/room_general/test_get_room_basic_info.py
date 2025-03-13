import grpc
from unittest.mock import MagicMock
from typing import  Tuple

from src.proto_generated.nori.v0.room.general.room_basic_info_response_pb2 import (
    RoomBasicInfoResponse,
)
from src.proto_generated.nori.v0.room.room_user_request_pb2 import RoomUserRequest
from src.api.room.room_general_service import RoomGeneralServicer, RoomMembers, Rooms
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from google.protobuf.empty_pb2 import Empty
from mock_repo import grpc_context, mock_repositories
def test_get_room_basic_info_success(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, mock_room_member_repo = mock_repositories
    room_service = RoomGeneralServicer()

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
    room_service = RoomGeneralServicer()

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
    room_service = RoomGeneralServicer()

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
    room_service = RoomGeneralServicer()

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
