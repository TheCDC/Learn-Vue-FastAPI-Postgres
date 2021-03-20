from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import Session, Query
from app import models
from app.db.base_class import Base
from sqlalchemy.orm import aliased

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

    def _get_base_query_user_can_read(
        self, db: Session, *, models_to_include: Base = [], user: models.User
    ):
        raise NotImplementedError(
            f"_get_base_query_user_can_read not implemented on class {self.__class__.__name__}"
        )

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session,) -> List[ModelType]:
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

    def user_can_read(
        self, db: Session, *, object: ModelType, user: models.User
    ) -> bool:
        raise NotImplementedError(
            f"user_can_read not implemented on class {self.__class__.__name__}"
        )

    def user_can_write(
        self, db: Session, *, object: ModelType, user: models.User
    ) -> bool:
        raise NotImplementedError(
            f"user_can_write not implemented on class {self.__class__.__name__}"
        )

    def search(
        self, db: Session, *, filter_string: str, user: models.User
    ) -> List[ModelType]:
        base_query: Query = self._get_base_query_user_can_read(db=db, user=user)
        sbq = str(base_query)
        # get a list of columns on the model that are String type (searchable)
        string_columns: List[Column] = [
            c for c in self.model.__table__.columns if isinstance(c.type, String)
        ]

        # no string columns means no need for filtering
        if len(string_columns) == 0:
            return db.query(self.model).select_from(base_query.subquery()).all()

        query_expression = string_columns[0].ilike(f"%{filter_string}%")

        # if only one string column then no need to dynamically build a SQLAlchemy query
        if len(string_columns) == 1:
            return (
                db.query(self.model)
                .select_from(base_query.filter(query_expression).subquery())
                .all()
            )
        # Dynamically build a SQLALchemy query by OR-ing the string column comparisons together
        # i.e. search for filter_string in ANY of the String columns
        for c in string_columns[1:]:
            query_expression = query_expression | c.ilike(f"%{filter_string}%")
        subquery = (
            base_query.filter(query_expression)  # string filtering
            .with_labels()  # make sure the underlying SQL subquery disambiguates common column names across tables
            .subquery()  # Create queryable "table-like" object
        )
        model_alias = aliased(self.model, subquery)
        final_query = db.query(
            # select exactly one model type to return from the subquery
            model_alias
        ).select_from(subquery)
        return final_query.all()
