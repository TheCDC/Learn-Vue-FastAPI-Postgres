from typing import Optional, Set

from pydantic import BaseModel, validator

from pydantic.color import Color
from ...crud.encoders import convert_color

# Shared properties
class BekpackTripBase(BaseModel):
    name: Optional[str]
    color: Optional[Color]

    class Config:
        orm_mode = True
        json_encoders = {Color: convert_color}

    @validator("color")
    def validate(cls, c: Color):
        if isinstance(c, Color):
            return c.as_hex()
        elif isinstance(c, str):
            return Color(c)
        return c


# Properties to receive on item creation
class BekpackTripCreate(BekpackTripBase):
    name: str
    color: Color = "black"


# Properties to receive on item update
class BekpackTripUpdate(BekpackTripBase):
    color: Optional[Color]
    is_active: Optional[bool]
    members: Optional[Set[int]]
    name: Optional[str]
    owner_id: Optional[int]


# Properties shared by models stored in DB
class BekpackTripInDBBase(BekpackTripBase):
    id: int
    name: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class BekpackTrip(BekpackTripInDBBase):
    bags: Set[int] = []
    members: Set[int] = []


# Additional properties stored in DB
class BekpackTripInDB(BekpackTripInDBBase):
    pass
