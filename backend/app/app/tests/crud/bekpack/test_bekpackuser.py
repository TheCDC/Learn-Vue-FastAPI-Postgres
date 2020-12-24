from app.tests.utils.user import create_random_user
from sqlalchemy.orm import Session
from app.schemas import BekPackUserCreate
from app.crud import bekpackuser


def test_create_bekpackuser(db: Session) -> None:
    bpuser_in = BekPackUserCreate()
    user = create_random_user(db)
    bpuser = bekpackuser.create_with_owner(db, obj_in=bpuser_in, owner_id=user.id)
    assert bpuser.owner_id == user.id


def test_get_bekpackuser_by_owner(db: Session):
    bpuser_in = BekPackUserCreate()
    user = create_random_user(db)
    bpuser = bekpackuser.create_with_owner(db, obj_in=bpuser_in, owner_id=user.id)
    assert bpuser.owner_id == user.id
    got = bekpackuser.get_by_owner(db, owner_id=user.id)
    assert got.owner_id == user.id
