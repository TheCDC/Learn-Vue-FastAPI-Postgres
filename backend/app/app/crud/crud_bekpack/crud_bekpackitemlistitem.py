from typing import List, Type

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

from app import crud, models, schemas
from app.core.security import SecurityError
from app.crud.base import CRUDBase
from app.db.base_class import Base


class CRUDBekpackItemListItem(
    CRUDBase[
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

    def user_can_read(self, db: Session, *, id: int, user: models.User) -> bool:
        if user.is_superuser:
            return True
        o = (
            self._get_base_query_user_can_read(db=db, user=user)
            .filter(self.model.id == id)
            .one_or_none()
        )
        if o:
            return True
        return False

    def user_can_write(self, db: Session, *, id: int, user: models.User) -> bool:
        if user.is_superuser:
            return True
        o = self.get(db=db, id=id)
        if not o:
            return False

        return crud.bekpackitemlist.user_can_write(
            db=db, id=o.parent_list_id, user=user
        )

    def get_multi_by_itemlist(
        self, db: Session, *, parent_itemlist_id: int, user: models.User
    ) -> List[models.BekpackItemListItem]:
        return (
            self._get_base_query_user_can_read(db=db, user=user)
            .filter(self.model.parent_list_id == parent_itemlist_id)
            .all()
        )

    def get_multi_by_bag(
        self, db: Session, *, bag_id: int, user: models.User
    ) -> List[models.BekpackItemListItem]:
        return (
            self._get_base_query_user_can_read(db=db, user=user)
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
        if crud.bekpackitemlist.user_can_write(db=db, id=parent_itemlist_id, user=user):
            obj_in_data = jsonable_encoder(obj_in)

            return self.model(
                **obj_in_data, parent_list_id=parent_itemlist_id, bag_id=bag_id
            )
        else:
            raise SecurityError("User cannot edit this list")


bekpackitemlistitem = CRUDBekpackItemListItem(models.BekpackItemListItem)
