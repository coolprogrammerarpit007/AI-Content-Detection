from sqlalchemy import Column, Integer, String, Float, DateTime, func, Text
from .database import Base


class CopyleaksToken(Base):
    __tablename__ = "copyleaks_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class AIDetection(Base):
    __tablename__ = "ai_detections"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String(100), unique=True, index=True)
    ai_score = Column(Float)
    human_score = Column(Float)
    text = Column(Text)
    text_length = Column(Integer)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
