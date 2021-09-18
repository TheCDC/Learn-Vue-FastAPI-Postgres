import pytest
from sqlalchemy.orm import Session, aliased

from app import crud, models, schemas
from app.core.security import SecurityError
from app.schemas.bekpack.bekpackitemlistitem import BekpackItemListItemCreate
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
