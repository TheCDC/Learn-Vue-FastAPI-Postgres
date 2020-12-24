from .validators import validate_color
from typing import Set, Optional

from pydantic import BaseModel, validator, ValidationError

# Shared properties
class BekpackBagBase(BaseModel):
    color: Optional[str] = "#F57900"

    @validator("color")
    def validate_color(cls, v: str):
        if not validate_color(v):
            raise ValidationError("Color string must be '#XXXXXX' where X [a-fA-F0-9]")
        return v

    items: Optional[Set[int]] = None
    name: Optional[str] = None
    owner_id: Optional[int] = None
    owner_trip_id: Optional[int] = None


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
