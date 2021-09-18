from typing import List, Type

from sqlalchemy.orm import Query, Session

from app import models
from app.crud.base import CRUDBaseSecure
from app.db.base_class import Base
from app.models.bekpack import BekpackUser
from app.schemas import BekpackUserCreate, BekpackUserUpdate


class CRUDBekpackUser(
    CRUDBaseSecure[BekpackUser, BekpackUserCreate, BekpackUserUpdate]
):
    def _get_base_query_user_can_read(
        self,
        db: Session,
        *,
        models_to_include: List[Type[Base]] = [],
        user: models.User,
    ) -> Query:
        # mti: List[Type[Base]] = [self.model]
        # mti.extend(models_to_include)
        return db.query(self.model)

    def _get_base_query_user_can_write(
        self,
        db: Session,
        *,
        models_to_include: List[Type[Base]] = [],
        user: models.User,
    ) -> Query:
        # mti: List[Type[Base]] = [self.model]
        # mti.extend(models_to_include)
        if user.is_superuser:
            return db.query(self.model)
        return db.query(self.model).filter(self.model.owner_id == user.id)

    def create_with_owner(self, db: Session, *, owner_id: int) -> BekpackUser:
        db_obj = self.model(owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_owner(self, db: Session, *, owner_id: int) -> BekpackUser:
        bp_user = (
            db.query(self.model).filter(BekpackUser.owner_id == owner_id).one_or_none()
        )
        if not bp_user:
            bp_user = self.create_with_owner(db=db, owner_id=owner_id)
        return bp_user


bekpackuser = CRUDBekpackUser(BekpackUser)
