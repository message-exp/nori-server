import grpc
from unittest.mock import MagicMock
from typing import Tuple


from src.api.room.room_member_service import RoomMemberServicer
from src.api.room.room_member_service import RoomMembers
from src.proto_generated.nori.v0.room.room_user_request_pb2 import RoomUserRequest
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from google.protobuf.empty_pb2 import Empty


def test_join_room_success(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, mock_room_member_repo = mock_repositories
    room_service = RoomMemberServicer()

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
    room_service = RoomMemberServicer()

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
    room_service = RoomMemberServicer()

    mock_room_repo.return_value.exists_room.return_value = True
    mock_user_repo.return_value.exists_user.return_value = False

    request = RoomUserRequest(room_id=RoomId(id=123), user_id=UserId(id=1))
    response = room_service.JoinRoom(request, grpc_context)

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("User with ID 1 not found.")
    assert isinstance(response, Empty)
