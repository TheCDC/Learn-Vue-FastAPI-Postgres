from typing import Generator
import pytest
from sqlalchemy.orm.session import Session

from app.models.bekpack import BekpackUser
from app.models.user import User
from app.tests.utils.bekpack import create_random_bekpackuser
from app import crud


@pytest.fixture(scope="function")
def user_registered_random(db: Session) -> Generator[User, None, None]:
    bpuser = create_random_bekpackuser(db)
    yield bpuser.owner
    crud.bekpackuser.remove(db=db, id=bpuser.id)
    crud.user.remove(db=db, id=bpuser.owner.id)


@pytest.fixture(scope="module")
def user_registered_constant(db: Session) -> Generator[User, None, None]:
    bpuser = create_random_bekpackuser(db)
    yield bpuser.owner
    crud.bekpackuser.remove(db=db, id=bpuser.id)
    crud.user.remove(db=db, id=bpuser.owner.id)
