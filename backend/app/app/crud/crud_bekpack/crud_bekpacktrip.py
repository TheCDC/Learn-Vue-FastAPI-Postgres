from typing import List
from app.db.base_class import Base

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, Query

from app import models
from app.crud.base import CRUDBase
from app.models.bekpack import BekpackTrip, BekpackTrip_Members, BekpackUser
from app.schemas import BekpackTripCreate, BekpackTripUpdate


class CRUDBekpackTrip(CRUDBase[BekpackTrip, BekpackTripCreate, BekpackTripUpdate]):
    def _get_base_query_user_can_read(
        self, db: Session, *, models_to_include: List[Base] = [], user: models.User
    ):

        if user.is_superuser:
            return db.query(self.model)

        included = Query(entities=[models.BekpackTrip] + models_to_include, session=db,)
        return (
            included.join(BekpackTrip_Members)
            .join(models.BekpackUser)
            .filter(BekpackUser.owner_id == user.id)
        )

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
            .join(BekpackUser, BekpackUser.owner_id == owner_id)
            .filter(BekpackTrip.owner_id == BekpackUser.id)
            .order_by(BekpackTrip.time_updated.desc())
            .all()
        )

    def get_all(self, db: Session,) -> List[BekpackTrip]:
        return db.query(self.model).order_by(BekpackTrip.time_updated.desc()).all()

    def get_joined_by_member(self, db: Session, *, member_id: int) -> List[BekpackTrip]:
        associations: List[BekpackTrip_Members] = (
            db.query(self.model)
            .join(BekpackTrip_Members)
            .filter(BekpackTrip_Members.user_id == member_id)
            .filter(self.model.id == BekpackTrip_Members.trip_id)
        )
        return associations

    def user_can_read(
        self, db: Session, object: BekpackTrip, user: models.User
    ) -> bool:
        if user.is_superuser:
            return True
        obj = (
            db.query(self.model)
            .join(models.BekpackUser, BekpackUser.owner_id == user.id)
            .join(BekpackTrip_Members, BekpackTrip.id == object.id)
            .filter(
                (BekpackTrip_Members.trip_id == object.id)
                & (BekpackTrip_Members.user_id == models.BekpackUser.id)
            )
            .one_or_none()
        )
        if not obj:
            return False
        return True

    def user_can_write(
        self, db: Session, object: BekpackTrip, user: models.User
    ) -> bool:
        if user.is_superuser:
            return True
        obj = (
            db.query(self.model)
            .join(models.BekpackUser, BekpackUser.owner_id == user.id)
            .join(BekpackTrip_Members, BekpackTrip.id == object.id)
            .filter(
                (BekpackTrip_Members.trip_id == object.id)
                & (BekpackTrip_Members.user_id == models.BekpackUser.id)
            )
            .one_or_none()
        )
        if not obj:
            return False
        return True


bekpacktrip = CRUDBekpackTrip(BekpackTrip)
