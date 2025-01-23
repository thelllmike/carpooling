from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from db import Base
from datetime import datetime

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(255), nullable=False)  # Added length for VARCHAR
    seen = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
