from app.models.bekpack import (
    BekpackBag,
    BekpackListItem,
    BekpackTrip,
    BekPackTrip_Members,
    BekpackTripItemList,
    BekpackUser,
)
from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import Boolean

# TODO: change modle imports to schema imports in order to properly define schemas.

# Shared properties
class BekPackUserBase(BaseModel):
    pass


# Properties to receive on item creation
class BekPackUserCreate(BekPackUserBase):
    owner_id: int


# Properties to receive on item update
class BekPackUserUpdate(BekPackUserBase):
    owned_trips: Optional[List[BekpackTrip]]
    joined_trips: Optional[List[BekpackTrip]]
    owned_bag: Optional[List[BekpackBag]]
    is_active: Optional[bool]


# Properties shared by models stored in DB
class BekPackUserInDBBase(BekPackUserBase):
    id: int
    owner_id: int
    is_active: True

    class Config:
        orm_mode = True


# Properties to return to client
class BekPackUser(BekPackUserBase):
    pass


# Properties properties stored in DB
class BekPackUserInDB(BekPackUserInDBBase):
    pass