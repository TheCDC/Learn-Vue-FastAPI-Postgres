from typing import List, Type
from app.db.base_class import Base

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, Query

from app.crud.base import CRUDBase, CRUDBaseSecure
from app.models.bekpack import BekpackTrip_Members, BekpackItemList, BekpackTrip
from app.schemas import BekpackItemListCreate, BekpackItemListUpdate
from app import crud, schemas, models


class CRUDBekpackItemList(
    CRUDBaseSecure[BekpackItemList, BekpackItemListCreate, BekpackItemListUpdate]
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

    def get_by_trip(
        self, db: Session, *, trip_id: int, user: models.User
    ) -> List[BekpackItemList]:
        return (
            self._get_base_query_user_can_read(
                db=db, user=user, models_to_include=[self.model]
            )
            .filter(BekpackItemList.parent_trip_id == trip_id)
            .all()
        )

    def get_by_owner(self, db: Session, *, owner_id: int) -> List[BekpackItemList]:
        return db.query(self.model).filter(self.model.parent_user_id == owner_id).all()


bekpackitemlist = CRUDBekpackItemList(BekpackItemList)
