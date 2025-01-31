from sqlmodel import Session


class RoomMemberRepository:
    def __init__(self, session: Session) -> None:
        self.db = session
