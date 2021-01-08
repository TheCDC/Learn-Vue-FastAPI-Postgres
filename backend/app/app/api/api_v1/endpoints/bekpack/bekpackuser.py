from typing import Any, List

import sqlalchemy
from app import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import bekpackuser as crud_bekpackuser
from app.crud import bekpacktrip as crud_bekpacktrip
from app.crud import user as crud_user
from app.models.bekpack import BekpackUser
from app.models import User
import app.schemas as schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.BekPackUser)
def create_bekpackuser(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.BekPackUserCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new BekpackUser"""
    try:
        bp_user = crud_bekpackuser.create_with_owner(
            db=db, obj_in=user_in, owner_id=current_user.id
        )
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=404, detail="BekpackUser already exists")
    return bp_user


@router.get("/me", response_model=schemas.BekPackUser)
def get_bekpackuser_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get a BekpackUser"""
    try:
        bp_user = crud_bekpackuser.get_by_owner(db=db, owner_id=current_user.id)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not bp_user:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not crud_user.is_superuser(current_user) and (
        current_user.id != bp_user.owner_id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return bp_user


@router.delete("/me", response_model=schemas.BekPackUser)
def delete_bekpackuser_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete a BekpackUser"""
    try:
        bp_user = crud_bekpackuser.get_by_owner(db=db, owner_id=current_user.id)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not bp_user:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not crud_user.is_superuser(current_user) and (
        current_user.id != bp_user.owner_id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    bp_user = crud_bekpackuser.remove(db=db, id=bp_user.id)
    return bp_user


@router.get("/owned_trips", response_model=List[schemas.BekpackTrip])
def get_my_owned_BekPackTrips(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Get a BekpackUser"""
    try:
        bp_user = crud_bekpackuser.get_by_owner(db=db, owner_id=current_user.id)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not bp_user:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    return crud_bekpacktrip.get_by_owner(
        db=db, owner_id=bp_user.id, skip=skip, limit=limit
    )


@router.get("/joined_trips", response_model=List[schemas.BekpackTrip])
def get_my_joined_BekPackTrips(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Get a BekpackUser"""
    try:
        bp_user = crud_bekpackuser.get_by_owner(db=db, owner_id=current_user.id)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not bp_user:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    return crud_bekpacktrip.get_joined_by_member(
        db=db, member_id=bp_user.id, skip=skip, limit=limit
    )


@router.get("/{id}", response_model=schemas.BekPackUser)
def get_bekpackuser_by_id(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get a BekpackUser"""
    bp_user = crud_bekpackuser.get(db=db, id=id)
    if not bp_user:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not crud_user.is_superuser(current_user) and (
        current_user.id != bp_user.owner_id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return bp_user


@router.delete("/{id}", response_model=schemas.BekPackUser)
def delete_bekpackuser(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete a BekpackUser"""
    bp_user = crud_bekpackuser.get(db=db, id=id)
    if not bp_user:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if not crud_user.is_superuser(current_user) and (
        current_user.id != bp_user.owner_id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    bp_user = crud_bekpackuser.remove(db=db, id=id)
    return bp_user
