import pytest
from unittest.mock import MagicMock
from typing import Generator, Tuple
from grpc import ServicerContext
from pytest_mock import MockerFixture
from src.utils.token_helper import generate_jwt_token


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
def mock_repositories_for_message(
    mocker: MockerFixture,
) -> Generator[Tuple[MagicMock, MagicMock, MagicMock, MagicMock , MagicMock], None, None]:
    """Mock UserRepository, RoomRepository, RoomMemberRepository"""
    mock_db_session = MagicMock()
    mocker.patch(
        "src.api.message.message_service.get_db", return_value=mock_db_session
    )
    mock_user_repo: MagicMock = mocker.patch(
        "src.api.message.message_service.UserRepo" , create= True
    )
    mock_room_repo: MagicMock = mocker.patch(
        "src.api.message.message_service.RoomRepo" , create= True
    )
    mock_room_member_repo: MagicMock = mocker.patch(
        "src.api.message.message_service.RoomMemberRepo" , create= True
    )
    mock_refresh_token_repo: MagicMock = mocker.patch(
        "src.api.message.message_service.RefreshTokenRepo" , create= True
    )
    mock_message_repo = mocker.patch(
        "src.api.message.message_service.MessageRepo" ,create= True
    )
    yield mock_user_repo, mock_room_repo, mock_room_member_repo, mock_refresh_token_repo , mock_message_repo

    
@pytest.fixture
def mock_repositories_for_room_general(
    mocker: MockerFixture,
) -> Generator[Tuple[MagicMock, MagicMock, MagicMock], None, None]:
    """Mock UserRepository, RoomRepository, RoomMemberRepository"""
    mock_db_session = MagicMock()
    mocker.patch(
        "src.api.room.room_general_service.get_db", return_value=mock_db_session
    )

    mock_user_repo: MagicMock = mocker.patch(
        "src.api.room.room_general_service.UserRepo" , create= True
    )
    mock_room_repo: MagicMock = mocker.patch(
        "src.api.room.room_general_service.RoomRepo" , create= True
    )
    mock_room_member_repo: MagicMock = mocker.patch(
        "src.api.room.room_general_service.RoomMemberRepo" , create= True
    )

    yield mock_user_repo, mock_room_repo, mock_room_member_repo
    


@pytest.fixture
def mock_repositories_for_room_member(
    mocker: MockerFixture,
) -> Generator[Tuple[MagicMock, MagicMock, MagicMock], None, None]:
    """Mock UserRepository, RoomRepository, RoomMemberRepository"""
    mock_db_session = MagicMock()
    mocker.patch(
        "src.api.room.room_member_service.get_db", return_value=mock_db_session
    )
    mock_user_repo: MagicMock = mocker.patch(
        "src.api.room.room_member_service.UserRepo" , create= True
    )
    mock_room_repo: MagicMock = mocker.patch(
        "src.api.room.room_member_service.RoomRepo" , create= True
    )
    mock_room_member_repo: MagicMock = mocker.patch(
        "src.api.room.room_member_service.RoomMemberRepo" , create= True
    )

    yield mock_user_repo, mock_room_repo, mock_room_member_repo


@pytest.fixture
def mock_repositories_for_user_access(
    mocker: MockerFixture,
) -> Generator[Tuple[MagicMock, MagicMock, MagicMock, MagicMock], None, None]:
    """Mock UserRepository, RoomRepository, RoomMemberRepository"""
    mock_db_session = MagicMock()
    mocker.patch(
        "src.api.user.user_access_service.get_db", return_value=mock_db_session
    )

    mock_user_repo: MagicMock = mocker.patch(
        "src.api.user.user_access_service.UserRepo" , create= True
    )
    mock_room_repo: MagicMock = mocker.patch(
        "src.api.user.user_access_service.RoomRepo" , create= True
    )
    mock_room_member_repo: MagicMock = mocker.patch(
        "src.api.user.user_access_service.RoomMemberRepo" , create= True
    ) 
    mock_refresh_token_repo: MagicMock = mocker.patch(
        "src.api.user.user_access_service.RefreshTokenRepo" , create= True
    )
    yield mock_user_repo, mock_room_repo, mock_room_member_repo, mock_refresh_token_repo

@pytest.fixture
def mock_repositories_for_user_account(
    mocker: MockerFixture,
) -> Generator[Tuple[MagicMock, MagicMock, MagicMock, MagicMock], None, None]:
    """Mock UserRepository, RoomRepository, RoomMemberRepository"""
    mock_db_session = MagicMock()
    mocker.patch(
        "src.api.user.user_account_service.get_db", return_value=mock_db_session
    )

    mock_user_repo: MagicMock = mocker.patch(
        "src.api.user.user_account_service.UserRepo" , create= True
    )
    mock_room_repo: MagicMock = mocker.patch(
        "src.api.user.user_account_service.RoomRepo" , create= True
    )
    mock_room_member_repo: MagicMock = mocker.patch(
        "src.api.user.user_account_service.RoomMemberRepo" , create= True
    ) 
    mock_refresh_token_repo: MagicMock = mocker.patch(
        "src.api.user.user_account_service.RefreshTokenRepo" , create= True
    )
    yield mock_user_repo, mock_room_repo, mock_room_member_repo, mock_refresh_token_repo

@pytest.fixture
def mock_repositories_for_user_network(
    mocker: MockerFixture,
) -> Generator[Tuple[MagicMock, MagicMock, MagicMock, MagicMock], None, None]:
    """Mock UserRepository, RoomRepository, RoomMemberRepository"""
    mock_db_session = MagicMock()
    mocker.patch(
        "src.api.user.user_network_service.get_db", return_value=mock_db_session
    )
    mock_user_repo: MagicMock = mocker.patch(
        "src.api.user.user_network_service.UserRepo" , create= True
    )
    mock_room_repo: MagicMock = mocker.patch(
        "src.api.user.user_network_service.RoomRepo" , create= True
    )
    mock_room_member_repo: MagicMock = mocker.patch(
        "src.api.user.user_network_service.RoomMemberRepo" , create= True
    )
    mock_refresh_token_repo: MagicMock = mocker.patch(
        "src.api.user.user_network_service.RefreshTokenRepo" , create= True
    )
    yield mock_user_repo, mock_room_repo, mock_room_member_repo, mock_refresh_token_repo

