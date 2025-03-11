import pytest
import grpc
from unittest.mock import MagicMock
from typing import Generator, Tuple
from pytest_mock import MockerFixture

from src.proto_generated.nori.v0.message.get_message_requests_pb2 import (
    GetLatestMessageRequest,
)
from src.proto_generated.nori.v0.message.message_pb2 import Message
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from src.utils.token_helper import generate_jwt_token
from src.api.message.message_service import MessageServicer


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
    mock_room_repository: MagicMock = mocker.patch(
        "src.api.message.message_service.RoomRepo"
    )

    yield mock_user_repo, mock_message_repo, mock_room_repository


@pytest.fixture
def grpc_context() -> MagicMock:
    """Mock gRPC context with valid authorization metadata"""
    context: MagicMock = MagicMock(spec=grpc.ServicerContext)
    token = generate_jwt_token(subject="test")
    context.invocation_metadata.return_value = (("authorization", token),)
    return context


@pytest.fixture
def mock_kafka_producer(mocker: MockerFixture) -> Generator[MagicMock, None, None]:
    """Mock KafkaProducer to prevent real Kafka interactions"""
    mock_producer = mocker.patch("src.api.message.message_service.KafkaProducer")
    yield mock_producer


def test_get_latest_messages_user_not_found(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock],
    grpc_context: MagicMock,
    mock_kafka_producer: MagicMock,
) -> None:
    mock_user_repo, _, _ = mock_repositories
    mock_user_repo.return_value.exists_user.return_value = False

    request = GetLatestMessageRequest(user_id=UserId(id=1), room_id=RoomId(id=1))
    service = MessageServicer(mock_kafka_producer)

    response = list(service.GetLatestMessages(request, grpc_context))

    grpc_context.abort.assert_called_once_with(
        grpc.StatusCode.NOT_FOUND, "User with ID 1 not found."
    )
    assert response == []


def test_get_latest_messages_room_not_found(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock],
    grpc_context: MagicMock,
    mock_kafka_producer: MagicMock,
) -> None:
    mock_user_repo, _, mock_room_repo = mock_repositories
    mock_user_repo.return_value.exists_user.return_value = True
    mock_room_repo.return_value.exists_room.return_value = False

    request = GetLatestMessageRequest(user_id=UserId(id=1), room_id=RoomId(id=1))
    service = MessageServicer(mock_kafka_producer)

    response = list(service.GetLatestMessages(request, grpc_context))

    grpc_context.abort.assert_called_once_with(
        grpc.StatusCode.NOT_FOUND, "Room with ID 1 not found."
    )
    assert response == []


def test_get_latest_messages_success(
    mock_repositories: Tuple[MagicMock, MagicMock, MagicMock],
    grpc_context: MagicMock,
    mock_kafka_producer: MagicMock,
    mocker: MockerFixture,
) -> None:
    mock_user_repo, _, mock_room_repo = mock_repositories
    mock_user_repo.return_value.exists_user.return_value = True
    mock_room_repo.return_value.exists_room.return_value = True

    mock_kafka_consumer = mocker.patch("src.api.message.message_service.KafkaConsumer")
    mock_message = Message()
    mock_message.author.id = 2
    mock_message.text = "Hello, World!"
    mock_message_bytes = mock_message.SerializeToString()

    mock_kafka_consumer.return_value.__iter__.return_value = [
        MagicMock(value=mock_message_bytes)
    ]

    request = GetLatestMessageRequest(user_id=UserId(id=1), room_id=RoomId(id=1))
    service = MessageServicer(mock_kafka_producer)

    response = list(service.GetLatestMessages(request, grpc_context))

    assert len(response) == 1
    assert isinstance(response[0], Message)
    assert response[0].author.id == 2
    assert response[0].text == "Hello, World!"
    mock_kafka_consumer.return_value.close.assert_called_once()
