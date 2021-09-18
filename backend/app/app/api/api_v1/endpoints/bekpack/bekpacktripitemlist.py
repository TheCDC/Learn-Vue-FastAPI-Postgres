from typing import Any, List

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, pagination_params
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
