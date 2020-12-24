from app.tests.utils.user import create_random_user
from sqlalchemy.orm import Session
from app import crud
from app.schemas import BekPackUserCreate
from app.models.bekpack import BekpackTrip


def get_bekpack_user(db: Session) -> BekpackTrip:
    bpuser_in = BekPackUserCreate()
    user = create_random_user(db)
    bpuser = crud.bekpackuser.create_with_owner(db, obj_in=bpuser_in, owner_id=user.id)
    return bpuser