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
    profile_picture: Optional[str] = None  # Optional field for updating profile picture

class UserOut(UserBase):
    id: int
    is_driver: bool

    class Config:
        orm_mode = True