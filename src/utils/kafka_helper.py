from google.protobuf.message import Message


def proto_serializer(data: Message) -> bytes:
    return data.SerializeToString()
