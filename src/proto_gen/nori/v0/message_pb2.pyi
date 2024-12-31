from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Message(_message.Message):
    __slots__ = ('message_id', 'author_id', 'room_id', 'text', 'timestamp')
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    author_id: str
    room_id: str
    text: str
    timestamp: _timestamp_pb2.Timestamp

    def __init__(self, message_id: _Optional[str]=..., author_id: _Optional[str]=..., room_id: _Optional[str]=..., text: _Optional[str]=..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...