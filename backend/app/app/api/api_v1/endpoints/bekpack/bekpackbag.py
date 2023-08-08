from typing import Any, List, Optional
from app.crud.crud_bekpack.crud_bekpackbag import CRUDBekpackBag
from app.models.bekpack import BekpackBag

from fastapi import Depends, HTTPException
from fastapi_pagination.page import Page
from fastapi_pagination.api import pagination_params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.paginator import paginate
from sqlalchemy.orm import Session

import app.schemas as schemas
from app import crud, models, schemas
from app.api import deps
from app.api.api_v1 import DefaultCrudRouter
from app.models import User

router = DefaultCrudRouter[
    models.BekpackBag,
    CRUDBekpackBag,
    schemas.BekpackBag,
    schemas.BekpackBagUpdate,
](
    model=models.BekpackBag,
    crud=crud.bekpackbag,
    read_schema=schemas.BekpackBag,
    update_schema=schemas.BekpackBagUpdate,
)


@router.post("/", response_model=schemas.BekpackBag)
def create_bekpackbag(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    owner_trip_id: int,
    obj_in: schemas.BekpackBagCreate,
) -> models.BekpackBag:
    """Create a new BekpackBag"""
    return crud.bekpackbag.create_with_trip(
        db=db,
        user=current_user,
        obj_in=obj_in,
        owner_trip_id=owner_trip_id,
        owner_id=current_user.id,
    )


@router.get("/select", response_model=List[schemas.BekpackBag])
def get_multi_bekpackbag_by_trip(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    trip_id: int,
) -> List[models.BekpackBag]:
    return []
    return crud.bekpackbag.get_multi_by_trip(
        db=db, owner_trip_id=trip_id, user=current_user
    )
