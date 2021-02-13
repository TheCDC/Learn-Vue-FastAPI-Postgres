from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.bekpack import BekPackTrip_Members, BekpackItemList, BekpackTrip
from app.schemas import BekpackItemListCreate, BekpackItemListUpdate


class CRUDBekpackItemList(
    CRUDBase[BekpackItemList, BekpackItemListCreate, BekpackItemListUpdate]
):
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

    def is_owned_by_bekpackuser(
        self, db: Session, *, list_id: int, member_id: int
    ) -> bool:
        return self.get(db=db, id=id).parent_trip.owner.id == member_id

    def user_can_see(self, db: Session, *, list_id: int, bekpack_user_id: int) -> bool:
        itemlist: BekpackItemList = db.query(self.model).filter(id=list_id).one()
        potential_membership = (
            db.query(self.model)
            .join(BekpackTrip, BekpackTrip.id == itemlist.trip_id)
            .join(BekPackTrip_Members, BekPackTrip_Members.user_id == bekpack_user_id)
            .one_or_none()
        )
        if potential_membership:
            return True
        return False

    def user_can_edit(self, db: Session, *, list_id: int, bekpack_user_id: int) -> bool:
        itemlist: BekpackItemList = db.query(self.model).filter(id=list_id).one()
        return itemlist.parent_user_id == bekpack_user_id


bekpackitemlist = CRUDBekpackItemList(BekpackItemList)
