import grpc
from grpc.aio import ServicerContext

from proto_generated.nori.v0.message.message_pb2 import Message
from proto_generated.nori.v0.message.message_service_pb2_grpc import (
    MessageServiceServicer,
)
from proto_generated.nori.v0.message.message_id_pb2 import MessageId
from model import Messages
from src.proto_generated.nori.v0.message.get_message_request_pb2 import GetMessageRequest
from utils.db_helper import get_db
from src.utils.token_helper import auth_required
from repositories import UserRepo, MessageRepo , RoomRepo


class MessageServicer(MessageServiceServicer):
    service_namespace = "nori.v0.MessageService"
    auth_config: dict[str, bool] = dict()

    @auth_required
    def SendMessage(self, request: Message, context: ServicerContext) -> MessageId | None:
        user_id = request.author.id
        room_id = request.room_id.id
        message = request.text
        userDB = UserRepo(next(get_db()))
        user = userDB.get_user(user_id=user_id)
        # check user exist
        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {user_id} not found.")
            return None
        roomDB = RoomRepo(next(get_db()))
        room_exist = roomDB.exists_room(room_id=room_id)
        # check room exist
        if not room_exist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Room with ID {room_id} not found.")
            return None
        messageDB = MessageRepo(next(get_db()))
        input_message_id = messageDB.add_message_to_db(
            Messages(

                room_id=room_id,
                message=message,
                user=user
            )
        ).id
        return MessageId(id=input_message_id)

    # @auth_required
    # def GetMessages(self, request: GetMessageRequest, context: ServicerContext) -> Message:
    #     # TODO: ...... (implement get messages logic)
    #     baseline = request.baseline
    #     limit = request.limit
    #     roomId: int = request.room_id
    #     message_db = MessageRepo(next(get_db()))
    #     return message_db.get_message_by_roomId(roomId)
