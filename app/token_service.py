import datetime
from sqlalchemy.orm import Session
from copyleaks.copyleaks import Copyleaks

from .models import CopyleaksToken
from .database import SessionLocal
from .config import settings
from .logger import logger


class TokenService:
    def __init__(self):
        pass

    def _get_db(self) -> Session:
        return SessionLocal()

    def _get_token_row(self, db: Session):
        return db.query(CopyleaksToken).order_by(CopyleaksToken.id.desc()).first()

    def _is_token_valid(self, token_row: CopyleaksToken) -> bool:
        if not token_row:
            return False
        now = datetime.datetime.now(datetime.timezone.utc)
        return token_row.expires_at > now

    def _refresh_token_and_store(self) -> str:
        logger.info("Refreshing Copyleaks token via login API...")

        new_token = Copyleaks.login(
            settings.COPYLEAKS_EMAIL,
            settings.COPYLEAKS_API_KEY
        )

        expires_at = (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(hours=48)
        )

        db = self._get_db()
        try:
            # Optional: clear old tokens
            db.query(CopyleaksToken).delete()

            token_row = CopyleaksToken(
                token=new_token,
                expires_at=expires_at
            )
            db.add(token_row)
            db.commit()
            db.refresh(token_row)

            logger.info("Saved new Copyleaks token in DB.")

        finally:
            db.close()

        return new_token

    def get_valid_token(self) -> str:
        db = self._get_db()
        try:
            row = self._get_token_row(db)
            if row and self._is_token_valid(row):
                return row.token
        finally:
            db.close()

        # Token invalid or missing → refresh
        return self._refresh_token_and_store()


token_service = TokenService()
