"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'nori/v0/service.proto')
_sym_db = _symbol_database.Default()
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from ...nori.v0 import message_pb2 as nori_dot_v0_dot_message__pb2
from ...nori.v0 import room_pb2 as nori_dot_v0_dot_room__pb2
from ...nori.v0 import user_pb2 as nori_dot_v0_dot_user__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15nori/v0/service.proto\x12\x07nori.v0\x1a\x1bgoogle/protobuf/empty.proto\x1a\x15nori/v0/message.proto\x1a\x12nori/v0/room.proto\x1a\x12nori/v0/user.proto"\x1f\n\x0bUserRequest\x12\x10\n\x08username\x18\x01 \x01(\t"\x1e\n\x0bRoomRequest\x12\x0f\n\x07room_id\x18\x01 \x01(\t"4\n\x0fJoinRoomRequest\x12\x0f\n\x07room_id\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t2\x98\x03\n\x07Service\x12<\n\nCreateUser\x12\x14.nori.v0.UserRequest\x1a\x16.google.protobuf.Empty"\x00\x120\n\x07GetUser\x12\x14.nori.v0.UserRequest\x1a\r.nori.v0.User"\x00\x125\n\nCreateRoom\x12\r.nori.v0.Room\x1a\x16.google.protobuf.Empty"\x00\x12>\n\x08JoinRoom\x12\x18.nori.v0.JoinRoomRequest\x1a\x16.google.protobuf.Empty"\x00\x120\n\x07GetRoom\x12\x14.nori.v0.RoomRequest\x1a\r.nori.v0.Room"\x00\x129\n\x0bSendMessage\x12\x10.nori.v0.Message\x1a\x16.google.protobuf.Empty"\x00\x129\n\x0bGetMessages\x12\x14.nori.v0.UserRequest\x1a\x10.nori.v0.Message"\x000\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nori.v0.service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_USERREQUEST']._serialized_start = 126
    _globals['_USERREQUEST']._serialized_end = 157
    _globals['_ROOMREQUEST']._serialized_start = 159
    _globals['_ROOMREQUEST']._serialized_end = 189
    _globals['_JOINROOMREQUEST']._serialized_start = 191
    _globals['_JOINROOMREQUEST']._serialized_end = 243
    _globals['_SERVICE']._serialized_start = 246
    _globals['_SERVICE']._serialized_end = 654