from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from db import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    rated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # New field to store driver ratings
    rating = Column(Integer, nullable=False)
    feedback = Column(String(255), nullable=True)  # Optional feedback