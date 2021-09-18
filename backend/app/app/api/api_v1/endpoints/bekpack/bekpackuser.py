from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.page import Page
from fastapi_pagination.paginator import paginate

import sqlalchemy
from app import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User
import app.schemas as schemas
from app.api import deps
from app import models, crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.BekpackUser)
def create_bekpackuser(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> models.BekpackUser:
    """Create new BekpackUser"""
    try:
        bp_user = crud.bekpackuser.create_with_owner(db=db, owner_id=current_user.id)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=409, detail="BekpackUser already exists")
    return bp_user


@router.get("/me", response_model=schemas.BekpackUser)
def get_bekpackuser_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> models.BekpackUser:
    """Get a BekpackUser"""
    try:
        bp_user = crud.bekpackuser.get_by_owner(db=db, owner_id=current_user.id)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not bp_user:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not crud.user.is_superuser(current_user) and (
        current_user.id != bp_user.owner_id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return bp_user


@router.delete("/me", response_model=schemas.BekpackUser)
def delete_bekpackuser_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> models.BekpackUser:
    """Delete a BekpackUser"""
    try:
        bp_user = crud.bekpackuser.get_by_owner(db=db, owner_id=current_user.id)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not bp_user:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not crud.user.is_superuser(current_user) and (
        current_user.id != bp_user.owner_id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    bp_user = crud.bekpackuser.remove(db=db, id=bp_user.id, user=current_user)
    return bp_user


@router.get("/owned_trips", response_model=Page[schemas.BekpackTrip])
def get_my_owned_BekPackTrips(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> AbstractPage[models.BekpackTrip]:
    """Get a BekpackUser"""
    try:
        bp_user = crud.bekpackuser.get_by_owner(db=db, owner_id=current_user.id)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not bp_user:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    return paginate(crud.bekpacktrip.get_by_owner(db=db, owner_id=bp_user.id))


@router.get("/joined_trips", response_model=Page[schemas.BekpackTrip])
def get_my_joined_BekPackTrips(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> AbstractPage[models.BekpackTrip]:
    """Get a BekpackUser"""
    try:
        bp_user = crud.bekpackuser.get_by_owner(db=db, owner_id=current_user.id)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not bp_user:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    return paginate(
        crud.bekpacktrip.get_joined_by_member(
            db=db,
            member_id=bp_user.id,
        )
    )
