from typing import List

import pytest
from sqlalchemy.orm import Session

from app import crud, core
from app.crud import bekpacktrip, bekpackuser
from app.models.bekpack import BekpackTrip, BekpackTrip_Members, BekpackUser
from app.schemas import BekpackTripCreate
from app.schemas.bekpack.bekpacktrip import BekpackTripUpdate
from app.tests.utils.bekpack import create_random_trip
from app.tests.utils.item import random_lower_string
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_name

from .utils import get_bekpack_user, get_random_color


def test_create_bekpaktrip(db: Session):
    bp_user = get_bekpack_user(db)
    btc = BekpackTripCreate(
        name=random_lower_name(),
        description=random_lower_string(),
        color=get_random_color(),
    )
    bpt = bekpacktrip.create_with_owner(db, obj_in=btc, owner=bp_user.owner)
    assert bpt.owner_id == bp_user.id
    u = bekpackuser.get(db=db, id=bp_user.id, user=bp_user.owner)
    assert u
    # trip added to users's list of owned trips
    assert bpt.id in list(i.id for i in u.owned_trips)
    # user added to list of trip's members
    assert u.id in list(i.id for i in bpt.members)


def test_create_bekpaktrip_unregistered(db: Session):
    owner = create_random_user(db)
    btc = BekpackTripCreate(
        name=random_lower_name(),
        description=random_lower_string(),
        color=get_random_color(),
    )
    bpt = bekpacktrip.create_with_owner(db, obj_in=btc, owner=owner)
    assert bpt.owner.owner_id == owner.id
    u = bekpackuser.get(db=db, id=bpt.owner.id, user=bpt.owner.owner)
    assert u
    # trip added to users's list of owned trips
    assert bpt.id in list(i.id for i in u.owned_trips)
    # user added to list of trip's members
    assert u.id in list(i.id for i in bpt.members)


def test_create_multiple_bekpacktrip(db: Session):

    bp_user = get_bekpack_user(db)
    # create five trips
    names = [random_lower_name() for i in range(5)]
    trips_created = sorted(
        [
            bekpacktrip.create_with_owner(
                db,
                obj_in=BekpackTripCreate(
                    name=name,
                    description=random_lower_string(),
                    color=get_random_color(),
                ),
                owner=bp_user.owner,
            )
            for name in names
        ],
        key=lambda trip: trip.id,
    )
    trips_retrieved = sorted(
        bekpacktrip.get_by_owner(db, owner_id=bp_user.owner_id),
        key=lambda trip: trip.id,
    )
    # same number of trips retrieved and created
    assert len(trips_retrieved) == len(trips_created)
    for c, r in zip(trips_created, trips_retrieved):
        assert c.id == r.id
        assert c.name == r.name
        assert c.owner_id == r.owner_id
        assert c.members == r.members


def test_delete_bekpaktrip(db: Session):
    bp_user = get_bekpack_user(db)
    btc = BekpackTripCreate(
        name=random_lower_name(),
        description=random_lower_string(),
        color=get_random_color(),
    )
    bpt_created = bekpacktrip.create_with_owner(db, obj_in=btc, owner=bp_user.owner)
    bpt_deleted = bekpacktrip.remove(db=db, id=bpt_created.id, user=bp_user.owner)
    with pytest.raises(core.SecurityError):
        # assert deleted record can't be found
        bpt_nonexistent = bekpacktrip.get(db=db, id=bpt_created.id, user=bp_user.owner)
    # deleted the very same record that was created
    assert bpt_created.id == bpt_deleted.id
    assert bpt_deleted.name == bpt_created.name
    assert bpt_deleted.owner_id == bp_user.id


def test_add_members_bekpaktrip(db: Session):
    bp_owner = get_bekpack_user(db)
    btc = BekpackTripCreate(
        name=random_lower_name(),
        description=random_lower_string(),
        color=get_random_color(),
    )
    trip_created = bekpacktrip.create_with_owner(db, obj_in=btc, owner=bp_owner.owner)
    other_members = [get_bekpack_user(db) for i in range(5)]
    for m in other_members:
        trip_created.members.append(m)
    trip_retrieved = bekpacktrip.get(db, id=trip_created.id, user=bp_owner.owner)
    assert trip_retrieved
    required_members_ids = [m.id for m in other_members] + [bp_owner.id]
    for m_r in trip_retrieved.members:
        assert m_r.id in required_members_ids


def test_update_bekpacktrip(db: Session):
    owner = get_bekpack_user(db)
    newowner = get_bekpack_user(db)
    btc = BekpackTripCreate(
        name=random_lower_name(),
        description=random_lower_string(),
        color=get_random_color(),
    )
    trip_created = bekpacktrip.create_with_owner(db, obj_in=btc, owner=owner.owner)
    new_name = random_lower_name()
    newcolor = get_random_color()
    new_is_active = False
    btc_2 = BekpackTripUpdate(
        name=new_name, color=newcolor, is_active=new_is_active, owner_id=newowner.id
    )
    trip_updated = bekpacktrip.update(
        db=db, db_obj=trip_created, obj_in=btc_2, user=owner.owner
    )
    # assert same record
    assert trip_created.id == trip_updated.id
    assert trip_created.owner_id == trip_updated.owner_id
    # assert properties changed
    assert trip_updated.owner_id == newowner.id
    assert trip_updated.name == new_name
    assert trip_updated.is_active == new_is_active
    assert trip_updated.color.lower() == newcolor.lower()


def test_change_owner_bekpaktrip(db: Session):
    bp_user_owner = get_bekpack_user(db)
    bp_user_newowner = get_bekpack_user(db)
    btc = BekpackTripCreate(name=random_lower_name(), description=random_lower_string())
    created = bekpacktrip.create_with_owner(db, obj_in=btc, owner=bp_user_owner.owner)
    update = BekpackTripUpdate(owner_id=bp_user_newowner.id)
    updated = bekpacktrip.update(
        db, db_obj=created, obj_in=update, user=bp_user_owner.owner
    )


def test_get_joined_by_member_bekpaktrip(db: Session):
    owner = get_bekpack_user(db)
    trips = [create_random_trip(db=db, bekpack_user=owner) for _ in range(10)]
    found: List[BekpackTrip] = crud.bekpacktrip.get_joined_by_member(
        db=db, member_id=owner.id
    )
    found_ids = [i.id for i in found]
    assert set(found_ids) == set(t.id for t in trips)


def test_get_by_owner_bekpaktrip(db: Session):
    owner_bpuser = get_bekpack_user(db)
    trips = [create_random_trip(db=db, bekpack_user=owner_bpuser) for _ in range(10)]
    found: List[BekpackTrip] = crud.bekpacktrip.get_by_owner(
        db=db, owner_id=owner_bpuser.owner_id
    )
    found_ids = [i.id for i in found]
    assert set(found_ids) == set(t.id for t in trips)


def test_user_can_read_bekpacktrip(db: Session):
    bpuser1 = get_bekpack_user(db)
    bpuser2 = get_bekpack_user(db)

    trip = create_random_trip(db, bpuser1)
    crud.bekpacktrip.get(db=db, id=trip.id, user=bpuser1.owner)

    with pytest.raises(core.SecurityError):
        crud.bekpacktrip.get(db=db, id=trip.id, user=bpuser2.owner)
