from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from model import Users, Rooms


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def get_user_only_ids(self, user_id: int) -> Users | None:
        stmt = (
            select(Users)
            .options(selectinload(Users.rooms).load_only(Rooms.id))
            .where(Users.id == user_id)
        )
        return self.db.exec(stmt).first()

    def get_user(self, user_id: int) -> Users:
        return self.db.exec(select(Users).where(Users.id == user_id)).first()

    def exists_user(self, user_id: int) -> bool:
        result = self.db.exec(select(Users).where(Users.id == user_id)).first()
        return result is not None

    def create_user(self, user: Users) -> int:
        self.db.add(user)
        self.db.commit()
        return user.id
