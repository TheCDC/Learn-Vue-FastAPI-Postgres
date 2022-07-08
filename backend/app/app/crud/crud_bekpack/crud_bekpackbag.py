from typing import List, Type
from app.models.bekpack import BekpackBag

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

from app import crud, models, schemas
from app.core.security import SecurityError
from app.crud.base import CRUDBaseSecure
from app.db.base_class import Base


class CRUDBekpackBag(
    CRUDBaseSecure[
        models.BekpackBag,
        schemas.BekpackBagCreate,
        schemas.BekpackBagUpdate,
    ]
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

    def get_multi_by_trip(
        self, db: Session, *, owner_trip_id: int, user: models.User
    ) -> List[BekpackBag]:
        return (
            self._get_base_query_user_can_read(db=db, user=user)
            .filter(self.model.owner_trip_id == owner_trip_id)
            .all()
        )

    def create_with_trip(
        self,
        db: Session,
        *,
        obj_in=schemas.BekpackBagCreate,
        owner_trip_id: int,
        owner_id: int,
        user: models.User
    ) -> BekpackBag:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


bekpackbag = CRUDBekpackBag(models.BekpackBag)
