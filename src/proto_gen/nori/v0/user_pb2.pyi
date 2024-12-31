from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ('username', 'password', 'room_ids')
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ROOM_IDS_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    room_ids: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, username: _Optional[str]=..., password: _Optional[str]=..., room_ids: _Optional[_Iterable[str]]=...) -> None:
        ...