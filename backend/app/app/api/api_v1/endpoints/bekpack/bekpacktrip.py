from typing import Any, List

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate
from sqlalchemy.orm import Session

import app.api.api_v1.endpoints.bekpack.deps as deps_bekpack
import app.schemas as schemas
from app.api import deps
from app.crud import bekpacktrip as crud_bekpacktrip
from app.crud import bekpacktripitemlist as crud_bekpackitemlist
from app.crud import bekpackuser as crud_bekpackuser
from app.crud import user as crud_user
from app.models import User
from app.models.bekpack import BekpackUser

router = APIRouter()


@router.get(
    "/",
    response_model=Page[schemas.BekpackTrip],
    dependencies=[Depends(pagination_params)],
)
def get_my_bakpacktrips(
    *,
    db: Session = Depends(deps.get_db),
    bekpack_user: BekpackUser = Depends(deps_bekpack.get_bekpack_user),
    current_user: User = Depends(deps.get_current_active_user),
) -> List[schemas.BekpackTrip]:
    if crud_user.is_superuser(current_user):
        return paginate(crud_bekpacktrip.get_all(db=db))
    records = crud_bekpacktrip.get_by_owner(db=db, owner_id=bekpack_user.id)
    return paginate(records)


@router.get("/{id}", response_model=schemas.BekpackTrip)
def get_bekpacktrip_by_id(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
    bekpack_user: BekpackUser = Depends(deps_bekpack.get_bekpack_user),
) -> schemas.BekpackTrip:
    trip = crud_bekpacktrip.get(db=db, id=id)
    if not trip:
        raise HTTPException(status_code=404, detail="BekpackTrip not found")
    if not crud_user.is_superuser(current_user) and (
        not crud_bekpacktrip.is_owned_by_bekpackuser(
            db=db, member_id=bekpack_user.id, id=id
        )
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return trip


@router.get(
    "/{trip_id}/lists",
    response_model=Page[schemas.BekpackTripItemList],
    dependencies=[Depends(pagination_params)],
)
def get_bekpacktrip_lists(
    *,
    db: Session = Depends(deps.get_db),
    bekpack_user: BekpackUser = Depends(deps_bekpack.get_bekpack_user),
    current_user: User = Depends(deps.get_current_active_user),
    trip_id: int,
) -> List[schemas.BekpackTrip]:
    if not crud_user.is_superuser(
        current_user
    ) and not crud_bekpacktrip.is_owned_by_bekpackuser(
        db=db, id=trip_id, member_id=bekpack_user.id
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    records = crud_bekpackitemlist.get_by_trip(db=db, trip_id=trip_id)
    return paginate(records)


@router.put("/{id}", response_model=schemas.BekpackTrip)
def update_bekpacktrip(
    *,
    db: Session = Depends(deps.get_db),
    trip_in: schemas.BekpackTripUpdate,
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
    bekpack_user: BekpackUser = Depends(deps_bekpack.get_bekpack_user),
) -> Any:
    trip = crud_bekpacktrip.get(db=db, id=id)
    if not trip:
        raise HTTPException(status_code=404, detail="BekpackTrip not found")
    if not crud_user.is_superuser(current_user) and (
        not crud_bekpacktrip.is_owned_by_bekpackuser(
            db=db, id=trip.id, member_id=bekpack_user.id
        )
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    trip = crud_bekpacktrip.update(db=db, db_obj=trip, obj_in=trip_in)
    return trip


@router.delete("/{id}", response_model=schemas.BekpackTrip)
def delete_bekpacktrip(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    pass
    """
    Delete a BekpackTrip.
    """
    trip = crud_bekpacktrip.get(db=db, id=id)
    if not trip:
        raise HTTPException(status_code=404, detail="BekpackTrip not found")
    if not crud_user.is_superuser(current_user) and (
        trip.owner.owner_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    trip = crud_bekpacktrip.remove(db=db, id=id)
    return trip


@router.post("/", response_model=schemas.BekpackTrip)
def create_bekpacktrip(
    *,
    db: Session = Depends(deps.get_db),
    trip_in: schemas.BekpackTripCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new BekpackTrip"""
    try:
        owner_bekpack_user = crud_bekpackuser.get_by_owner(
            db=db, owner_id=current_user.id
        )
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="User not registered for BekPack")
    trip = crud_bekpacktrip.create_with_owner(
        db=db, obj_in=trip_in, owner_id=owner_bekpack_user.id
    )

    return trip
