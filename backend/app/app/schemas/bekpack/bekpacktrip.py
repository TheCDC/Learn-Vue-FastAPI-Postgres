from datetime import datetime
from typing import ForwardRef, List, Optional

from pydantic import BaseModel, validator
from pydantic.color import Color

from ...crud.encoders import convert_color


# Shared properties
class BekpackTripBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
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
    description: str
    color: Color = "blue"


# Properties to receive on item update
class BekpackTripUpdate(BekpackTripBase):
    color: Optional[Color]
    is_active: Optional[bool]
    name: Optional[str]
    description: Optional[str]
    owner_id: Optional[int]


# Properties shared by models stored in DB
class BekpackTripInDBBase(BekpackTripBase):
    id: int
    name: str
    owner_id: int


# Properties to return to client
class BekpackTrip(BekpackTripInDBBase):
    # bags: List[BekpackBag]
    members: List[ForwardRef("BekPackUser")]
    time_updated: datetime
    # time_created: datetime


# Additional properties stored in DB
class BekpackTripInDB(BekpackTripInDBBase):
    pass
