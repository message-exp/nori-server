from sqlmodel import Session, select
from model import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def exists_refresh_token(
        self,
        refresh_token: str,
    ) -> bool:
        refresh_token_found = self.db.exec(
            select(RefreshToken).where(RefreshToken.refresh_token == refresh_token)
        ).first()
        return refresh_token_found is not None

    def save_refresh_token(self, refresh_token: RefreshToken) -> int:
        self.db.add(refresh_token)
        self.db.commit()
        return refresh_token.id
