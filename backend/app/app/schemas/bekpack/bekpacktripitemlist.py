from typing import Optional
from app.schemas.bekpack.bekpackbag import BekpackBagInDBBase

from pydantic import BaseModel

# Shared properties
class BekpackTripItemListBase(BaseModel):
    name: Optional[str] = None
    parent_trip_id: Optional[int] = None
    parent_user_id: Optional[int] = None


# Properties to receive via API on creation
class BekpackTripItemListCreate(BekpackTripItemListBase):
    name: str
    parent_trip_id: int
    parent_user_id: int


# Properties to receive via API on update
class BekpackTripItemListUpdate(BekpackTripItemListBase):
    pass


# Properties shared by models stored in DB
class BekpackTripItemListInDBBase(BekpackTripItemListBase):
    id: int
    name: str

    class Config:
        orm_mode = True


# Properties to return to client
class BekpackTrip(BekpackTripItemListInDBBase):
    pass


# Additional properties stored in DB
class BekpackTripInDB(BekpackBagInDBBase):
    pass