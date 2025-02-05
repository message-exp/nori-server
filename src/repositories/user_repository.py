from sqlmodel import Session, select
from model import Users


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def get_user(self, user_id: int) -> Users:
        return self.db.exec(select(Users).where(Users.id == user_id)).first()
