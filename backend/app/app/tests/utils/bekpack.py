from typing import Optional
from app.schemas.bekpack.bekpacktrip import BekpackTripCreate

from sqlalchemy.orm import Session

from app import crud, models
from app.models import User
from app.models.bekpack import BekpackUser
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_bekpackuser(db: Session, user: User = None):
    if user is None:
        user = create_random_user(db=db)
    bekpack_user = crud.bekpackuser.create_with_owner(db=db, owner_id=user.id)
    return bekpack_user


def create_random_trip(db: Session, bekpack_user: BekpackUser = None):
    if bekpack_user is None:
        bekpack_user = create_random_bekpackuser(db=db)
    obj_in = BekpackTripCreate(
        name=random_lower_string(), description=random_lower_string()
    )
    trip = crud.bekpacktrip.create_with_owner(
        db=db, owner_id=bekpack_user.id, obj_in=obj_in
    )
    return trip
