import asyncio
import logging
from datetime import datetime, timezone
from typing import Any

import grpc
from proto_gen.chat.message_pb2 import Message
from proto_gen.chat.room_pb2 import Room
from proto_gen.chat.user_pb2 import User
from proto_gen.chat.service_pb2 import UserRequest, RoomRequest, JoinRoomRequest
from proto_gen.chat.service_pb2_grpc import ServiceServicer, add_ServiceServicer_to_server

from google.protobuf.empty_pb2 import Empty
from google.protobuf.timestamp_pb2 import Timestamp

import db as db


class ServiceServicer(ServiceServicer):
    def CreateUser(self: Any, request: UserRequest, unused_context) -> Empty:
        logging.info(f"Create user {request.username}")
        db.new_user(request.username, "")
        logging.debug(f"rooms of {request.username}: {db.get_user(request.username)["rooms"]}")
        return Empty()

    def GetUser(self: Any, request: UserRequest, unused_context) -> User:
        logging.info(f"Get user {request.username}")
        user = db.get_user(request.username)
        return User(username=user["username"], password="", room_ids=user["rooms"])

    def CreateRoom(self: Any, request: Room, unused_context) -> Empty:
        logging.info(f"Create room {request.name}")
        room_id = db.generate_room_id()
        db.new_room(room_id, request.name, request.usernames)
        return Empty()
    
    def JoinRoom(self: Any, request: JoinRoomRequest, unused_context) -> Empty:
        logging.info(f"User {request.username} Joined room {request.room_id}")
        db.join_room(request.username, request.room_id)
        return Empty()

    def GetRoom(self: Any, request: RoomRequest, unused_context) -> Room:
        logging.info(f"Get room {request.room_id}")
        room = db.get_room(request.room_id)
        return Room(room_id=room["room_id"], name=room["name"], usernames=room["usernames"])

    def SendMessage(self: Any, request: Message, unused_context) -> Empty:
        logging.info(f"Send message: user {request.author_id} in room {request.room_id} says {request.text}")
        server_time = datetime.now(timezone.utc)
        user_timestamp = request.timestamp
        user_time = datetime.fromtimestamp(user_timestamp.seconds + user_timestamp.nanos / 1e9, timezone.utc)
        if user_time < server_time and (server_time - user_time).total_seconds() < 0.5:
            msg_time = user_time
        else:
            msg_time = server_time

        db.new_message(request.author_id, request.room_id, request.text, msg_time)
        return Empty()

    async def GetMessages(self: Any, request: UserRequest, unused_context):
        # while True:
        messages = db.get_user_messages(request.username)
        for message in messages:
            yield Message(
                message_id=message["msg_id"], 
                author_id=message["author_username"], 
                room_id=message["room_id"], 
                text=message["message"], 
                timestamp=Timestamp(seconds=int(message["timestamp"].timestamp()), nanos=int(message["timestamp"].microsecond * 1e3))
            )
        # await asyncio.sleep(0.1)


async def serve() -> None:
    db.init_db()
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = grpc.aio.server()
    add_ServiceServicer_to_server(ServiceServicer(), server)
    server.add_insecure_port("[::]:3000")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.get_event_loop().run_until_complete(serve())
