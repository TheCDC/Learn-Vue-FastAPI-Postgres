from app.tests.utils.user import create_random_user
from sqlalchemy.orm import Session
from app import crud
from app.schemas import BekPackUserCreate


# def test_create_bekpackuser(db: Session) -> None:
#     bpuser_in = BekPackUserCreate()
#     user = create_random_user(db)
#     bpuser = crud.bekpackuser.create_with_owner(db, obj_in=bpuser_in, owner_id=user.id)
#     assert bpuser.owner_id == user.id
