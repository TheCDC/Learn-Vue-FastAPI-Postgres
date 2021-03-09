from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.page import Page
from fastapi_pagination.paginator import paginate
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

from app.api import deps
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models import User

ModelType = TypeVar("ModelType", bound=Base)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
CRUDType = TypeVar("CRUDType", bound=CRUDBase)


class DefaultCrudRouter(
    Generic[ModelType, CRUDType, ReadSchemaType, UpdateSchemaType,], APIRouter
):
    """
    Default router for a model
    Provides the following functions, one per route
    - get_all
	- get_one
	- update_one
	- delete_one
	- delete_many
    """

    def __init__(
        self,
        *,
        model: Type[ModelType],
        crud: CRUDType,
        read_schema: ReadSchemaType,
        update_schema: UpdateSchemaType
    ):
        """
        APIRouter object with default methods to Create, Read, Update, Delete.
        **Parameters**
        * `model`: A SQLAlchemy model class
        """
        super().__init__()
        self.model = model
        self.crud = crud
        self.read_type = read_schema
        self.update_type = update_schema
        # def initialize(self):
        @self.get(
            "/",
            response_model=Page[self.read_type],
            dependencies=[Depends(pagination_params)],
        )
        def get_all(
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_superuser),
        ):
            return paginate(self.crud.get_multi(db=db))

        @self.get(
            "/{id}",
            response_model=self.read_type,
            dependencies=[Depends(pagination_params)],
        )
        def get_one(
            id: int,
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_user),
        ):
            """Get one record"""
            obj = self.crud.get(db=db, id=id)
            if not obj:
                raise HTTPException(status_code=404)

            if self.crud.user_can_read(db=db, id=id, user=current_user):
                return obj
            raise HTTPException(status_code=403, detail="Not authorized")

        @self.put(
            "/{id}", response_model=self.read_type,
        )
        def update_one(
            id: int,
            obj_in: self.update_type,
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_user),
        ):
            """Update one record."""
            obj = self.crud.get(db=db, id=id)
            if not obj:
                raise HTTPException(status_code=404)
            if not self.crud.user_can_write(db=db, id=id, user=current_user):
                raise HTTPException(status_code=403, detail="Not authorized")
            print(repr(obj), obj_in)
            return self.crud.update(db=db, db_obj=obj, obj_in=obj_in)

        @self.delete("/{id}", response_model=self.read_type)
        def delete_one(
            id: int,
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_user),
        ) -> Any:
            """Delete one record."""
            obj = self.crud.get(db=db, id=id)
            if not obj:
                raise HTTPException(status_code=404)
            if not self.crud.user_can_write(db=db, user=current_user, id=id):
                raise HTTPException(status_code=403, detail="Not authorized")
            return self.crud.remove(db=db, id=id)

        @self.delete("/", response_model=List[self.read_type])
        def delete_many(
            ids: List[int],
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_user),
        ) -> Any:
            """Delete multiple records.
            """
            objs = self.crud.get_multi(db=db, ids=ids)
            if any(not o for o in objs):
                raise HTTPException(status_code=404)
            # TODO: optimize this to a single SQL query
            if any(
                not self.crud.user_can_write(db=db, user=current_user, id=id)
                for id in ids
            ):
                raise HTTPException(status_code=403, detail="Not authorized")
            return self.crud.remove(db=db, id=id)
