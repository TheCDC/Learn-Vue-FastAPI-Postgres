from datetime import datetime
from typing import ForwardRef, List, Optional

from pydantic import BaseModel, validator
from pydantic.color import Color

from ...crud.encoders import convert_color

BekpackUser = ForwardRef("BekpackUser")

# Shared properties
class BekpackTripBase(BaseModel):
    color: Optional[Color]
    description: Optional[str]
    name: Optional[str]

    class Config:
        orm_mode = True
        json_encoders = {Color: convert_color}

    @validator("color")
    def color_is_correct_type(cls, v):
        if isinstance(v, Color):
            return v.as_hex()
        elif isinstance(v, str):
            return Color(v)
        raise ValueError(
            f"BekpackTripBase.color is {type(v)}. Expected {Color} or {str}"
        )


# Properties to receive on item creation
class BekpackTripCreate(BekpackTripBase):
    color: Color = "blue"
    description: str
    name: str


# Properties to receive on item update
class BekpackTripUpdate(BekpackTripBase):
    color: Optional[Color]
    description: Optional[str]
    is_active: Optional[bool]
    name: Optional[str]
    owner_id: Optional[int]


# Properties shared by models stored in DB
class BekpackTripInDBBase(BekpackTripBase):
    id: int
    name: str
    owner_id: Optional[int]


# Properties to return to client
class BekpackTrip(BekpackTripInDBBase):
    # bags: List[BekpackBag]
    # members: List[BekpackUser]
    item_lists: List[ForwardRef("BekpackItemList")]
    owner: Optional[BekpackUser]
    time_created: datetime
    time_updated: datetime
    pass


# Additional properties stored in DB
class BekpackTripInDB(BekpackTripInDBBase):
    pass
