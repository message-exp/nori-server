from sqlmodel import Session ,select
from model import Messages ,Rooms ,RoomMembers

class MessageRepository:
    def __init__(self, session: Session) -> None:
        self.db = session
    def get_message_by_roomId(self ,room_id : int) -> Messages:
        return self.db.exec(select(Messages).where(Messages.room_id == room_id)).one_or_none()


