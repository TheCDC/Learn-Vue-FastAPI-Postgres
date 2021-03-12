from datetime import datetime
from typing import ForwardRef, List, Optional

from pydantic import BaseModel, validator
from pydantic.color import Color

from ...crud.encoders import convert_color
from ..bekpack.bekpackuser import BekPackUser
from ..bekpack.bekpacktrip import BekpackTrip

# Shared properties
class BekpackTrip_MembersBase(BaseModel):
    id: Optional[int]
    trip_id: Optional[int]
    user_id: Optional[int]
    trip: Optional[BekpackTrip]
    user: Optional[BekPackUser]


# Properties to receive on item creation
class BekpackTrip_MembersCreate(BekpackTrip_MembersBase):
    pass


# Properties to receive on item update
class BekpackTrip_MembersUpdate(BekpackTrip_MembersBase):
    pass


# Properties shared by models stored in DB
class BekpackTrip_MembersInDBBase(BekpackTrip_MembersBase):
    pass


# Properties to return to client
class BekpackTrip_Members(BekpackTrip_MembersInDBBase):
    pass


# Additional properties stored in DB
class BekpackTrip_MembersInDB(BekpackTrip_MembersInDBBase):
    pass
