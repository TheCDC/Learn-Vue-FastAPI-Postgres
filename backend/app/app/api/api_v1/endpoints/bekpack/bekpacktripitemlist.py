from typing import Any, List
from app.api.api_v1 import DefaultCrudRouter
from app.crud.crud_bekpack.crud_bekpackitemlist import CRUDBekpackItemList

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate
from sqlalchemy.orm import Session

import app.api.api_v1.endpoints.bekpack.deps as deps_bekpack
import app.schemas as schemas
from app.api import deps
from app.crud import bekpacktrip as crud_bekpacktrip
from app.crud import bekpackitemlist as crud_bekpackitemlist
from app.crud import bekpackuser as crud_bekpackuser
from app.crud import user as crud_user
from app.models import User
from app.models.bekpack import BekpackUser
from app import models, crud, schemas

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


@router.get(
    "/{list_id}",
    response_model=Page[schemas.BekpackItemList],
    dependencies=[Depends(pagination_params)],
)
def get_bekpacktrip_lists(
    *,
    db: Session = Depends(deps.get_db),
    bekpack_user: BekpackUser = Depends(deps_bekpack.get_bekpack_user),
    current_user: User = Depends(deps.get_current_active_user),
    list_id: int,
) -> List[schemas.BekpackTrip]:
    if not crud_user.is_superuser(
        current_user
    ) and not crud_bekpackitemlist.is_owned_by_bekpackuser(
        db=db, list_id=list_id, member_id=bekpack_user.id
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    records = crud_bekpackitemlist.get(db=db, id=list_id)
    return paginate(records)
