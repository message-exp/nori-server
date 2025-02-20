from sqlmodel import Session, select
from model import Messages
from sqlalchemy import desc


class MessageRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def get_message_by_roomId(
        self, room_id: int, baseline: int, limit: int = 10
    ) -> list[Messages]:
        if baseline is None:
            return list(
                self.db.exec(
                    select(Messages)
                    .where(Messages.room_id == room_id)
                    .order_by(desc(Messages.id))
                    .limit(limit)
                ).all()
            )
        else:
            return list(
                self.db.exec(
                    select(Messages)
                    .where(Messages.room_id == room_id)
                    .where(Messages.id < baseline)
                    .order_by(desc(Messages.id))
                    .limit(limit)
                ).all()
            )

    def add_message(self, message: Messages) -> None:
        self.db.add(message)
        self.db.commit()
        return None

    def update_message(self, room_id: int, id: int) -> None:
        # Update
        return None
