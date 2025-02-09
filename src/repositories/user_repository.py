from sqlmodel import Session, select, col
from model import Users
from typing import Optional


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def get_user(
        self, user_id: Optional[int] = None, email: Optional[str] = None
    ) -> Users | None:
        if user_id is not None:
            return self.db.exec(select(Users).where(Users.id == user_id)).first()
        if email is not None:
            return self.db.exec(select(Users).where(Users.email == email)).first()
        return None

    def exists_user(
        self, user_id: Optional[int] = None, email: Optional[str] = None
    ) -> bool:
        if user_id is not None:
            user = self.db.exec(select(Users).where(Users.id == user_id)).first()
        elif email is not None:
            user = self.db.exec(select(Users).where(Users.email == email)).first()
        return user is not None

    def exists_all_users(self, user_list: list[int]) -> bool:
        if not user_list:
            return False
        existing_users = self.db.exec(
            select(Users.id).where(col(Users.id).in_(user_list))
        ).all()
        return len(existing_users) == len(user_list)

    def create_user(self, user: Users) -> int:
        self.db.add(user)
        self.db.commit()
        return user.id
