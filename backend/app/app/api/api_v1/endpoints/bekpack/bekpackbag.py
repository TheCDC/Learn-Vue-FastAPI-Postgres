from typing import Any, List, Optional

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
