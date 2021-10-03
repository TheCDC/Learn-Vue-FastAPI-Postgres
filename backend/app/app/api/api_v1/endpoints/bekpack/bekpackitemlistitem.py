from typing import Any, List, Optional

from fastapi import Depends, HTTPException
from fastapi_pagination.page import Page
from fastapi_pagination.api import pagination_params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.paginator import paginate
from sqlalchemy.orm import Session
from app.crud.crud_bekpack.crud_bekpackitemlistitem import CRUDBekpackItemListItem

import app.schemas as schemas
from app import crud, models, schemas
from app.api import deps
from app.api.api_v1 import DefaultCrudRouter
from app.crud.crud_bekpack.crud_bekpacktrip import CRUDBekpackTrip
from app.models import User
from app.schemas.bekpack.bekpackitemlistitem import (
    BekpackItemListItem,
    BekpackItemListItemCreate,
    BekpackItemListItemUpdate,
)

router = DefaultCrudRouter[
    models.BekpackItemListItem,
    CRUDBekpackItemListItem,
    BekpackItemListItem,
    BekpackItemListItemUpdate,
](
    model=models.BekpackItemListItem,
    crud=crud.bekpackitemlistitem,
    read_schema=BekpackItemListItem,
    update_schema=BekpackItemListItemUpdate,
)


@router.post("/", response_model=BekpackItemListItem)
def create_bekpackitemlistitem(
    *,
    parent_itemlist_id: int,
    bag_id: Optional[int] = None,
    db: Session = Depends(deps.get_db),
    obj_in: BekpackItemListItemCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> models.BekpackItemListItem:

    """Create new BekpackItemListItem"""
    return crud.bekpackitemlistitem.create_with_itemlist(
        db=db,
        obj_in=obj_in,
        parent_itemlist_id=parent_itemlist_id,
        bag_id=bag_id,
        user=current_user,
    )
