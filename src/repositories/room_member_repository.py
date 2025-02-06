from sqlmodel import Session
from model import RoomMembers


class RoomMemberRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def create_room_member(self, room_member: RoomMembers) -> int:
        self.db.add(room_member)
        self.db.commit()
        return room_member.id
