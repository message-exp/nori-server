from sqlmodel import Session, select
from model import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: Session) -> None:
        self.db = session

    def exists_refresh_token(
        self,
        user_id: int,
        refresh_token: str,
    ) -> bool:
        refresh_token_found = self.db.exec(
            select(RefreshToken).where(
                RefreshToken.refresh_token == refresh_token
                and RefreshToken.user_id == user_id
            )
        ).first()
        return refresh_token_found is not None

    def save_refresh_token(self, refresh_token: RefreshToken) -> int:
        self.db.add(refresh_token)
        self.db.commit()
        return refresh_token.id

    def update_refresh_token(
        self, user_id: int, old_refresh_token: str, new_refresh_token: str
    ) -> None:
        # use old refresh token to find the RefreshToken in the database
        refresh_token_found = self.db.exec(
            select(RefreshToken).where(
                RefreshToken.user_id
                == user_id & RefreshToken.refresh_token
                == old_refresh_token
            )
        ).first()
        if refresh_token_found:
            refresh_token_found.refresh_token = new_refresh_token
            self.db.add(refresh_token_found)
            self.db.commit()
