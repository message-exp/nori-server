"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'nori/v0/message.proto')
_sym_db = _symbol_database.Default()
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15nori/v0/message.proto\x12\x07nori.v0\x1a\x1fgoogle/protobuf/timestamp.proto"~\n\x07Message\x12\x12\n\nmessage_id\x18\x01 \x01(\t\x12\x11\n\tauthor_id\x18\x02 \x01(\t\x12\x0f\n\x07room_id\x18\x03 \x01(\t\x12\x0c\n\x04text\x18\x04 \x01(\t\x12-\n\ttimestamp\x18\x05 \x01(\x0b2\x1a.google.protobuf.Timestampb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nori.v0.message_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_MESSAGE']._serialized_start = 67
    _globals['_MESSAGE']._serialized_end = 193