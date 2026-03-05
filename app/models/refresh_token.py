from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from datetime import datetime
from app.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    token = Column(String(512), unique=True, nullable=False)

    expires_at = Column(TIMESTAMP, nullable=False)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)