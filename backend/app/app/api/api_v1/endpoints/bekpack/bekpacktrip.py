from typing import Any, List

from fastapi import Depends, HTTPException
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate
from sqlalchemy.orm import Session

import app.schemas as schemas
from app import crud, models, schemas
from app.api import deps
from app.api.api_v1 import DefaultCrudRouter
from app.crud.crud_bekpack.crud_bekpacktrip import CRUDBekpackTrip
from app.models import User

router = DefaultCrudRouter[
    models.BekpackTrip, CRUDBekpackTrip, schemas.BekpackTrip, schemas.BekpackTripUpdate
](
    model=models.BekpackTrip,
    crud=crud.bekpacktrip,
    read_schema=schemas.BekpackTrip,
    update_schema=schemas.BekpackTripUpdate,
)


@router.get(
    "/mine/all",
    response_model=Page[schemas.BekpackTrip],
    dependencies=[Depends(pagination_params)],
)
def get_my_bakpacktrips(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Page[schemas.BekpackTrip]:
    records = crud.bekpacktrip.get_by_owner(db=db, owner_id=current_user.id)
    return paginate(records)


@router.get(
    "/{trip_id}/lists",
    response_model=Page[schemas.BekpackItemList],
    dependencies=[Depends(pagination_params)],
)
def get_bekpacktrip_lists(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    trip_id: int,
) -> Page[schemas.BekpackTrip]:
    if not crud.bekpacktrip.user_can_read(db=db, object=id, user=current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    records = crud.bekpackitemlist.get_by_trip(db=db, trip_id=trip_id)
    return paginate(records)


@router.post("/", response_model=schemas.BekpackTrip)
def create_bekpacktrip(
    *,
    db: Session = Depends(deps.get_db),
    trip_in: schemas.BekpackTripCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new BekpackTrip"""

    trip = crud.bekpacktrip.create_with_owner(db=db, obj_in=trip_in, owner=current_user)

    return trip
