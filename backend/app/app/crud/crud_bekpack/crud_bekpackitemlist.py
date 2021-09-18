from typing import List, Type
from app.db.base_class import Base

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, Query

from app.crud.base import CRUDBase
from app.models.bekpack import BekpackTrip_Members, BekpackItemList, BekpackTrip
from app.schemas import BekpackItemListCreate, BekpackItemListUpdate
from app import crud, schemas, models


class CRUDBekpackItemList(
    CRUDBase[BekpackItemList, BekpackItemListCreate, BekpackItemListUpdate]
):
    def _get_base_query_user_can_read(
        self,
        db: Session,
        *,
        models_to_include: List[Type[Base]] = [],
        user: models.User
    ) -> Query:
        if user.is_superuser:
            return db.query(self.model)
        mti: List[Type[Base]] = [self.model]
        mti.extend(models_to_include)
        return crud.bekpacktrip._get_base_query_user_can_read(
            db=db, models_to_include=mti, user=user
        ).join(self.model)

    def create_with_trip_owner(
        self,
        db: Session,
        *,
        obj_in: BekpackItemListCreate,
        parent_user: int,
        trip_id: int
    ) -> BekpackItemList:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data, parent_user_id=parent_user, parent_trip_id=trip_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_trip(self, db: Session, *, trip_id: int) -> List[BekpackItemList]:
        return (
            db.query(self.model).filter(BekpackItemList.parent_trip_id == trip_id).all()
        )

    def get_by_owner(self, db: Session, *, owner_id: int) -> List[BekpackItemList]:
        return db.query(self.model).filter(self.model.parent_user_id == owner_id).all()

    def user_can_read(self, db: Session, *, id: int, user: models.User) -> bool:
        if user.is_superuser:
            return True
        o = (
            self._get_base_query_user_can_read(db=db, user=user)
            .filter(self.model.id == id)
            .one_or_none()
        )
        if o:
            return True
        return False

    def user_can_write(self, db: Session, *, id: int, user: models.User) -> bool:
        if user.is_superuser:
            return True
        user_owns_parent_trip = (
            db.query(self.model)
            .filter(self.model.id == id)
            .join(
                models.BekpackTrip, self.model.parent_trip_id == models.BekpackTrip.id
            )
            .join(
                models.BekpackUser, models.BekpackTrip.owner_id == models.BekpackUser.id
            )
            .filter(models.BekpackUser.owner_id == user.id)
            .one_or_none()
        )
        if user_owns_parent_trip:
            return True

        user_parents_this_list = (
            db.query(self.model)
            .filter(self.model.id == id)
            .join(
                models.BekpackUser, self.model.parent_user_id == models.BekpackUser.id
            )
            .filter(models.BekpackUser.owner_id == user.id)
            .one_or_none()
        )
        if user_parents_this_list:
            return True
        return False


bekpackitemlist = CRUDBekpackItemList(BekpackItemList)
