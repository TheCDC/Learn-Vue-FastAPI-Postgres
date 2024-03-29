import inspect

from pydantic import BaseModel
from .item import Item, ItemCreate, ItemInDB, ItemUpdate
from .msg import Msg
from .token import Token, TokenPayload
from .user import User, UserCreate, UserInDB, UserUpdate
from .bekpack.bekpackbag import (
    BekpackBag,
    BekpackBagCreate,
    BekpackBagInDB,
    BekpackBagUpdate,
)
from .bekpack.bekpackitemlistitem import (
    BekpackItemListItem,
    BekpackItemListItemCreate,
    BekpackItemListItemInDB,
    BekpackItemListItemUpdate,
)

from .bekpack.bekpacktrip import (
    BekpackTrip,
    BekpackTripCreate,
    BekpackTripInDB,
    BekpackTripUpdate,
)

from .bekpack.bekpacktrip_members import (
    BekpackTrip_Members,
    BekpackTrip_MembersCreate,
    BekpackTrip_MembersUpdate,
)
from .bekpack.bekpackitemlist import (
    BekpackItemList,
    BekpackItemListCreate,
    BekpackItemListInDBBase,
    BekpackItemListUpdate,
)

from .bekpack.bekpackitemlistitem import (
    BekpackItemListItem,
    BekpackItemListItemCreate,
    BekpackItemListItemInDBBase,
    BekpackItemListItemUpdate,
)

from .bekpack.bekpackuser import (
    BekpackUser,
    BekpackUserCreate,
    BekpackUserInDB,
    BekpackUserUpdate,
)


for k, v in dict(locals()).items():
    if inspect.isclass(v):
        if issubclass(v, BaseModel):
            v.update_forward_refs(**locals())
