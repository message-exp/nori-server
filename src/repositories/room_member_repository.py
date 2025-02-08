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
