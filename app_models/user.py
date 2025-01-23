from db import Base  # Absolute import from the top level
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), index=True)  # Added length for VARCHAR
    email = Column(String(255), unique=True, index=True)  # Added length for VARCHAR
    password = Column(String(255))  # Added length for VARCHAR
    is_driver = Column(Boolean, default=False)
    nic_number = Column(String(50), nullable=True)  # Added length for VARCHAR
    license_number = Column(String(50), nullable=True)  # Added length for VARCHAR
    profile_picture = Column(String(255), nullable=True)  # Added length for VARCHAR
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, full_name='{self.full_name}', email='{self.email}')>"
