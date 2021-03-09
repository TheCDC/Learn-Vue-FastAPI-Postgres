from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import models
from app.crud.base import CRUDBase
from app.models.bekpack import BekpackUser
from app.schemas import BekPackUserCreate, BekPackUserUpdate


class CRUDBekpackUser(CRUDBase[BekpackUser, BekPackUserCreate, BekPackUserUpdate]):
    def create_with_owner(self, db: Session, *, owner_id: int) -> BekpackUser:
        db_obj = self.model(owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_owner(self, db: Session, *, owner_id: int) -> BekpackUser:
        return (
            db.query(self.model).filter(BekpackUser.owner_id == owner_id).one_or_none()
        )

    def user_can_read(self, db: Session, *, id: int, user: models.User) -> bool:
        return True

    def user_can_write(self, db: Session, *, id: int, user: models.User) -> bool:
        obj: models.BekpackUser = db.query(self.model).filter(self.model.id == id).one()
        if not obj:
            return False
        return obj.owner_id == user.id


bekpackuser = CRUDBekpackUser(BekpackUser)
