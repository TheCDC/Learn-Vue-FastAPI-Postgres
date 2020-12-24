from typing import Any, List
from app import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import bekpackuser as crud_bekpackuser
from app.models.bekpack import BekpackUser
from app.schemas.bekpack import bekpackuser
from app.api import deps

router = APIRouter()


@router.post("/", response_model=bekpackuser.BekPackUser)
def create_bekpackuser(
    *,
    db: Session = Depends(deps.get_db),
    user_in: bekpackuser.BekPackUserCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    bp_user = crud_bekpackuser.create_with_owner(
        db, obj_in=user_in, owner_id=current_user.id
    )
    return bp_user


@router.delete("/{id}", response_model=bekpackuser.BekPackUser)
def delete_bekpackuser(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    bp_user = crud_bekpackuser.get(db=db, id=id)
    if not bp_user:
        raise HTTPException(status_code=404, detail="BekpackUser not found")
    if current_user.id != bp_user.owner_id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    bp_user = crud_bekpackuser.remove(db=db, id=id)
    return bp_user
