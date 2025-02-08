from sqlmodel import Session
from model import RoomMembers


class RoomMemberRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def create_room_member(self, room_member: RoomMembers) -> int:
        self.db.add(room_member)
        self.db.commit()
        return room_member.id

    def create_room_members(self, room_id: int, users_id: list[int]) -> None:
        self.db.add_all(
            [RoomMembers(room_id=room_id, user_id=user_id) for user_id in users_id]
        )
        self.db.commit()
