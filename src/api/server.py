import grpc

from api.user_auth_interceptor import UserAuthInterceptor
from api.user import user_service
# from api.room.room_service import RoomServicer
# from api.message.message_service import MessageServicer

# server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
server = grpc.aio.server(interceptors=(UserAuthInterceptor(),))

user_service.add_service_to_server(server)
# TODO: add other services
