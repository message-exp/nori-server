import grpc
from unittest.mock import MagicMock
from typing import Tuple


from src.api.room.room_member_service import RoomMemberServicer
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.user.user_id_pb2 import UserId

from src.proto_generated.nori.v0.room.member.invite_user_to_room_request_pb2 import (
    InviteUserToRoomRequest,
)
from google.protobuf.empty_pb2 import Empty


def test_invite_to_room_room_not_found(
    mock_repositories_for_room_member: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    _, mock_room_repo, _ = mock_repositories_for_room_member
    mock_room_repo.return_value.exists_room.return_value = False

    service = RoomMemberServicer()
    request = InviteUserToRoomRequest(
        room_id=RoomId(id=1), inviter=UserId(id=2), invitees=[UserId(id=3)]
    )
    response = service.InviteToRoom(request, grpc_context)

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("Room with ID 1 not found.")
    assert isinstance(response, Empty)


def test_invite_to_room_inviter_not_found(
    mock_repositories_for_room_member: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, _ = mock_repositories_for_room_member
    mock_room_repo.return_value.exists_room.return_value = True
    mock_user_repo.return_value.exists_user.return_value = False

    service = RoomMemberServicer()
    request = InviteUserToRoomRequest(
        room_id=RoomId(id=1), inviter=UserId(id=2), invitees=[UserId(id=3)]
    )
    response = service.InviteToRoom(request, grpc_context)

    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("User with ID 2 not found.")
    assert isinstance(response, Empty)


def test_invite_to_room_invitees_not_found(
    mock_repositories_for_room_member: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, _ = mock_repositories_for_room_member
    mock_room_repo.return_value.exists_room.return_value = True
    mock_user_repo.return_value.exists_user.return_value = True
    mock_user_repo.return_value.exists_all_users.return_value = False

    service = RoomMemberServicer()
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
    mock_repositories_for_room_member: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_user_repo, mock_room_repo, mock_room_member_repo = mock_repositories_for_room_member
    mock_room_repo.return_value.exists_room.return_value = True
    mock_user_repo.return_value.exists_user.return_value = True
    mock_user_repo.return_value.exists_all_users.return_value = True
    mock_room_member_repo.return_value.create_room_members.return_value = None

    service = RoomMemberServicer()
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
