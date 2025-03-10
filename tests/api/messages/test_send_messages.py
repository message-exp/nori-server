from datetime import datetime
import pytest
import grpc
from unittest.mock import MagicMock , patch
from typing import Generator, Tuple
from grpc import ServicerContext
from pytest_mock import MockerFixture

from src.proto_generated.nori.v0.message.message_id_pb2 import MessageId
from src.proto_generated.nori.v0.message.send_message_request_pb2 import (
    SendMessageRequest,
)
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from src.utils.token_helper import generate_jwt_token
from src.api.message.message_service import MessageServicer, db


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
    token = generate_jwt_token(subject="test")
    context.invocation_metadata.return_value = (("authorization", token),)
    return context


@pytest.fixture
def mock_kafka_producer(mocker: MockerFixture) -> Generator[MagicMock, None, None]:
    """Mock KafkaProducer to prevent real Kafka interactions"""
    mock_producer = mocker.patch("src.api.message.message_service.KafkaProducer")
    yield mock_producer
@pytest.fixture
def mock_messages(mocker: MockerFixture) -> Generator[MagicMock, None, None]:
    mock_messages = mocker.patch("src.api.message.message_service.db.Messages")
    yield mock_messages


def test_send_message_success(
    mock_messages: MagicMock,
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock],
    grpc_context: MagicMock,
    mock_kafka_producer: MagicMock,
) -> None:
    fake_message = MagicMock(
    id=1,
    room_id=123,
    message="abc",
    user_id=66,
    created_at=datetime.now()
    )
    mock_message_repo, mock_user_repo, mock_room_repository = mock_repositories
    mock_message_repo.return_value.add_message.return_value = MagicMock(
        id=1, room_id=123, text="abc" , created_at=fake_message.created_at
    )  # Message
    mock_user_repo.return_value.exists_user.return_value = True
    mock_room_repository.return_value.exists_room.return_value = True
    mock_messages.return_value = fake_message
    servicer: MessageServicer = MessageServicer(mock_kafka_producer)
    request: SendMessageRequest = SendMessageRequest(
        room_id=RoomId(id=123), text="abc", author=UserId(id=66)
    )
    
    response: MessageId = servicer.SendMessage(request, grpc_context)
    assert isinstance(response, MessageId)
    mock_message_repo.return_value.add_message.assert_called_once_with(fake_message)
    mock_user_repo.return_value.exists_user.assert_called_once_with(user_id=66)
    mock_room_repository.return_value.exists_room.assert_called_once_with(room_id=123)





def test_send_message_userNotFound(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock],
    grpc_context: MagicMock,
    mock_kafka_producer: MagicMock,
) -> None:
    mock_message_repo, mock_user_repo, mock_room_repository = mock_repositories
    mock_message_repo.return_value.add_message.return_value = MagicMock(
        id=1, room_id=123, text="abc"
    )  # Message
    mock_user_repo.return_value.exists_user.return_value = None
    mock_room_repository.return_value.exists_room.return_value = True

    servicer: MessageServicer = MessageServicer(mock_kafka_producer)
    request: SendMessageRequest = SendMessageRequest(
        room_id=RoomId(id=123), text="abc", author=UserId(id=66)
    )
    response: MessageId = servicer.SendMessage(request, grpc_context)
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("User with ID 66 not found.")

    assert isinstance(response, MessageId)
    mock_message_repo.return_value.add_message.assert_not_called()
    mock_user_repo.return_value.exists_user.assert_called_once_with(user_id=66)
    mock_room_repository.return_value.exists_room.assert_not_called()


def test_send_message_roomNotFound(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock],
    grpc_context: MagicMock,
    mock_kafka_producer: MagicMock,
) -> None:
    mock_message_repo, mock_user_repo, mock_room_repository = mock_repositories
    mock_message_repo.return_value.add_message.return_value = MagicMock(
        id=1, room_id=123, text="abc"
    )  # Message
    mock_user_repo.return_value.exists_user.return_value = MagicMock(user_id=66)
    mock_room_repository.return_value.exists_room.return_value = False

    servicer: MessageServicer = MessageServicer(mock_kafka_producer)
    request: SendMessageRequest = SendMessageRequest(
        room_id=RoomId(id=123), text="abc", author=UserId(id=66)
    )
    response: MessageId = servicer.SendMessage(request, grpc_context)
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("Room with ID 123 not found.")

    assert isinstance(response, MessageId)
    mock_message_repo.return_value.add_message.assert_not_called()
    mock_user_repo.return_value.exists_user.assert_called_once_with(user_id=66)
    mock_room_repository.return_value.exists_room.assert_called_once_with(room_id=123)
