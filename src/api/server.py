import grpc

from api.logging_interceptor import LoggingInterceptor
# from api.user.user_service import UserServicer



# from api.room.room_service import RoomServicer
from api.message.message_service import MessageServicer
# from proto_generated.nori.v0.user.user_service_pb2_grpc import (
    # add_UserServiceServicer_to_server,
# )
# from proto_generated.nori.v0.room.room_service_pb2_grpc import (
#     add_RoomServiceServicer_to_server,
# )
from proto_generated.nori.v0.message.message_service_pb2_grpc import (
    add_MessageServiceServicer_to_server,
)
# from proto_generated.nori.v0.room import room_service_pb2
from proto_generated.nori.v0.message import message_service_pb2
# from proto_generated.nori.v0.user import user_service_pb2
from grpc_reflection.v1alpha import reflection

from api.user.user_access_service import UserAccessServicer
from api.user.user_account_service import UserAccountServicer
from api.user.user_network_service import UserNetworkServicer
from api.room.room_general_service import RoomGeneralServicer
from api.room.room_member_service import RoomMemberServicer


from proto_generated.nori.v0.user.access import user_access_service_pb2
from proto_generated.nori.v0.user.account import user_account_service_pb2
from proto_generated.nori.v0.user.network import user_network_service_pb2
from proto_generated.nori.v0.room.general import room_general_service_pb2
from proto_generated.nori.v0.room.member import room_member_service_pb2



from proto_generated.nori.v0.user.access.user_access_service_pb2_grpc import add_UserAccessServiceServicer_to_server
from proto_generated.nori.v0.user.account.user_account_service_pb2_grpc import add_UserAccountServiceServicer_to_server
from proto_generated.nori.v0.user.network.user_network_service_pb2_grpc import add_UserNetworkServiceServicer_to_server
from proto_generated.nori.v0.room.general.room_general_service_pb2_grpc import add_RoomGeneralServiceServicer_to_server
from proto_generated.nori.v0.room.member.room_member_service_pb2_grpc import add_RoomMemberServiceServicer_to_server


def get_server() -> grpc.Server:
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = grpc.aio.server(interceptors=(LoggingInterceptor(),))

    # add_UserServiceServicer_to_server(servicer=UserServicer(), server=server)
    # add_RoomServiceServicer_to_server(servicer=RoomServicer(), server=server)
    add_RoomGeneralServiceServicer_to_server(servicer= RoomGeneralServicer(),server= server)
    add_RoomMemberServiceServicer_to_server(servicer= RoomMemberServicer() , server= server)
    add_UserAccessServiceServicer_to_server(servicer=UserAccessServicer() , server = server)
    add_UserNetworkServiceServicer_to_server(servicer= UserNetworkServicer() , server= server)
    add_UserAccountServiceServicer_to_server(servicer= UserAccountServicer() , server= server)
    
    add_MessageServiceServicer_to_server(servicer=MessageServicer(), server=server)
    SERVICE_NAMES = (
        # user_service_pb2.DESCRIPTOR.services_by_name["UserService"].full_name,
        # room_service_pb2.DESCRIPTOR.services_by_name["RoomService"].full_name,
        user_access_service_pb2.DESCRIPTOR.services_by_name["UserAccessService"].full_name,
        user_account_service_pb2.DESCRIPTOR.services_by_name["UserAccountService"].full_name,
        user_network_service_pb2.DESCRIPTOR.services_by_name["UserNetworkService"].full_name,
        room_general_service_pb2.DESCRIPTOR.services_by_name["RoomGeneralService"].full_name,
        room_member_service_pb2.DESCRIPTOR.services_by_name["RoomMemberService"].full_name,
        message_service_pb2.DESCRIPTOR.services_by_name["MessageService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    # TODO: add other services
    return server
