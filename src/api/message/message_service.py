from grpc.aio import ServicerContext

from google.protobuf.empty_pb2 import Empty
from proto_generated.nori.v0.message.message_pb2 import Message
from proto_generated.nori.v0.room.room_id_pb2 import RoomId

from proto_generated.nori.v0.message.message_service_pb2_grpc import (
    MessageServiceServicer,
)


class MessageServicer(MessageServiceServicer):
    def SendMessage(self, request: Message, context: ServicerContext) -> Empty:
        # TODO: ...... (implement send message logic)

        # context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        # context.set_details('Method not implemented!')
        return Empty()

    def GetMessages(self, request: RoomId, context: ServicerContext) -> Message:
        # TODO: ...... (implement get messages logic)
        return Message()
