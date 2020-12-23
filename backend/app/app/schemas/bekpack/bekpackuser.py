from typing import Optional, Set

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import Boolean

# Shared properties
class BekPackUserBase(BaseModel):
    owned_trips: Optional[Set[int]] = None
    joined_trips: Optional[Set[int]] = None
    owned_bags: Optional[Set[int]] = None
    is_active: Optional[bool] = True


# Properties to receive via API on creation
class BekPackUserCreate(BekPackUserBase):
    owner_id: int


# Properties to receive via API on update
class BekPackUserUpdate(BekPackUserBase):
    owned_trips: Optional[Set[int]]
    joined_trips: Optional[Set[int]]
    owned_bags: Optional[Set[int]]
    is_active: Optional[bool]


# Properties shared by models stored in DB
class BekPackUserInDBBase(BekPackUserBase):
    id: int
    owner_id: int
    is_active: True

    class Config:
        orm_mode = True


# Additional properties to return via API
class BekPackUser(BekPackUserBase):
    pass


# Additional properties stored in DB
class BekPackUserInDB(BekPackUserInDBBase):
    pass