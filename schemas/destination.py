from pydantic import BaseModel

class DestinationBase(BaseModel):
    location_name: str
    latitude: float
    longitude: float

class DestinationCreate(DestinationBase):
    pass

class DestinationOut(DestinationBase):
    id: int

    class Config:
        orm_mode = True
