from typing import Any, List
from app.crud.crud_bekpack import crud_bekpackuser

import sqlalchemy
from app import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import bekpacktrip as crud_bekpacktrip
from app.crud import bekpackuser as crud_bekpackuser
from app.crud import user as crud_user
from app.models.bekpack import BekpackTrip, BekpackUser
from app.models import User
import app.schemas as schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.BekpackTrip)
def create_bekpacktrip(
    *,
    db: Session = Depends(deps.get_db),
    trip_in: schemas.BekpackTripCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new BekpackTrip"""
    try:
        owner = crud_bekpackuser.get_by_owner(db=db, owner_id=current_user.id)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="User not registered for BekPack")
    trip = crud_bekpacktrip.create_with_owner(db=db, obj_in=trip_in, owner_id=owner.id)

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
    if not crud_user.is_superuser(current_user) and (trip.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    trip = crud_bekpacktrip.remove(db=db, id=id)
    return trip


@router.put("/{id}", response_model=schemas.BekpackTrip)
def update_bekpacktrip(
    *,
    db: Session = Depends(deps.get_db),
    trip_in: schemas.BekpackTripUpdate,
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    trip = crud_bekpacktrip.get(db=db, id=id)
    if not trip:
        raise HTTPException(status_code=404, detail="BekpackTrip not found")
    if not crud_user.is_superuser(current_user) and (trip.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    trip = crud_bekpacktrip.update(db=db, db_obj=trip, obj_in=trip_in)


@router.get("/", response_model=List[schemas.BekpackTrip])
def get_bakpacktrips(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> List[schemas.BekpackTrip]:
    try:
        owner = crud_bekpackuser.get_by_owner(db=db, owner_id=current_user.id)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="User not registered for BekPack")

    return crud_bekpacktrip.get_by_owner(db=db, owner_id=owner.id)
