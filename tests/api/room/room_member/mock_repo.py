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
def mock_repositories(
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
