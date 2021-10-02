from typing import List, Type

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

from app import crud, models, schemas
from app.core.security import SecurityError
from app.crud.base import CRUDBaseSecure
from app.db.base_class import Base


class CRUDBekpackItemListItem(
    CRUDBaseSecure[
        models.BekpackItemListItem,
        schemas.BekpackItemListItemCreate,
        schemas.BekpackItemListItemUpdate,
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
        return crud.bekpackitemlist._get_base_query_user_can_read(
            db=db, models_to_include=mti, user=user
        ).join(self.model)

    def get_multi_by_itemlist(
        self, db: Session, *, parent_itemlist_id: int, user: models.User
    ) -> List[models.BekpackItemListItem]:
        return (
            self._get_query_objects_user_can_read(db=db, user=user)
            .filter(self.model.parent_list_id == parent_itemlist_id)
            .all()
        )

    def get_multi_by_bag(
        self, db: Session, *, bag_id: int, user: models.User
    ) -> List[models.BekpackItemListItem]:
        return (
            self._get_query_objects_user_can_read(db=db, user=user)
            .filter(self.model.bag_id == bag_id)
            .all()
        )

    def create_with_itemlist(
        self,
        db: Session,
        *,
        obj_in: schemas.BekpackItemListItemCreate,
        parent_itemlist_id: int,
        bag_id=None,
        user: models.User
    ) -> models.BekpackItemListItem:
        parent = crud.bekpackitemlist.get(db=db, id=parent_itemlist_id, user=user)
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, parent_list_id=parent.id, bag_id=bag_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


bekpackitemlistitem = CRUDBekpackItemListItem(models.BekpackItemListItem)
