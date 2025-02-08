from sqlmodel import Session, select
from model import Rooms


class RoomRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def create_room(self, room: Rooms) -> int:
        self.db.add(room)
        self.db.commit()
        return room.id

    def exists_room(self, room_id: int) -> bool:
        room = self.db.exec(select(Rooms).where(Rooms.id == room_id)).first()
        return room is not None
