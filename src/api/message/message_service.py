from typing import Generator
import grpc
from grpc.aio import ServicerContext

from proto_generated.nori.v0.message.message_pb2 import Message
from proto_generated.nori.v0.message.message_service_pb2_grpc import (
    MessageServiceServicer,
)
from proto_generated.nori.v0.message.message_id_pb2 import MessageId
from model import Messages
from src.proto_generated.nori.v0.message.get_message_request_pb2 import (
    GetMessageRequest,
)
from utils.db_helper import get_db
from src.utils.token_helper import auth_required
from repositories import UserRepo, MessageRepo, RoomRepo
from google.protobuf.empty_pb2 import Empty


class MessageServicer(MessageServiceServicer):
    service_namespace = "nori.v0.MessageService"
    auth_config: dict[str, bool] = dict()

    @auth_required
    def SendMessage(
        self, request: Message, context: ServicerContext
    ) -> Empty:
        user_id = request.author.id
        room_id = request.room_id.id
        message = request.text
        user_db = UserRepo(next(get_db()))
        user = user_db.get_user(user_id=user_id)
        # check user exist
        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {user_id} not found.")
            return Empty()
        room_db = RoomRepo(next(get_db()))
        room_exist = room_db.exists_room(room_id=room_id)
        # check room exist
        if not room_exist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Room with ID {room_id} not found.")
            return Empty()
        message_db = MessageRepo(next(get_db()))
        message_db.add_message(
            Messages(room_id=room_id, message=message, user=user)
        ).id
        return Empty()

    @auth_required
    def GetMessages(
        self, request: GetMessageRequest, context: ServicerContext
    ) -> Generator[Messages , None , None]:
        baseline = request.baseline.id
        limit = request.limit
        room_id: int = request.room_id.id
        room_db = RoomRepo(next(get_db()))
        room_exist = room_db.exists_room(room_id=room_id)
        if not room_exist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Room with ID {room_id} not found.")
            return
        message_db = MessageRepo(next(get_db()))
        list_of_message = message_db.get_message_by_roomId(
            room_id=room_id, baseline=baseline, limit=limit
        )
        for message in list_of_message:
            yield message
