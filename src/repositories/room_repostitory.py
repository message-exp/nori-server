from sqlmodel import Session

class RoomRepository:
    def __init__(self, session: Session) -> None:
        self.db = session