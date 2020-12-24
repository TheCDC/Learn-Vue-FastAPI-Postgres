from .crud_item import item
from .crud_user import user
from .crud_bekpack import bekpackuser
from .crud_bekpack import bekpacktrip
from .crud_bekpack import bekpacktripitemlist

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
