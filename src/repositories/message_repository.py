from sqlmodel import Session


class MessageRepository:
    def __init__(self, session: Session) -> None:
        self.db = session
