from typing import ForwardRef, List, Optional

from pydantic import BaseModel, validator
from pydantic.color import Color

from app.crud.encoders import convert_color
from app.schemas.bekpack.bekpackbag import BekpackBagInDBBase

BekpackTrip = ForwardRef("BekpackTrip")
BekpackTripItemList = ForwardRef("BekpackItemList")
BekpackItemListItem = ForwardRef("BekpackItemListItem")
# Shared properties
class BekpackItemListBase(BaseModel):
    color: Optional[Color]
    name: Optional[str] = None

    @validator("color")
    def color_is_correct_type(cls, v):
        if isinstance(v, Color):
            return v.as_hex()
        elif isinstance(v, str):
            return Color(v)
        raise ValueError(
            f"BekpackTripBase.color is {type(v)}. Expected {Color} or {str}"
        )

    class Config:
        orm_mode = True
        json_encoders = {Color: convert_color}


# Properties to receive via API on creation
class BekpackItemListCreate(BekpackItemListBase):
    name: str
    color: Color = "blue"


# Properties to receive via API on update
class BekpackItemListUpdate(BekpackItemListBase):
    pass


# Properties shared by models stored in DB
class BekpackItemListInDBBase(BekpackItemListBase):
    id: int
    name: str

    class Config:
        orm_mode = True


# Properties to return to client
class BekpackItemList(BekpackItemListInDBBase):
    items: List[BekpackItemListItem]


# Additional properties stored in DB
class BekpackTripInDB(BekpackBagInDBBase):
    pass
