from datetime import datetime
import pytest
import grpc
from unittest.mock import MagicMock
from typing import Generator, Tuple
from grpc import ServicerContext
from pytest_mock import MockerFixture

from src.proto_generated.nori.v0.message.get_message_requests_pb2 import (
    GetHistoryMessageRequest,
)
from google.protobuf.timestamp_pb2 import Timestamp
from src.proto_generated.nori.v0.message.message_id_pb2 import MessageId
from src.proto_generated.nori.v0.message.message_list_pb2 import MessageList
from src.proto_generated.nori.v0.room.room_id_pb2 import RoomId
from src.proto_generated.nori.v0.message.message_pb2 import Message
from src.proto_generated.nori.v0.user.user_id_pb2 import UserId
from src.utils.token_helper import generate_jwt_token
from src.api.message.message_service import MessageServicer, Messages
from src.api.user.user_service import Users


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


@pytest.fixture
def mock_kafka_producer(mocker: MockerFixture) -> Generator[MagicMock, None, None]:
    """Mock KafkaProducer to prevent real Kafka interactions"""
    mock_producer = mocker.patch("src.api.message.message_service.KafkaProducer")
    yield mock_producer


def test_get_history_message_success(
    mock_repositories: Tuple[MagicMock, MagicMock],
    grpc_context: MagicMock,
    mock_kafka_producer: MagicMock,
) -> None:
    mock_message_repo, mock_room_repo = mock_repositories
    mock_message_repo.return_value.get_message_by_roomId.return_value = [
        Messages(
            id=1,
            room_member_id=1,
            room_id=123,
            user=Users(id=1),
            created_at=datetime(2023, 12, 25, 15, 30, 0),
            message="hello",
        ),
        Messages(
            id=2,
            room_member_id=1,
            room_id=123,
            user=Users(id=1),
            created_at=datetime(2023, 12, 25, 15, 30, 0),
            message="world",
        ),
        Messages(
            id=3,
            room_member_id=1,
            room_id=123,
            user=Users(id=1),
            created_at=datetime(2023, 12, 25, 15, 30, 0),
            message="!",
        ),
        Messages(
            id=4,
            room_member_id=1,
            room_id=123,
            user=Users(id=1),
            created_at=datetime(2023, 12, 25, 15, 30, 0),
            message="I",
        ),
        Messages(
            id=5,
            room_member_id=1,
            room_id=123,
            user=Users(id=1),
            created_at=datetime(2023, 12, 25, 15, 30, 0),
            message="am",
        ),
        Messages(
            id=6,
            room_member_id=1,
            room_id=123,
            user=Users(id=1),
            created_at=datetime(2023, 12, 25, 15, 30, 0),
            message="here",
        ),
    ]
    mock_room_repo.return_value.exists_room.return_value = True
    servicer: MessageServicer = MessageServicer(mock_kafka_producer)
    request: GetHistoryMessageRequest = GetHistoryMessageRequest(
        room_id=RoomId(id=123), limit=6, baseline=MessageId(id=1234567890)
    )
    response = servicer.GetHistoryMessages(request, grpc_context)

    timestamp = Timestamp()
    timestamp.FromDatetime(datetime(2023, 12, 25, 15, 30, 0))

    # 確保 response 是 MessageList 類型
    assert isinstance(response, MessageList)

    # 預期的結果列表
    expected_messages = [
        Message(
            room_id=RoomId(id=123),
            message_id=MessageId(id=1),
            created_at=timestamp,
            author=UserId(id=1),
            text="hello",
        ),
        Message(
            room_id=RoomId(id=123),
            message_id=MessageId(id=2),
            created_at=timestamp,
            author=UserId(id=1),
            text="world",
        ),
        Message(
            room_id=RoomId(id=123),
            message_id=MessageId(id=3),
            created_at=timestamp,
            author=UserId(id=1),
            text="!",
        ),
        Message(
            room_id=RoomId(id=123),
            message_id=MessageId(id=4),
            created_at=timestamp,
            author=UserId(id=1),
            text="I",
        ),
        Message(
            room_id=RoomId(id=123),
            message_id=MessageId(id=5),
            created_at=timestamp,
            author=UserId(id=1),
            text="am",
        ),
        Message(
            room_id=RoomId(id=123),
            message_id=MessageId(id=6),
            created_at=timestamp,
            author=UserId(id=1),
            text="here",
        ),
    ]

    # 用 for 迴圈來比較每一個 message 的屬性
    for expected_msg, actual_msg in zip(expected_messages, response.messages):
        assert expected_msg.room_id == actual_msg.room_id, (
            f"RoomId mismatch: {expected_msg.room_id} != {actual_msg.room_id}"
        )
        assert expected_msg.message_id == actual_msg.message_id, (
            f"MessageId mismatch: {expected_msg.message_id} != {actual_msg.message_id}"
        )
        assert expected_msg.created_at == actual_msg.created_at, (
            f"CreatedAt mismatch: {expected_msg.created_at} != {actual_msg.created_at}"
        )
        assert expected_msg.author == actual_msg.author, (
            f"Author mismatch: {expected_msg.author} != {actual_msg.author}"
        )
        assert expected_msg.text == actual_msg.text, (
            f"Text mismatch: {expected_msg.text} != {actual_msg.text}"
        )

    # 確認 mock 函數被正確調用
    mock_message_repo.return_value.get_message_by_roomId.assert_called_once_with(
        room_id=123, baseline=1234567890, limit=6
    )
    mock_room_repo.return_value.exists_room.assert_called_once_with(room_id=123)


def test_get_history_message_roomNotFound(
    mock_repositories: Tuple[MagicMock, MagicMock],
    grpc_context: MagicMock,
    mock_kafka_producer: MagicMock,
) -> None:
    _, mock_room_repo = mock_repositories
    mock_room_repo.return_value.exists_room.return_value = False
    servicer: MessageServicer = MessageServicer(mock_kafka_producer)
    request: GetHistoryMessageRequest = GetHistoryMessageRequest(
        room_id=RoomId(id=123), limit=6, baseline=MessageId(id=1234567890)
    )
    response = servicer.GetHistoryMessages(request, grpc_context)
    assert response == MessageList()
    grpc_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    grpc_context.set_details.assert_called_once_with("Room with ID 123 not found.")
    mock_room_repo.return_value.exists_room.assert_called_once_with(room_id=123)
