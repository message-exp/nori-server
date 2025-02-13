from datetime import datetime
from sqlmodel import Session, select
from model import Messages
from google.protobuf.empty_pb2 import Empty

class MessageRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def get_message_by_roomId(
        self, room_id: int, baseline: datetime, limit: int
    ) -> list[Messages]:
        return list(
            self.db.exec(
                select(Messages)
                .where(Messages.room_id == room_id)
                .where(Messages.created_at < baseline)
                .limit(limit)
            ).all()
        )

    def add_message(self, message: Messages) -> None :
        self.db.add(message)
        self.db.commit()
        return None

    def update_message(self, room_id: int, id: int) -> None:
        # Update
        return None
