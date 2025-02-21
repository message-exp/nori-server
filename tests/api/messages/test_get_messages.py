import pytest
import grpc
from unittest.mock import MagicMock
from typing import Generator, Tuple
from grpc import ServicerContext
from pytest_mock import MockerFixture

from src.proto_generated.nori.v0.message.get_message_request_pb2 import (
    GetMessageRequest,
)
from src.proto_generated.nori.v0.message.message_id_pb2 import MessageId
from src.proto_generated.nori.v0.message.message_list_pb2 import MessageList
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.message.message_pb2 import Message
from src.utils.token_helper import generate_jwt_token
from src.api.message.message_service import MessageServicer, Messages
from src.model import Users


@pytest.fixture
def mock_repositories(
    mocker: MockerFixture,
) -> Generator[Tuple[MagicMock, MagicMock], None, None]:
    mock_db_session = MagicMock()
    mocker.patch("src.api.room.room_service.get_db", return_value=mock_db_session)

    mock_message_repo: MagicMock = mocker.patch(
        "src.api.message.message_service.MessageRepo"
    )
    mock_room_repository = mocker.patch("src.api.message.message_service.RoomRepo")

    yield mock_message_repo, mock_room_repository


@pytest.fixture
def grpc_context() -> MagicMock:
    """Mock gRPC context with valid authorization metadata"""
    context: MagicMock = MagicMock(spec=ServicerContext)
    token = generate_jwt_token(subject="test")
    context.invocation_metadata.return_value = (("authorization", token),)
    return context


def test_get_message_success(
    mock_repositories: Tuple[MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_message_repo, mock_room_repo = mock_repositories
    mock_message_repo.return_value.get_message_by_roomId.return_value = [
        Messages(id = 1, room_member_id= 1 ,room_id = 123 , user= Users(id = 1),text="hello"),
        Messages(id = 2, room_member_id= 1 ,room_id = 123 , user= Users(id = 1),text="world"),
        Messages(id = 3, room_member_id= 1 ,room_id = 123 , user= Users(id = 1),text="!"),
        Messages(id = 4, room_member_id= 1 ,room_id = 123 , user= Users(id = 1),text="I"),
        Messages(id = 5, room_member_id= 1 ,room_id = 123 , user= Users(id = 1),text="am"),
        Messages(id = 6, room_member_id= 1 ,room_id = 123 , user= Users(id = 1),text="here"),
        Messages(id = 7, room_member_id= 1 ,room_id = 123 , user= Users(id = 1),text="."),
    ]
    mock_room_repo.return_value.exists_room.return_value = True
    servicer: MessageServicer = MessageServicer()
    request: GetMessageRequest = GetMessageRequest(
        room_id=RoomId(id=123), limit=6, baseline=MessageId(id=1234567890)
    )
    response = servicer.GetMessages(request, grpc_context)
    assert isinstance(response, MessageList)
    assert response == MessageList( [
        Message(room_id = 123 , message_id = 1 , text="hello"),
        Message(text="world"),
        Message(text="!"),
        Message(text="I"),
        Message(text="am"),
        Message(text="here"),
    ])
    mock_message_repo.return_value.get_message_by_roomId.assert_called_once_with(
        room_id=123, baseline=1234567890, limit=6
    )
    mock_room_repo.return_value.exists_room.assert_called_once_with(room_id=123)


def test_get_message_roomNotFound(
    mock_repositories: Tuple[MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    _, mock_room_repo = mock_repositories
    mock_room_repo.return_value.exists_room.return_value = False
    servicer: MessageServicer = MessageServicer()
    request: GetMessageRequest = GetMessageRequest(
        room_id=RoomId(id=123), limit=6, baseline=MessageId(id=1234567890)
    )
    response = servicer.GetMessages(request, grpc_context)
    assert list(response) == []
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("Room with ID 123 not found.")
    mock_room_repo.return_value.exists_room.assert_called_once_with(room_id=123)
