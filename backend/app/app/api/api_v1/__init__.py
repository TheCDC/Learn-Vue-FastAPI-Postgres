from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.param_functions import Security
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.paginator import paginate
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api import deps
from app.core.security import SecurityError
from app.crud.base import CRUDBase, CRUDBaseSecure
from app.db.base_class import Base
from app.models import User
from app import schemas

ModelType = TypeVar("ModelType", bound=Base)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
CRUDType = TypeVar("CRUDType", bound=CRUDBaseSecure)


class DefaultCrudRouter(
    Generic[ModelType, CRUDType, ReadSchemaType, UpdateSchemaType], APIRouter
):
    """
    Default router for a model

    Provides the following functions, one per route
    - get_one
    - get_multi_by_ids
    - get_all
    - update_one
    - delete_one
    - delete_multi_by_ids
    """

    def __init__(
        self,
        model: Type[ModelType],
        crud: CRUDBaseSecure,
        read_schema: Type[ReadSchemaType],
        update_schema: Type[UpdateSchemaType],
    ):
        """
        APIRouter object with default methods to Create, Read, Update, Delete.

        **Parameters**

        * `model`: A SQLAlchemy model class
        """
        super().__init__()
        self.model = model
        self.crud = crud
        self.read_schema = read_schema
        self.update_schema = update_schema

        @self.get(
            "/",
            response_model=Page[read_schema],
            dependencies=[Depends(pagination_params)],
        )
        def get_all(
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_superuser),
        ) -> AbstractPage[model]:
            objects = self.crud.get_multi(db=db, user=current_user)
            return paginate(objects)

        @self.get(
            "/{id}",
            response_model=self.read_schema,
        )
        def get_one(
            id: int,
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_user),
        ) -> Any:
            """Get one record"""
            try:
                object = self.crud.get(db=db, id=id, user=current_user)
                return object
            except SecurityError as e:

                raise HTTPException(status_code=404, detail=str(e))

        @self.get(
            "/select/by_string",
            response_model=Page[read_schema],
            dependencies=[Depends(pagination_params)],
        )
        def filter_by_string(
            filter_string: str = "",
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_user),
        ):
            """Filter by a string"""
            objects = self.crud.search(
                db=db, filter_string=filter_string, user=current_user
            )
            return paginate(objects)

        @self.get(
            "/select/by_ids",
            response_model=List[read_schema],
        )
        def get_multi_by_ids(
            ids: List[int] = Query([]),
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_user),
        ):
            """Get multiple records"""
            # TODO: optimize this to a single SQL query using _get_base_query_user_can_read

            objects = self.crud.get_multi_by_ids(db=db, ids=ids, user=current_user)
            if any(not o for o in objects) or len(objects) < len(ids):
                ids_not_found = list(set(ids) - set(i.id for i in objects))
                raise HTTPException(
                    status_code=404, detail=f"ids not found: {ids_not_found}"
                )

            return objects

        @self.put(
            "/{id}",
            response_model=self.read_schema,
        )
        def update_one(
            id: int,
            obj_in: update_schema,
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_user),
        ):
            """Update one record."""
            try:
                found = self.crud.get(db=db, id=id, user=current_user)
                return self.crud.update(
                    db=db, db_obj=found, obj_in=obj_in, user=current_user
                )
            except SecurityError as e:
                raise HTTPException(404, str(e))

        @self.delete("/{id}", response_model=self.read_schema)
        def delete_one(
            id: int,
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_user),
        ) -> Any:
            """Delete one record."""
            try:
                return self.crud.remove(db=db, id=id, user=current_user)
            except SecurityError as e:
                raise HTTPException(404, str(e))

        @self.delete("/", response_model=int)
        def delete_multi_by_ids(
            ids: List[int] = list(),
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_user),
        ) -> Any:
            """Delete multiple records."""
            # TODO: optimize this to a single SQL query using _get_base_query_user_can_write
            # TODO: implement _get_base_query_user_can_write
            objects = self.crud.get_multi_by_ids(db=db, ids=ids, user=current_user)
            if len(objects) < len(ids):
                raise HTTPException(status_code=404)
            ret = self.crud.remove_multi(db=db, ids=ids, user=current_user)
            return ret
