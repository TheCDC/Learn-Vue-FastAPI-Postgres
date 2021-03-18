from app import crud, models, schemas
from app.crud.base import CRUDBase


class CRUDBekpackItemListItem(
    CRUDBase[
        models.BekpackItemListItem,
        schemas.BekpackItemListItemCreate,
        schemas.BekpackItemListItemUpdate,
    ]
):
    pass
