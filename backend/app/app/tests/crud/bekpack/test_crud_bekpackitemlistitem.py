import pytest
from sqlalchemy.orm import Session, aliased

from app import crud, models, schemas
from app.core.security import SecurityError
from app.schemas.bekpack.bekpackitemlistitem import (
    BekpackItemListItemCreate,
    BekpackItemListItemUpdate,
)
from app.tests.crud.bekpack.utils import get_bekpack_user, get_random_color
from app.tests.utils.bekpack import (
    create_random_bekpackuser,
    create_random_itemlist,
    create_random_trip,
)
from app.tests.utils.user import create_random_user, get_superuser
from app.tests.utils.utils import random_lower_string


def test_create_bekpackitemlistitem_unauthorized(
    db: Session, user_registered_random: models.User
) -> None:
    itemlist = create_random_itemlist(db)
    with pytest.raises(SecurityError):
        pass
        obj = crud.bekpackitemlistitem.create_with_itemlist(
            db=db,
            obj_in=BekpackItemListItemCreate(
                description=random_lower_string(),
                name=random_lower_string(),
                quantity=1,
            ),
            parent_itemlist_id=itemlist.id,
            user=user_registered_random,
        )


def test_create_bekpackitemlistitem(
    db: Session, user_registered_random: models.User
) -> None:
    itemlist = create_random_itemlist(db)
    owner = itemlist.parent_trip.owner.owner
    obj = crud.bekpackitemlistitem.create_with_itemlist(
        db=db,
        obj_in=BekpackItemListItemCreate(
            description=random_lower_string(), name=random_lower_string(), quantity=1
        ),
        parent_itemlist_id=itemlist.id,
        user=owner,
    )
    assert obj
    assert obj.parent_list_id == itemlist.id
    assert obj.bag_id == None


def test_create_with_itemlist_unauthorized(
    db: Session, user_registered_random: models.User
) -> None:
    itemlist = create_random_itemlist(db)
    owner = itemlist.parent_trip.owner.owner
    with pytest.raises(SecurityError):
        obj = crud.bekpackitemlistitem.create_with_itemlist(
            db=db,
            obj_in=BekpackItemListItemCreate(
                description=random_lower_string(),
                name=random_lower_string(),
                quantity=1,
            ),
            parent_itemlist_id=itemlist.id,
            user=user_registered_random,
        )


def test_create_bekpackitemlistitem_parent_nonexistent(
    db: Session, user_registered_random: models.User
) -> None:
    itemlist = create_random_itemlist(db)
    owner = itemlist.parent_trip.owner.owner
    with pytest.raises(SecurityError):
        crud.bekpackitemlistitem.create_with_itemlist(
            db=db,
            obj_in=BekpackItemListItemCreate(
                description=random_lower_string(),
                name=random_lower_string(),
                quantity=1,
            ),
            parent_itemlist_id=-1,
            user=owner,
        )


def test_read_bekpackitemlistitem_unauthorized(
    db: Session, user_registered_random: models.User
) -> None:
    itemlist = create_random_itemlist(db)
    owner = itemlist.parent_trip.owner.owner
    obj = crud.bekpackitemlistitem.create_with_itemlist(
        db=db,
        obj_in=BekpackItemListItemCreate(
            description=random_lower_string(), name=random_lower_string(), quantity=1
        ),
        parent_itemlist_id=itemlist.id,
        user=owner,
    )
    with pytest.raises(SecurityError):
        crud.bekpackitemlistitem.update(
            db=db,
            db_obj=obj,
            obj_in=BekpackItemListItemUpdate(),
            user=user_registered_random,
        )


def test_read_bekpackitemlistitem_superuser(
    db: Session, superuser: models.User
) -> None:
    itemlist = create_random_itemlist(db)
    owner = itemlist.parent_trip.owner.owner
    obj = crud.bekpackitemlistitem.create_with_itemlist(
        db=db,
        obj_in=BekpackItemListItemCreate(
            description=random_lower_string(), name=random_lower_string(), quantity=1
        ),
        parent_itemlist_id=itemlist.id,
        user=owner,
    )
    assert obj
    assert obj
    assert crud.bekpackitemlistitem.get(db=db, id=obj.id, user=superuser)
    assert crud.bekpackitemlistitem.update(
        db=db,
        db_obj=obj,
        obj_in=BekpackItemListItemUpdate(),
        user=superuser,
    )


def test_get_multi_by_itemlist(db: Session):
    itemlist = create_random_itemlist(db)
    user = itemlist.parent_user.owner
    items = [
        crud.bekpackitemlistitem.create_with_itemlist(
            db=db,
            obj_in=schemas.BekpackItemListItemCreate(name=random_lower_string()),
            parent_itemlist_id=itemlist.id,
            user=user,
        )
        for _ in range(16)
    ]
    ids_created = set(i.id for i in items)
    found = list(
        crud.bekpackitemlistitem.get_multi_by_itemlist(
            db=db, parent_itemlist_id=itemlist.id, user=user
        )
    )
    print(found, found[0], type(found[0]))
    assert found
    assert isinstance(found[0], models.BekpackItemListItem)
    ids_found = set(i.id for i in found)
    assert ids_created == ids_found
