from typing import ForwardRef, List, Optional, Set

from pydantic import BaseModel
from app.schemas.user import User

# Shared properties
class BekPackUserBase(BaseModel):
    class Config:
        orm_mode = True

    pass


# Properties to receive via API on creation
class BekpackUserCreate(BekPackUserBase):
    pass


# Properties to receive via API on update
class BekpackUserUpdate(BekPackUserBase):
    is_active: Optional[bool]
    joined_trips: Optional[Set[int]]
    owner_id: Optional[int]


# Properties shared by models stored in DB
class BekPackUserInDBBase(BekPackUserBase):
    id: int
    is_active: bool
    owner_id: int


# Additional properties to return via API
class BekpackUser(BekPackUserBase):

    id: int
    is_active: bool = True
    owner_id: int
    owner: User


# Additional properties stored in DB
class BekpackUserInDB(BekPackUserInDBBase):
    pass


1
