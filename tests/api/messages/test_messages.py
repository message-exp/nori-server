import pytest
import grpc
from unittest.mock import MagicMock
from typing import Generator, Tuple
from grpc import ServicerContext
from pytest_mock import MockerFixture
from src.utils.token_helper import generate_token
from src.api.message.message_service import MessageServicer
from repositories.message_repository import MessageRepository
@pytest.fixture
def mock_repositories(
    mocker: MockerFixture,

) -> Generator[Tuple[MagicMock], None, None]:
    """Mock UserRepository, RoomRepository, RoomMemberRepository"""
    mock_db_session = MagicMock()
    mocker.patch("src.api.room.room_service.get_db", return_value=mock_db_session)

    mock_message_repo: MagicMock = mocker.patch("src.api.message.message_service.MessageRepository")
    
    yield mock_message_repo

@pytest.fixture
def grpc_context() -> MagicMock:
    """Mock gRPC context with valid authorization metadata"""
    context: MagicMock = MagicMock(spec=ServicerContext)
    token = generate_token(subject="test")
    context.invocation_metadata.return_value = (("authorization", token),)
    return context

def test_get_message_success(mock_repositories : Tuple[MagicMock] , grpc_context: MagicMock) -> None:
    mock_message_repo = mock_repositories
    mock_message_repo.return_value.get_message_by_roomId.return_value = [
        MagicMock(id = 1 , room_id = 123 , text = "abc" ,)

    ]
    servicer = MessageServicer()
    request : GetMessageRequest = GetMessageRequest(
        room_id = 123,
        limit = 3,
    ) 




    
