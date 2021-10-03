from typing import Any, List

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.page import Page
from fastapi_pagination.api import pagination_params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.paginator import paginate
from sqlalchemy.orm import Session

import app.api.api_v1.endpoints.bekpack.deps as deps_bekpack
import app.schemas as schemas
from app import crud, models, schemas
from app.api import deps
from app.api.api_v1 import DefaultCrudRouter
from app.crud import user as crud_user
from app.crud.crud_bekpack.crud_bekpackitemlist import CRUDBekpackItemList
from app.models import User
from app.models.bekpack import BekpackUser

router = DefaultCrudRouter[
    models.BekpackItemList,
    CRUDBekpackItemList,
    schemas.BekpackItemList,
    schemas.BekpackItemListUpdate,
](
    model=models.BekpackItemList,
    crud=crud.bekpackitemlist,
    read_schema=schemas.BekpackItemList,
    update_schema=schemas.BekpackItemListUpdate,
)


@router.post("/", response_model=schemas.BekpackItemList)
def create_bekpackitemlist(
    *,
    parent_trip_id: int,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.BekpackItemListCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> models.BekpackItemList:
    """Create new BekpackItemListItem"""
    return crud.bekpackitemlist.create_with_trip_owner(
        db=db,
        obj_in=obj_in,
        parent_trip_id=parent_trip_id,
        parent_user_id=current_user.id,
    )
