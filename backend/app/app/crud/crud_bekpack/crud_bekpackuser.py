from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.bekpack import BekpackUser
from app.schemas import BekPackUserCreate, BekPackUserUpdate


class CRUDBekpackUser(CRUDBase[BekpackUser, BekPackUserCreate, BekPackUserUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: BekPackUserCreate, owner_id: int
    ) -> BekpackUser:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_owner(self, db: Session, *, owner_id: int) -> BekpackUser:
        return db.query(self.model).filter(BekpackUser.owner_id == owner_id).one()


bekpackuser = CRUDBekpackUser(BekpackUser)