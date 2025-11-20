from sqlalchemy import Column, Integer,Float, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class ContentLog(Base):
    __tablename__ = "content_logs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, nullable=True)
    human_score = Column(Float, nullable=True)
    readability_score = Column(Integer, nullable=True)
    credits_used = Column(Integer, nullable=True)
    credits_remaining = Column(Integer, nullable=True)
    language = Column(String(5), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())