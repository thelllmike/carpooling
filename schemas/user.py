from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    full_name: str
    email: str
    profile_picture: Optional[str] = None  # Optional field for profile picture

class UserCreate(UserBase):
    password: str
    is_driver: bool
    nic_number: Optional[str] = None
    license_number: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    nic_number: Optional[str] = None
    license_number: Optional[str] = None
    # We'll store the file path in the DB; not the raw file bytes
    profile_picture: Optional[str] = None # Optional field for updating profile picture

class UserOut(BaseModel):
    id: int
    full_name: str
    nic_number: str
    license_number: str
    profile_picture: Optional[str] = None

    class Config:
        from_attributes = True  # Pydantic v2 for ORM
        # or "orm_mode = True" if using Pydantic v1