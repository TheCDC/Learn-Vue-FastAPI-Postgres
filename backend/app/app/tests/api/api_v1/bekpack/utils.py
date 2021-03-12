from app.core.config import settings
from app.tests.utils.user import create_random_user
from sqlalchemy.orm.session import Session
from starlette.testclient import TestClient
from app import crud


def get_bekpack_user(db: Session, owner=None):
    if not owner:
        owner = create_random_user(db=db)
    user = crud.bekpackuser.create_with_owner(db=db, owner_id=owner.id)
    return user
