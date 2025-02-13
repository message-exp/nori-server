import pytest
import grpc
from unittest.mock import MagicMock
from typing import Generator, Tuple
from grpc import ServicerContext
from pytest_mock import MockerFixture

from src.proto_generated.nori.v0.message.message_id_pb2 import MessageId
from src.proto_generated.nori.v0.message.message_pb2 import Message
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from src.utils.token_helper import generate_token
from src.api.message.message_service import MessageServicer, Messages
from google.protobuf.empty_pb2 import Empty

@pytest.fixture
def mock_repositories(
    mocker: MockerFixture,
) -> Generator[Tuple[MagicMock, MagicMock, MagicMock], None, None]:
    mock_db_session = MagicMock()
    mocker.patch("src.api.room.room_service.get_db", return_value=mock_db_session)

    mock_message_repo: MagicMock = mocker.patch(
        "src.api.message.message_service.MessageRepo"
    )
    mock_user_repo: MagicMock = mocker.patch("src.api.message.message_service.UserRepo")
    mock_room_repository = mocker.patch("src.api.message.message_service.RoomRepo")

    yield mock_message_repo, mock_user_repo, mock_room_repository


@pytest.fixture
def grpc_context() -> MagicMock:
    """Mock gRPC context with valid authorization metadata"""
    context: MagicMock = MagicMock(spec=ServicerContext)
    token = generate_token(subject="test")
    context.invocation_metadata.return_value = (("authorization", token),)
    return context


def test_send_message_success(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_message_repo, mock_user_repo, mock_room_repository = mock_repositories
    mock_message_repo.return_value.add_message_to_db.return_value = MagicMock(
        id=1, room_id=123, text="abc"
    )  # Message
    mock_user_repo.return_value.get_user.return_value = MagicMock(user_id=66)
    mock_room_repository.return_value.exists_room.return_value = True

    servicer: MessageServicer = MessageServicer()
    request: Message = Message(room_id=RoomId(id=123), text="abc", author=UserId(id=66))
    response: Empty = servicer.SendMessage(request, grpc_context)

    assert isinstance(response, Empty)
    mock_message_repo.return_value.add_message_to_db.assert_called_once_with(
        Messages(room_id=123, message="abc")
    )
    mock_user_repo.return_value.get_user.assert_called_once_with(user_id=66)
    mock_room_repository.return_value.exists_room.assert_called_once_with(room_id=123)


def test_send_message_userNotFound(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_message_repo, mock_user_repo, mock_room_repository = mock_repositories
    mock_message_repo.return_value.add_message_to_db.return_value = MagicMock(
        id=1, room_id=123, text="abc"
    )  # Message
    mock_user_repo.return_value.get_user.return_value = None
    mock_room_repository.return_value.exists_room.return_value = True

    servicer: MessageServicer = MessageServicer()
    request: Message = Message(room_id=RoomId(id=123), text="abc", author=UserId(id=66))
    response: MessageId = servicer.SendMessage(request, grpc_context)
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("User with ID 66 not found.")

    assert isinstance(response, Empty)
    mock_message_repo.return_value.add_message_to_db.assert_not_called()
    mock_user_repo.return_value.get_user.assert_called_once_with(user_id=66)
    mock_room_repository.return_value.exists_room.assert_not_called()


def test_send_message_roomNotFound(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock], grpc_context: MagicMock
) -> None:
    mock_message_repo, mock_user_repo, mock_room_repository = mock_repositories
    mock_message_repo.return_value.add_message_to_db.return_value = MagicMock(
        id=1, room_id=123, text="abc"
    )  # Message
    mock_user_repo.return_value.get_user.return_value = MagicMock(user_id=66)
    mock_room_repository.return_value.exists_room.return_value = False

    servicer: MessageServicer = MessageServicer()
    request: Message = Message(room_id=RoomId(id=123), text="abc", author=UserId(id=66))
    response: MessageId = servicer.SendMessage(request, grpc_context)
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("Room with ID 123 not found.")

    assert isinstance(response, Empty)
    mock_message_repo.return_value.add_message_to_db.assert_not_called()
    mock_user_repo.return_value.get_user.assert_called_once_with(user_id=66)
    mock_room_repository.return_value.exists_room.assert_called_once_with(room_id=123)
