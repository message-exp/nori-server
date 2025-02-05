from sqlmodel import Session, select
from sqlalchemy.orm import selectinload, load_only
from model import Users, Rooms


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def get_user(self, user_id: int) -> Users:
        stmt = (
            select(Users)
            .options(selectinload(Users.rooms).load_only(Rooms.id))
            .where(Users.id == user_id)
        )
        return self.db.exec(stmt).first()
