from sqlmodel import Session, select
from model import RoomMembers


class RoomMemberRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def get_user_room_members(self, user_id: int) -> list[RoomMembers] | None:
        result = self.db.exec(
            select(RoomMembers).where(RoomMembers.user_id == user_id)
        ).all()
        return list(result) if result else None

    def create_room_member(self, room_member: RoomMembers) -> int:
        self.db.add(room_member)
        self.db.commit()
        return room_member.id

    def create_room_members(self, room_id: int, users_id: list[int]) -> None:
        self.db.add_all(
            [RoomMembers(room_id=room_id, user_id=user_id) for user_id in users_id]
        )
        self.db.commit()
