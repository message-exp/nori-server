import logging
import grpc
from typing import Any, Generator
from grpc.aio import ServicerContext
from kafka import KafkaConsumer, KafkaProducer

from model import Messages
from repositories import UserRepo, MessageRepo, RoomRepo

from proto_generated.nori.v0.message.message_pb2 import Message
from proto_generated.nori.v0.message.send_message_request_pb2 import SendMessageRequest
from proto_generated.nori.v0.message.message_service_pb2_grpc import (
    MessageServiceServicer,
)

from proto_generated.nori.v0.message.get_message_requests_pb2 import (
    GetHistoryMessageRequest,
    GetLatestMessageRequest,
)
from proto_generated.nori.v0.message.message_id_pb2 import MessageId
from proto_generated.nori.v0.message.message_list_pb2 import MessageList
from proto_generated.nori.v0.room.room_id_pb2 import RoomId
from proto_generated.nori.v0.user.user_id_pb2 import UserId
from google.protobuf.timestamp_pb2 import Timestamp

from utils.db_helper import get_db
from utils.token_helper import auth_required
from utils.config import config
from utils.kafka_helper import proto_serializer


class MessageServicer(MessageServiceServicer):
    service_namespace = "nori.v0.MessageService"
    auth_config: dict[str, bool] = dict()

    def __init__(self, producer: KafkaProducer = None) -> None:
        self.producer = (
            KafkaProducer(
                bootstrap_servers=config.KAFKA_SERVER, value_serializer=proto_serializer
            )
            if producer is None
            else producer
        )

    @auth_required
    def SendMessage(
        self, request: SendMessageRequest, context: ServicerContext
    ) -> MessageId:
        user_id = request.author.id
        room_id = request.room_id.id
        message = request.text

        # check user exist
        user_repo = UserRepo(next(get_db()))
        if not user_repo.exists_user(user_id=user_id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {user_id} not found.")
            return MessageId()

        # check room exist
        room_repo = RoomRepo(next(get_db()))
        if not room_repo.exists_room(room_id=room_id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Room with ID {room_id} not found.")
            return MessageId()

        message_repo = MessageRepo(next(get_db()))
        message = Messages(room_id=room_id, message=message, user_id=user_id)
        message_repo.add_message(message)
        timestamp = Timestamp()
        timestamp.FromDatetime(message.created_at)
        self.producer.send(topic=f"room_{room_id}", value=Message(
            room_id=RoomId(id=room_id), message_id=MessageId(id=message.id), created_at=timestamp, author=UserId(id=user_id), text=message.message))
        return MessageId(id=message.id)

    @auth_required
    def GetHistoryMessages(
        self, request: GetHistoryMessageRequest, context: ServicerContext
    ) -> MessageList:
        baseline: int = request.baseline.id
        limit: int = request.limit
        room_id: int = request.room_id.id

        # check room exist
        room_repo = RoomRepo(next(get_db()))
        if not room_repo.exists_room(room_id=room_id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Room with ID {room_id} not found.")
            return MessageList()

        message_repo = MessageRepo(next(get_db()))
        list_of_message: list[Messages] = []

        if limit is not None:
            list_of_message = message_repo.get_message_by_roomId(
                room_id=room_id, baseline=baseline, limit=limit
            )
        else:
            list_of_message = message_repo.get_message_by_roomId(
                room_id=room_id, baseline=baseline
            )

        result = []
        timestamp = Timestamp()
        for message in list_of_message:
            timestamp.FromDatetime(message.created_at)
            result.append(
                Message(
                    room_id=RoomId(id=message.room_id),
                    message_id=MessageId(id=message.id),
                    created_at=timestamp,
                    author=UserId(id=message.user.id),
                    text=message.message,
                )
            )
        return MessageList(messages=result)

    @auth_required
    def GetLatestMessages(
        self, request: GetLatestMessageRequest, context: ServicerContext
    ) -> Generator[Message, Any, None]:
        user_id = request.user_id.id
        room_id = request.room_id.id

        # check user exist
        user_repo = UserRepo(next(get_db()))
        if not user_repo.exists_user(user_id=user_id):
            context.abort(
                grpc.StatusCode.NOT_FOUND, f"User with ID {user_id} not found."
            )
            return

        # check room exist
        room_repo = RoomRepo(next(get_db()))
        if not room_repo.exists_room(room_id=room_id):
            context.abort(
                grpc.StatusCode.NOT_FOUND, f"Room with ID {room_id} not found."
            )
            return

        topic = f"room_{room_id}"
        consumer = KafkaConsumer(
            topic,
            group_id=f"user_{user_id}",
            bootstrap_servers=config.KAFKA_SERVER,
            auto_offset_reset="earliest",
        )

        try:
            for msg in consumer:
                message = Message()
                message.ParseFromString(msg.value)
                if message.author.id != user_id:
                    yield message
        finally:
            consumer.close()
