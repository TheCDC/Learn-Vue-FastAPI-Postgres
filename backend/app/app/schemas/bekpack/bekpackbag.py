from typing import Optional, Set

from pydantic import BaseModel, ValidationError, validator
from pydantic.color import Color

from app.crud.encoders import convert_color
from .validators import validate_color


# Shared properties
class BekpackBagBase(BaseModel):
    color: Optional[Color]
    items: Optional[Set[int]] = None
    name: Optional[str] = None
    owner_id: Optional[int] = None
    owner_trip_id: Optional[int] = None

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
class BekpackBagCreate(BekpackBagBase):
    name: str
    owner_id: int
    owner_trip_id: int


# Properties to receive via API on update
class BekpackBagUpdate(BekpackBagBase):
    pass


# Properties shared by models stored in DB
class BekpackBagInDBBase(BekpackBagBase):
    id: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class BekpackBag(BekpackBagInDBBase):
    pass


# Additional properties stored in DB
class BekpackBagInDB(BekpackBagInDBBase):
    pass
