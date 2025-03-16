import grpc
from unittest.mock import MagicMock
from typing import  Tuple
from src.api.room.room_general_service import RoomGeneralServicer, RoomMembers, Rooms
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from src.proto_generated.nori.v0.room.general.room_create_request_pb2 import (
    RoomCreateRequest,
)
from tests.api.room.room_general.mock_repo import grpc_context, mock_repositories
def test_create_room_success(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, mock_room_member_repo = mock_repositories
    mock_user_repo.return_value.get_user.return_value = MagicMock(
        display_name="Test User"
    )
    mock_room_repo.return_value.create_room.return_value = 123

    servicer: RoomGeneralServicer = RoomGeneralServicer()
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

    servicer: RoomGeneralServicer = RoomGeneralServicer()
    request: RoomCreateRequest = RoomCreateRequest(
        creator=UserId(id=999), name="Test Room"
    )
    response: RoomId = servicer.CreateRoom(request, grpc_context)

    assert isinstance(response, RoomId)
    assert response.id == 0
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("User with ID 999 not found.")

