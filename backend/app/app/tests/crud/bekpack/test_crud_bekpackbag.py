from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.tests.utils.bekpack import create_random_trip
from pydantic.color import Color

from app.tests.utils.utils import random_lower_string


def test_crud_bekpackbag_create_with_trip(
    db: Session, user_registered_random: models.User
) -> None:
    trip = create_random_trip(db=db)
    obj = schemas.BekpackBagCreate(
        color=Color("FFFFFF"),
        name=random_lower_string(),
    )
    crud.bekpackbag.create_with_trip(
        db=db,
        obj_in=obj,
        user=trip.owner.owner,
        owner_id=trip.owner.owner.id,
        owner_trip_id=trip.id,
    )
