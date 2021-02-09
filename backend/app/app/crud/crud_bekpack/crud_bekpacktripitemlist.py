from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.bekpack import BekpackTripItemList
from app.schemas import BekpackTripItemListCreate, BekpackTripItemListUpdate


class CRUDBekpackTripItemList(
    CRUDBase[BekpackTripItemList, BekpackTripItemListCreate, BekpackTripItemListUpdate]
):
    def create_with_trip(
        self, db: Session, *, obj_in: BekpackTripItemListCreate, owner_id: int
    ) -> BekpackTripItemList:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_trip(self, db: Session, *, trip_id: int) -> List[BekpackTripItemList]:
        return (
            db.query(self.model)
            .filter(BekpackTripItemList.parent_trip_id == trip_id)
            .all()
        )

    def is_owned_by_bekpackuser(
        self, db: Session, *, list_id: int, member_id: int
    ) -> bool:
        self.get(db=db, id=id).parent_trip.owner.id == member_id


bekpacktripitemlist = CRUDBekpackTripItemList(BekpackTripItemList)
