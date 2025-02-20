import grpc
from grpc.aio import ServicerContext

from proto_generated.nori.v0.message.message_pb2 import Message
from proto_generated.nori.v0.message.message_service_pb2_grpc import (
    MessageServiceServicer,
)
from model import Messages
from proto_generated.nori.v0.message.get_message_request_pb2 import (
    GetMessageRequest,
)
from utils.db_helper import get_db
from utils.token_helper import auth_required
from repositories import UserRepo, MessageRepo, RoomRepo
from google.protobuf.empty_pb2 import Empty
from proto_generated.nori.v0.message.message_list_pb2 import MessageList


class MessageServicer(MessageServiceServicer):
    service_namespace = "nori.v0.MessageService"
    auth_config: dict[str, bool] = dict()

    @auth_required
    def SendMessage(self, request: Message, context: ServicerContext) -> Empty:
        user_id = request.author.id
        room_id = request.room_id.id
        message = request.text
        user_repo = UserRepo(next(get_db()))
        user = user_repo.get_user(user_id=user_id)
        # check user exist
        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {user_id} not found.")
            return Empty()
        room_repo = RoomRepo(next(get_db()))
        room_exist = room_repo.exists_room(room_id=room_id)
        # check room exist
        if not room_exist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Room with ID {room_id} not found.")
            return Empty()
        message_repo = MessageRepo(next(get_db()))
        message_repo.add_message(
            Messages(room_id=room_id, message=message, user=user)
        ).id
        return Empty()

    @auth_required
    def GetMessages(
        self, request: GetMessageRequest, context: ServicerContext
    ) -> MessageList:
        baseline: int = request.baseline.id
        limit: int = request.limit
        room_id: int = request.room_id.id
        room_repo = RoomRepo(next(get_db()))
        room_exist: bool = room_repo.exists_room(room_id=room_id)
        if not room_exist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Room with ID {room_id} not found.")
            return []
        message_repo = MessageRepo(next(get_db()))
        list_of_message: list[Messages] = []
        #
        if limit is not None:
            list_of_message = message_repo.get_message_by_roomId(
                room_id=room_id, baseline=baseline, limit=limit
            )
        else:
            list_of_message = message_repo.get_message_by_roomId(
                room_id=room_id, baseline=baseline
            )
        return MessageList(messages = list_of_message)
