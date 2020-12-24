from app.tests.utils.user import create_random_user
from app.tests.utils.item import random_lower_string
from sqlalchemy.orm import Session
from app.schemas import BekpackTripCreate
from app.crud import bekpacktrip
from app.models.bekpack import BekpackUser
from .utils import get_bekpack_user


def test_create_bekpaktrip(db: Session):
    bp_user = get_bekpack_user(db)
    btc = BekpackTripCreate(name=random_lower_string())
    bpt = bekpacktrip.create_with_owner(db, obj_in=btc, owner_id=bp_user.id)
    assert bpt.owner_id == bp_user.id
    u: BekpackUser = db.query(BekpackUser).filter(BekpackUser.id == bp_user.id).one()
    # trip added to users's list of owned trips
    assert bpt.id in list(i.id for i in u.owned_trips)
    # user added to list of trip's members
    assert u.id in list(i.id for i in bpt.members)


def test_create_multiple_bekpacktrip(db: Session):
    bp_user = get_bekpack_user(db)
    # create five trips
    names = [random_lower_string() for i in range(5)]
    trips_created = [
        bekpacktrip.create_with_owner(
            db, obj_in=BekpackTripCreate(name=name), owner_id=bp_user.id
        )
        for name in names
    ]
    trips_retrieved = bekpacktrip.get_by_owner(db, owner_id=bp_user.id)
    # same number of trips retrieved and created
    assert len(trips_retrieved) == len(trips_created)
    for c, r in zip(trips_created, trips_retrieved):
        assert c.id == r.id
        assert c.name == r.name
        assert c.owner_id == r.owner_id
        assert c.members == r.members


def test_delete_bekpaktrip(db: Session):
    bp_user = get_bekpack_user(db)
    btc = BekpackTripCreate(name=random_lower_string())
    bpt_created = bekpacktrip.create_with_owner(db, obj_in=btc, owner_id=bp_user.id)
    bpt_deleted = bekpacktrip.remove(db=db, id=bpt_created.id)
    bpt_nonexistent = bekpacktrip.get(db=db, id=bpt_created.id)
    # assert deleted record can't be found
    assert bpt_nonexistent is None
    # deleted the very same record that was created
    assert bpt_created.id == bpt_deleted.id
    assert bpt_deleted.name == bpt_created.name
    assert bpt_deleted.owner_id == bp_user.id


def test_add_members(db: Session):
    owner = get_bekpack_user(db)
    btc = BekpackTripCreate(name=random_lower_string())
    trip_created = bekpacktrip.create_with_owner(db, obj_in=btc, owner_id=owner.id)
    other_members = [get_bekpack_user(db) for i in range(5)]
    for m in other_members:
        trip_created.members.append(m)
    trip_retrieved = bekpacktrip.get(db, id=trip_created.id)
    required_members_ids = [m.id for m in other_members] + [owner.id]
    for m_r in trip_retrieved.members:
        assert m_r.id in required_members_ids