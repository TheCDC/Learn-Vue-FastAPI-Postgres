from typing import List
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
        self, db: Session, *, models_to_include: List[Base] = [], user: models.User
    ):
        if user.is_superuser:
            return db.query(self.model)
        return crud.bekpacktrip._get_base_query_user_can_read(
            db=db, models_to_include=[self.model] + models_to_include, user=user
        ).join(self.model)

    def create_with_trip_owner(
        self, db: Session, *, obj_in: BekpackItemListCreate, owner_id: int, trip_id: int
    ) -> BekpackItemList:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data, parent_user_id=owner_id, parent_trip_id=trip_id
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

    def user_can_see(self, db: Session, *, list_id: int, bekpack_user_id: int) -> bool:
        itemlist: BekpackItemList = db.query(self.model).filter(id=list_id).one()
        potential_membership = (
            db.query(self.model)
            .join(BekpackTrip, BekpackTrip.id == itemlist.trip_id)
            .join(BekpackTrip_Members, BekpackTrip_Members.user_id == bekpack_user_id)
            .one_or_none()
        )
        if potential_membership:
            return True
        return False

    def user_can_write(
        self, db: Session, *, list_id: int, bekpack_user_id: int
    ) -> bool:
        itemlist: BekpackItemList = db.query(self.model).filter(id=list_id).one()
        return itemlist.parent_user_id == bekpack_user_id


bekpackitemlist = CRUDBekpackItemList(BekpackItemList)
