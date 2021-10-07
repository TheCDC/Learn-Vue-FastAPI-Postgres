from typing import Any, List

from fastapi import Depends
from sqlalchemy.orm import Session

import app.schemas as schemas
from app import crud, models, schemas
from app.api import deps
from app.api.api_v1 import DefaultCrudRouter
from app.crud.crud_bekpack.crud_bekpackitemlist import CRUDBekpackItemList
from app.models import User

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


@router.get("/{id}/items", response_model=List[schemas.BekpackItemListItem])
def get_bekpackitemlist_items(
    *,
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    return crud.bekpackitemlistitem.get_multi_by_itemlist(
        db=db, parent_itemlist_id=id, user=current_user
    )
