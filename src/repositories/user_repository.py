from sqlmodel import Session, select
from model import Users


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def get_user(self, user_id: int) -> Users:
        return self.db.exec(select(Users).where(Users.id == user_id)).first()

    def exists_user(self, user_id: int) -> bool:
        result = self.db.exec(select(Users).where(Users.id == user_id)).first()
        return result is not None

    def create_user(self, user: Users) -> int:
        self.db.add(user)
        self.db.commit()
        return user.id
