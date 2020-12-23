from typing import Optional, Set

from pydantic import BaseModel

from colour import Color

# Shared properties
class BekpackTripBase(BaseModel):
    bags: Optional[Set[int]] = None
    color: Optional[Color] = Color("blue")
    is_active: Optional[bool] = True
    members: Optional[Set[int]] = None
    name: Optional[str] = None


# Properties to receive on item creation
class BekpackTripCreate(BekpackTripBase):
    name: str
    owner_id: int


# Properties to receive on item update
class BekpackTripUpdate(BekpackTripBase):
    bags: Optional[Set[int]]
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
    pass


# Additional properties stored in DB
class BekpackTripInDB(BekpackTripInDBBase):
    pass