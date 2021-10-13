from app.tests.utils.user import create_random_user
from sqlalchemy.orm import Session
from app.crud import bekpackuser
from app.schemas import BekpackUserCreate
from app.models.bekpack import BekpackTrip, BekpackUser
from random import choice


def get_bekpack_user(db: Session) -> BekpackUser:
    user = create_random_user(db)
    bpuser = bekpackuser.create_with_owner(db, owner_id=user.id)
    return bpuser


def get_random_color() -> str:
    legal = "1234567890abcdef"
    return "#" + "".join(choice(legal) for _ in range(6))
