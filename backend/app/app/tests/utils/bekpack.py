from typing import Optional
from app.tests.crud.bekpack.utils import get_random_color

from sqlalchemy.orm import Session

from app import crud, schemas
from app.models import User
from app.models.bekpack import BekpackItemList, BekpackTrip, BekpackUser
from app.schemas.bekpack.bekpacktrip import BekpackTripCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_bekpackuser(db: Session, user: User = None) -> BekpackUser:
    if user is None:
        user = create_random_user(db=db)
    bekpack_user = crud.bekpackuser.create_with_owner(db=db, owner_id=user.id)
    return bekpack_user


def create_random_trip(db: Session, bekpack_user: BekpackUser = None) -> BekpackTrip:
    if bekpack_user is None:
        bekpack_user = create_random_bekpackuser(db=db)
    obj_in = BekpackTripCreate(
        name=random_lower_string(), description=random_lower_string()
    )
    trip = crud.bekpacktrip.create_with_owner(
        db=db, owner=bekpack_user.owner, obj_in=obj_in
    )
    return trip


def create_random_itemlist(
    db: Session, bekpack_user: BekpackUser = None, trip: BekpackTrip = None
) -> BekpackItemList:
    if bekpack_user is None:
        bekpack_user = create_random_bekpackuser(db=db)
    if trip is None:
        trip = create_random_trip(db=db, bekpack_user=bekpack_user)
    itemlist = crud.bekpackitemlist.create_with_trip_owner(
        db=db,
        obj_in=schemas.BekpackItemListCreate(
            name=random_lower_string(), color=get_random_color()
        ),
        parent_user=bekpack_user.id,
        trip_id=trip.id,
    )
    return itemlist
