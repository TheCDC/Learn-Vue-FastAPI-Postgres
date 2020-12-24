from typing import Optional, Set

from pydantic import BaseModel, validator, ValidationError

from .validators import validate_color


# Shared properties
class BekpackTripBase(BaseModel):
    bags: Optional[Set[int]] = []
    color: Optional[str] = str("#729FCF")
    is_active: Optional[bool] = True
    members: Optional[Set[int]] = []
    name: Optional[str] = None

    @validator("color")
    def validate_color(cls, v: str):
        if not validate_color(v):
            raise ValidationError("Color string must be '#XXXXXX' where X [a-fA-F0-9]")
        return v


# Properties to receive on item creation
class BekpackTripCreate(BekpackTripBase):
    name: str


# Properties to receive on item update
class BekpackTripUpdate(BekpackTripBase):
    bags: Optional[Set[int]]
    color: Optional[str]
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