from sqlmodel import Session
from model import Rooms


class RoomRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def create_room(self, room: Rooms) -> int:
        self.db.add(room)
        self.db.commit()
        return room.id
