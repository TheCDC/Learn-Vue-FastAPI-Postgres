from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.bekpack import BekpackTrip, BekpackUser
from app.schemas import BekpackTripCreate, BekpackTripUpdate


class CRUDBekpackTrip(CRUDBase[BekpackTrip, BekpackTripCreate, BekpackTripUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: BekpackTripCreate, owner_id: int
    ) -> BekpackTrip:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        user = db.query(BekpackUser).filter(BekpackUser.id == owner_id).one()
        db_obj.members.append(user)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_owner(self, db: Session, *, owner_id: int) -> List[BekpackTrip]:
        return db.query(self.model).filter(BekpackTrip.owner_id == owner_id).all()


bekpacktrip = CRUDBekpackTrip(BekpackTrip)
