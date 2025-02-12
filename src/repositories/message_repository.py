from datetime import datetime
from sqlmodel import Session, select
from model import Messages


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

    def add_message_to_db(self, message: Messages) -> Messages:
        self.db.add(message)
        self.db.commit()
        return message

    def update_message_to_db(self, room_id: int, id: int) -> None:
        # Update
        return None
