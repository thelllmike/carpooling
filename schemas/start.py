from pydantic import BaseModel

class StartBase(BaseModel):
    location_name: str
    latitude: float
    longitude: float

class StartCreate(StartBase):
    pass

class StartOut(StartBase):
    id: int

    class Config:
        orm_mode = True
