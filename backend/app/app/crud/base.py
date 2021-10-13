from functools import reduce
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import Session, Query
from app import models
from app.core.security import SecurityError
from app.db.base_class import Base
from sqlalchemy.orm import aliased

from app.models.user import User

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
    ) -> List[ModelType]:
        return db.query(self.model).all()

    def get_multi_by_ids(self, db: Session, *, ids: List[int]) -> List[ModelType]:
        return db.query(self.model).filter(self.model.id.in_(tuple(ids))).all()

    def get_multi_paginate(
        self, db: Session, *, limit: int = 100, skip: int = 0
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def remove_multi(self, db: Session, *, ids: List[int]) -> List[ModelType]:
        records = (
            db.query(self.model)
            .filter(self.model.id.in_(tuple(ids)))
            .delete(synchronize_session=False)  # Don't update deleted objects
        )
        db.commit()
        return records


class CRUDBaseSecure(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def _get_base_query_user_can_read(
        self,
        db: Session,
        *,
        models_to_include: List[Type[Base]] = [],
        user: models.User,
    ) -> Query:
        raise NotImplementedError(
            f"_get_base_query_user_can_read not implemented on class {self.__class__.__name__}"
        )

    def _get_query_objects_user_can_read(
        self, db: Session, *, user: models.User
    ) -> Query:
        subquery_visible_objects = (
            self._get_base_query_user_can_read(db=db, user=user)
            # make sure the underlying SQL subquery disambiguates common column names across tables
            .with_labels()
            # Create queryable "table-like" object
            .subquery()
        )

        return db.query(self.model).select_from(subquery_visible_objects)

    def _get_base_query_user_can_write(
        self,
        db: Session,
        *,
        models_to_include: List[Type[Base]] = [],
        user: models.User,
    ) -> Query:
        if user.is_superuser:
            return db.query(self.model)
        return self._get_base_query_user_can_read(
            db=db, models_to_include=models_to_include, user=user
        )

    def search(
        self, db: Session, *, filter_string: str, user: models.User
    ) -> List[ModelType]:
        """Permissions-safe filter records by string"""

        base_query: Query = self._get_base_query_user_can_read(db=db, user=user)
        # list of columns on the model that are searchable (String type)
        string_columns: List[Column] = [
            c for c in self.model.__table__.columns if isinstance(c.type, String)
        ]
        visible_objects = self._get_query_objects_user_can_read(db=db, user=user)

        # dynamically build SQLAlchemy query that checks all string fields on the model
        query_expression = reduce(
            lambda acc, next: acc | next,
            [c.ilike(f"%{filter_string}%") for c in string_columns],
        )
        return visible_objects.filter(query_expression).all()

    def get(self, db: Session, id: int, user: User) -> ModelType:
        q = self._get_query_objects_user_can_read(db=db, user=user).filter(
            self.model.id == id
        )
        obj = q.one_or_none()
        if not obj:
            raise SecurityError("User cannot get object")
        return obj

    def get_multi(self, db: Session, user: User) -> List[ModelType]:
        """Permissions-safe get all records"""

        return self._get_query_objects_user_can_read(db=db, user=user).all()

    def get_multi_by_ids(
        self, db: Session, *, ids: List[int], user: User
    ) -> List[ModelType]:
        """Permissions-safe get multiple records by ids"""

        return (
            self._get_query_objects_user_can_read(db=db, user=user)
            .filter(self.model.id.in_(tuple(ids)))
            .all()
        )

    def get_multi_paginate(
        self, db: Session, *, limit: int = 100, skip: int = 0, user: User
    ) -> List[ModelType]:
        """Permissions-safe get multiple records paginated"""

        return (
            self._get_query_objects_user_can_read(db=db, user=user)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        user: User,
    ) -> ModelType:
        """Permissions-safe update record"""
        query = self._get_base_query_user_can_write(db=db, user=user).filter(
            self.model.id == db_obj.id
        )
        can_read = query.one_or_none()
        if not can_read:
            raise SecurityError("User cannot update this resource.")

        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)

    def remove(self, db: Session, *, id: int, user: User) -> ModelType:
        """Permissions-safe delete record"""

        obj = (
            self._get_base_query_user_can_write(db=db, user=user)
            .filter(self.model.id == id)
            .one_or_none()
        )
        if not obj:
            raise SecurityError("User cannot delete this resource")
        return super().remove(db=db, id=id)

    def remove_multi(
        self, db: Session, *, ids: List[int], user: User
    ) -> List[ModelType]:
        """Permissions-safe delete multiple records"""

        records = (
            self._get_base_query_user_can_write(db=db, user=user)
            .filter(self.model.id.in_(tuple(ids)))
            .delete(synchronize_session=False)  # Don't update deleted objects
        )
        db.commit()
        return records
