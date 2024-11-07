# app_models/user.py

from db import Base  # Absolute import from the top level
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_driver = Column(Boolean, default=False)
    nic_number = Column(String, nullable=True)
    license_number = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)  # New column for profile picture
    created_at = Column(DateTime, default=datetime.utcnow)