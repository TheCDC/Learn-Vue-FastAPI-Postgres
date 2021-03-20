from sqlalchemy.orm import Session, aliased

from app import crud, models, schemas
from app.tests.crud.bekpack.utils import get_bekpack_user, get_random_color
from app.tests.utils.bekpack import (
    create_random_bekpackuser,
    create_random_itemlist,
    create_random_trip,
)
from app.tests.utils.user import create_random_user, get_superuser
from app.tests.utils.utils import random_lower_string


def test_create_bekpackitemlist(db: Session) -> None:
    user = get_bekpack_user(db=db)
    trip = create_random_trip(db=db, bekpack_user=user)

    itemlist = crud.bekpackitemlist.create_with_trip_owner(
        db=db,
        obj_in=schemas.BekpackItemListCreate(
            name=random_lower_string(), color=get_random_color()
        ),
        parent_user=user.id,
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


def test_crud_bekpacktrip__get_base_query_user_can_read_superuser(db: Session):
    su = get_superuser(db=db)
    itemlist = create_random_itemlist(db=db)
    found = (
        crud.bekpackitemlist._get_base_query_user_can_read(db=db, user=su).filter(
            models.BekpackItemList.id == itemlist.id
        )
    ).one()
    assert found
    assert found.id == itemlist.id
    assert found.name == itemlist.name


def test_crud_bekpackitemlist_user_can_read(db: Session):
    itemlist = create_random_itemlist(db=db,)
    assert crud.bekpackitemlist.user_can_read(
        db=db, id=itemlist.id, user=itemlist.parent_trip.owner.owner
    )


def test_crud_bekpackitemlist_user_can_read_unauthorized(db: Session):
    itemlist = create_random_itemlist(db=db,)
    user = create_random_user(db=db)
    assert not crud.bekpackitemlist.user_can_read(db=db, id=itemlist.id, user=user)


def test_crud_bekpackitemlist_user_can_read_superuser(db: Session):
    itemlist = create_random_itemlist(db=db,)
    su = get_superuser(db=db)
    assert crud.bekpackitemlist.user_can_read(db=db, id=itemlist.id, user=su)


def test_crud_bekpackitemlist_user_can_write_owned_trip(db: Session):
    itemlist = create_random_itemlist(db=db,)
    assert crud.bekpackitemlist.user_can_write(
        db=db, id=itemlist.id, user=itemlist.parent_trip.owner.owner
    )


def test_crud_bekpackitemlist_user_can_write_owned_list(db: Session):
    trip = create_random_trip(db=db, bekpack_user=create_random_bekpackuser(db=db))
    trip_owner = trip.owner.owner
    itemlist = create_random_itemlist(
        db=db, trip=trip, bekpack_user=create_random_bekpackuser(db=db)
    )
    list_owner = itemlist.parent_user.owner
    assert itemlist.parent_user_id != trip.owner_id
    assert crud.bekpackitemlist.user_can_write(db=db, id=itemlist.id, user=list_owner)


def test_crud_bekpackitemlist_user_can_write_unauthorized(db: Session):
    itemlist = create_random_itemlist(db=db,)
    user = create_random_user(db=db)
    assert not crud.bekpackitemlist.user_can_write(db=db, id=itemlist.id, user=user)


def test_crud_bekpackitemlist_user_can_write_superuser(db: Session):
    itemlist = create_random_itemlist(db=db,)
    su = get_superuser(db=db)
    assert crud.bekpackitemlist.user_can_write(db=db, id=itemlist.id, user=su)


def test_crud_bekpackitemlist__get_base_query_user_can_read(db: Session):
    target_record = create_random_itemlist(db=db)
    user = target_record.parent_trip.owner.owner
    model = models.BekpackItemList
    mycrud = crud.bekpackitemlist
    subquery = (
        (
            mycrud._get_base_query_user_can_read(db=db, user=user).filter(
                model.id == target_record.id
            )
        )
        .with_labels()
        .subquery()
    )
    print(f"user.id={user.id}, target_record.id={target_record.id}", subquery)
    final_query = db.query(aliased(model, subquery)).select_from(subquery)
    found = final_query.one()
    print(found)
    assert found
    assert found.id == target_record.id
    assert found.name == target_record.name
