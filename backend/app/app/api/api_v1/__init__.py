from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.page import Page
from fastapi_pagination.paginator import paginate
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models import User

ModelType = TypeVar("ModelType", bound=Base)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
CRUDType = TypeVar("CRUDType", bound=CRUDBase)


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
        *,
        model: Type[ModelType],
        crud: CRUDType,
        read_schema: ReadSchemaType,
        update_schema: UpdateSchemaType,
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
            object = self.crud.get(db=db, id=id)
            if not object:
                raise HTTPException(status_code=404)

            if self.crud.user_can_read(db=db, object=object, user=current_user):
                return object
            raise HTTPException(status_code=403, detail="Not authorized")

        @self.get(
            "/select/by_string",
            response_model=Page[self.read_type],
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
            # print(objects)
            return paginate(objects)

        @self.get(
            "/select/by_ids", response_model=List[self.read_type],
        )
        def get_multi_by_ids(
            ids: List[int] = Query([]),
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_user),
        ):
            """Get multiple records"""
            # TODO: optimize this to a single SQL query using _get_base_query_user_can_read

            objects = self.crud.get_multi_by_ids(db=db, ids=ids)
            if any(not o for o in objects) or len(objects) < len(ids):
                ids_not_found = list(set(ids) - set(i.id for i in objects))
                raise HTTPException(
                    status_code=404, detail=f"ids not found: {ids_not_found}"
                )
            if not all(
                self.crud.user_can_read(db=db, user=current_user, object=object)
                for object in objects
            ):
                raise HTTPException(status_code=403, detail="Not authorized")

            return objects

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
            object = self.crud.get(db=db, id=id)
            if not object:
                raise HTTPException(status_code=404)
            if not self.crud.user_can_write(db=db, object=object, user=current_user):
                raise HTTPException(status_code=403, detail="Not authorized")
            return self.crud.update(db=db, db_obj=object, obj_in=obj_in)

        @self.delete("/{id}", response_model=self.read_type)
        def delete_one(
            id: int,
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_user),
        ) -> Any:
            """Delete one record."""
            object = self.crud.get(db=db, id=id)
            if not object:
                raise HTTPException(status_code=404)
            if not self.crud.user_can_write(db=db, user=current_user, object=object):
                raise HTTPException(status_code=403, detail="Not authorized")
            return self.crud.remove(db=db, id=id)

        @self.delete("/", response_model=int)
        def delete_multi_by_ids(
            ids: List[int] = list(),
            db: Session = Depends(deps.get_db),
            current_user: User = Depends(deps.get_current_active_user),
        ) -> Any:
            """Delete multiple records.

            """
            # TODO: optimize this to a single SQL query using _get_base_query_user_can_write
            # TODO: implement _get_base_query_user_can_write
            objects = self.crud.get_multi_by_ids(db=db, ids=ids)
            if len(objects) < len(ids):
                raise HTTPException(status_code=404)
            if any(
                not self.crud.user_can_write(db=db, user=current_user, object=object)
                for object in objects
            ):
                raise HTTPException(status_code=403, detail="Not authorized")
            ret = self.crud.remove_multi(db=db, ids=ids)
            return ret
