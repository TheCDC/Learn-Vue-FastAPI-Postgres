from typing import Optional

from pydantic import BaseModel, validator
from pydantic.color import Color

from app.crud.encoders import convert_color
from app.schemas.bekpack.bekpackbag import BekpackBagInDBBase


# Shared properties
class BekpackItemListBase(BaseModel):
    color: Optional[Color]
    name: Optional[str] = None

    @validator("color")
    def validate(cls, c: Color):
        if isinstance(c, Color):
            return c.as_hex()
        elif isinstance(c, str):
            return Color(c)
        return c

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
    pass


# Additional properties stored in DB
class BekpackTripInDB(BekpackBagInDBBase):
    pass
