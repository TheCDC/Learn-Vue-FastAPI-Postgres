from app.tests.utils.user import create_random_user
from sqlalchemy.orm import Session
from app.crud import bekpackuser
from app.schemas import BekPackUserCreate
from app.models.bekpack import BekpackTrip
from random import choice


def get_bekpack_user(db: Session) -> BekpackTrip:
    bpuser_in = BekPackUserCreate()
    user = create_random_user(db)
    bpuser = bekpackuser.create_with_owner(db, obj_in=bpuser_in, owner_id=user.id)
    return bpuser


def get_random_color() -> str:
    legal = "1234567890abcdefABCDEF"
    return "#" + "".join(choice(legal) for _ in range(6))
