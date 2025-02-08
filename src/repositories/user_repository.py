from sqlmodel import Session, select, col
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
        user = self.db.exec(select(Users).where(Users.id == user_id)).first()
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
