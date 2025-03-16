import grpc
from unittest.mock import MagicMock
from typing import Tuple
from src.proto_generated.nori.v0.room.room_pb2 import Room
from src.api.room.room_general_service import RoomGeneralServicer
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.room.member.room_member_pb2 import RoomMemberStatus
from google.protobuf.empty_pb2 import Empty


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

    room_service = RoomGeneralServicer()
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

    room_service = RoomGeneralServicer()
    request = RoomId(id=1)
    response = room_service.GetRoom(request, grpc_context)

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("Room with ID 1 not found.")
    assert isinstance(response, Empty)
