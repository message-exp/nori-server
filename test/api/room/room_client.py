import grpc
from src.proto_generated.nori.v0.room.room_create_request_pb2 import RoomCreateRequest
from src.proto_generated.nori.v0.room.room_service_pb2_grpc import RoomServiceStub
from src.proto_generated.nori.v0.user.user_id_pb2 import UserId


def create_room() -> None:
    # 建立與 gRPC 伺服器的連接
    channel = grpc.insecure_channel("localhost:3000")
    stub = RoomServiceStub(channel)
    # 準備要發送的請求資料
    request = RoomCreateRequest(
        user_id=UserId(user_id=7292453983640096768),  # 假設這是用戶 ID
        name="Test Room",  # 假設這是房間名稱
    )

    try:
        # 呼叫 CreateRoom 方法並接收回應
        response = stub.CreateRoom(request)

        # 輸出房間 ID
        print(f"Room created with ID: {response.room_id}")

    except grpc.RpcError as e:
        # 處理錯誤情況
        print(f"Error creating room: {e.code()} - {e.details()}")


if __name__ == "__main__":
    create_room()
