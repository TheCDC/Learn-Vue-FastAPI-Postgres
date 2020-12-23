from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.bekpack import BekpackUser
from app.schemas import BekPackUserCreate, BekPackUserUpdate


class CRUDBekpackUser(CRUDBase[BekpackUser, BekPackUserCreate, BekPackUserUpdate]):
    pass


bekpackuser = CRUDBekpackUser(BekpackUser)