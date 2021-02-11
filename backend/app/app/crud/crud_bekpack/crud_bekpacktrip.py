from typing import List
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.bekpack import BekpackTrip, BekpackUser
from app.models.bekpack import BekpackTrip, BekpackUser, BekPackTrip_Members
from app.schemas import BekpackTripCreate, BekpackTripUpdate


class CRUDBekpackTrip(CRUDBase[BekpackTrip, BekpackTripCreate, BekpackTripUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: BekpackTripCreate, owner_id: int
    ) -> BekpackTrip:
        obj_in_data = jsonable_encoder(obj_in)
        owner: BekpackUser = (
            db.query(BekpackUser).filter(BekpackUser.id == owner_id).one()
        )

        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        # trip owner is also a member by default
        db_obj.members.append(owner)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_owner(self, db: Session, *, owner_id: int,) -> List[BekpackTrip]:
        return (
            db.query(self.model)
            .filter(BekpackTrip.owner_id == owner_id)
            .order_by(BekpackTrip.time_updated.desc())
            .all()
        )

    def get_all(self, db: Session,) -> List[BekpackTrip]:
        return db.query(self.model).order_by(BekpackTrip.time_updated.desc()).all()

    def get_joined_by_member(self, db: Session, *, member_id: int) -> List[BekpackTrip]:
        associations: List[BekPackTrip_Members] = (
            db.query(self.model)
            .join(BekPackTrip_Members)
            .filter(BekPackTrip_Members.user_id == member_id)
            .filter(self.model.id == BekPackTrip_Members.trip_id)
        )
        return associations

    def is_owned_by_bekpackuser(self, db: Session, *, id: int, member_id: int,) -> bool:
        t = self.get(db=db, id=id)
        return t.owner_id == member_id


bekpacktrip = CRUDBekpackTrip(BekpackTrip)
