from typing import List, Optional, Set

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import Boolean

# Shared properties
class BekPackUserBase(BaseModel):
    class Config:
        orm_mode = True


# Properties to receive via API on creation
class BekPackUserCreate(BekPackUserBase):
    pass


# Properties to receive via API on update
class BekPackUserUpdate(BekPackUserBase):
    owned_trips: Optional[Set[int]]
    joined_trips: Optional[Set[int]]
    owned_bags: Optional[Set[int]]
    is_active: Optional[bool]
    owner_id: Optional[int]


# Properties shared by models stored in DB
class BekPackUserInDBBase(BekPackUserBase):
    id: int
    owner_id: int
    is_active: bool

    class Config:
        orm_mode = True


# Additional properties to return via API
class BekPackUser(BekPackUserBase):
    id: int
    owned_trips: Set[int] = None
    joined_trips: Set[int] = None
    owned_bags: Set[int] = None
    is_active: bool = True
    owner_id: int
    pass


# Additional properties stored in DB
class BekPackUserInDB(BekPackUserInDBBase):
    pass
