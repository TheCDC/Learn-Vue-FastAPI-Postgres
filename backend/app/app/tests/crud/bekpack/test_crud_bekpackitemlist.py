# TODO: test bekpackitemlist CRUDs
from app.tests.utils.utils import random_lower_string
from sqlalchemy.orm import Session

from app import crud, schemas
from app.tests.crud.bekpack.utils import get_bekpack_user, get_random_color
from app.tests.utils.bekpack import create_random_itemlist, create_random_trip
from app.tests.utils.user import create_random_user


def test_create_bekpackitemlist(db: Session) -> None:
    user = get_bekpack_user(db=db)
    trip = create_random_trip(db=db, bekpack_user=user)

    itemlist = crud.bekpackitemlist.create_with_trip_owner(
        db=db,
        obj_in=schemas.BekpackItemListCreate(
            name=random_lower_string(), color=get_random_color()
        ),
        owner_id=user.id,
        trip_id=trip.id,
    )
    assert itemlist.parent_user_id == user.id
    assert itemlist.parent_trip_id == trip.id


def test_get_itemlist_by_owner(db: Session):
    user = get_bekpack_user(db=db)
    trip = create_random_trip(db=db, bekpack_user=user)
    itemlists = [
        create_random_itemlist(db=db, bekpack_user=user, trip=trip) for _ in range(10)
    ]
    found_lists = crud.bekpackitemlist.get_by_owner(db=db, owner_id=user.id)
    target_ids = set([i.id for i in itemlists])
    found_ids = set([i.id for i in found_lists])
    assert target_ids == found_ids


def test_itemlist_get_by_trip(db: Session):
    trip = create_random_trip(db=db)
    itemlists = [create_random_itemlist(db=db, trip=trip) for _ in range(10)]
    found_lists = crud.bekpackitemlist.get_by_trip(db=db, trip_id=trip.id)
    target_ids = set([i.id for i in itemlists])
    found_ids = set([i.id for i in found_lists])
    assert target_ids == found_ids
