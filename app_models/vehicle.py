from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    license_plate = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_link = Column(String(255))  # New column for storing image URL or path

    # owner = relationship("User", back_populates="vehicles")