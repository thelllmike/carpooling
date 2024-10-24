from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from db import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    rated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    passenger_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    rating = Column(Integer, nullable=False)
    feedback = Column(String, nullable=True)

    # trip = relationship("Trip")
    # rated_by_user = relationship("User", foreign_keys=[rated_by_user_id])
    # passenger = relationship("User", foreign_keys=[passenger_id])
