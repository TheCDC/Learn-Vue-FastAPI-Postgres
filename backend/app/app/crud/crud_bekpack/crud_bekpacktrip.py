from typing import List, Type

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql.elements import and_, or_

from app import crud, models
from app.core.security import SecurityError
from app.crud.base import CRUDBaseSecure
from app.db.base_class import Base
from app.models.bekpack import BekpackTrip, BekpackTrip_Members, BekpackUser
from app.models.user import User
from app.schemas import BekpackTripCreate, BekpackTripUpdate


class CRUDBekpackTrip(
    CRUDBaseSecure[BekpackTrip, BekpackTripCreate, BekpackTripUpdate]
):
    def _get_base_query_user_can_read(
        self,
        db: Session,
        *,
        models_to_include: List[Type[Base]] = [],
        user: models.User,
    ):

        mti: List[Type[Base]] = [self.model]
        mti.extend(models_to_include)
        if user.is_superuser:
            return db.query(self.model)

        included = Query(
            entities=mti,
            session=db,
        )
        return (
            included.join(
                BekpackTrip_Members,
            )
            .join(
                BekpackUser,
            )
            .filter(
                or_(
                    and_(
                        BekpackTrip_Members.trip_id == self.model.id,
                        BekpackTrip_Members.user_id == models.BekpackUser.id,
                        BekpackUser.owner_id == user.id,
                    ),  # you are a member)
                    BekpackTrip.owner_id == user.id,  # you are the owner
                ),
            )
        )

    def _get_base_query_user_can_write(
        self,
        db: Session,
        *,
        models_to_include: List[Type[Base]] = [],
        user: models.User,
    ) -> Query:
        return self._get_base_query_user_can_read(
            db=db, models_to_include=models_to_include, user=user
        )

    def create_with_owner(
        self, db: Session, *, obj_in: BekpackTripCreate, owner: models.User
    ) -> BekpackTrip:
        # bp_user: BekpackUser = (
        #     db.query(self.model).filter(self.model.owner_id == owner.id).one_or_none()
        # )
        bp_user: BekpackUser = crud.bekpackuser.get_by_owner(db=db, owner_id=owner.id)

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=bp_user.id)
        # trip owner is also a member by default
        db_obj.members.append(bp_user)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_owner(
        self,
        db: Session,
        *,
        owner_id: int,
    ) -> List[BekpackTrip]:
        return (
            db.query(self.model)
            .join(BekpackUser, BekpackUser.owner_id == owner_id)
            .filter(BekpackTrip.owner_id == BekpackUser.id)
            .order_by(BekpackTrip.time_updated.desc())
            .all()
        )

    def get_all(
        self,
        db: Session,
    ) -> List[BekpackTrip]:
        return db.query(self.model).order_by(BekpackTrip.time_updated.desc()).all()

    def get_joined_by_member(self, db: Session, *, member_id: int) -> List[BekpackTrip]:
        associations: List[BekpackTrip] = (
            db.query(self.model)
            .join(BekpackTrip_Members)
            .filter(BekpackTrip_Members.user_id == member_id)
            .filter(self.model.id == BekpackTrip_Members.trip_id)
        )
        return associations

    def add_member(
        self,
        db: Session,
        *,
        trip_obj: BekpackTrip,
        bp_user_obj: BekpackUser,
        user: User,
    ) -> BekpackTrip:
        can = (
            self._get_base_query_user_can_write(db=db, user=user)
            .filter(BekpackTrip.id == trip_obj.id)
            .one_or_none()
            != None
        )
        if not can:
            raise SecurityError("User cannot edit this Trip")
        trip_obj.members.append(bp_user_obj)
        db.add(trip_obj)
        db.commit()
        db.refresh(trip_obj)
        return trip_obj


bekpacktrip = CRUDBekpackTrip(BekpackTrip)
