from typing import Set, Optional
from colour import Color

from pydantic import BaseModel

# Shared properties
class BekpackBagBase(BaseModel):
    color: Optional[Color] = Color("orange")
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