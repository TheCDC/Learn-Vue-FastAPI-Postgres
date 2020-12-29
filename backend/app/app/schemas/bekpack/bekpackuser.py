from typing import List, Optional, Set
from app.db.base_class import Base
from app.schemas.bekpack.bekpacktrip import BekpackTrip

from pydantic import BaseModel, validator
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
    is_active: Optional[bool]
    joined_trips: Optional[Set[int]]
    owned_bags: Optional[Set[int]]
    owned_trips: Optional[Set[int]]
    owner_id: Optional[int]


# Properties shared by models stored in DB
class BekPackUserInDBBase(BekPackUserBase):
    id: int
    is_active: bool
    owner_id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class BekPackUser(BekPackUserBase):

    id: int
    is_active: bool = True
    joined_trips: List[BekpackTrip] = []
    owned_bags: List[int] = []
    owned_trips: List[BekpackTrip] = []
    owner_id: int

    # @validator("joined_trips")
    # def validate_joined(cls, val):
    #     # print("joined", [v for v in val if not isinstance(v, int)])
    #     if len(val) > 0:
    #         if isinstance(val[0], Base):
    #             return [m.id for m in val]
    #     return val

    # @validator("owned_trips")
    # def validate_owned(cls, val):
    #     print("owned", [v for v in val if not isinstance(v, int)])
    #     if len(val) > 0:
    #         if isinstance(val[0], Base):
    #             return [m.id for m in val]

    #     return val


# Additional properties stored in DB
class BekPackUserInDB(BekPackUserInDBBase):
    pass
