from typing import Set, Optional
from pydantic import BaseModel

# Shared properties
class BekpackItemListItemBase(BaseModel):
    id: Optional[int]

    description: Optional[str]
    list_index: Optional[int]
    name: Optional[str]
    quantity: Optional[int]


# Properties to receive via API on creation
class BekpackItemListItemCreate(BekpackItemListItemBase):
    description: str
    name: str
    quantity: int


# Properties to receive via API on update
class BekpackItemListItemUpdate(BekpackItemListItemBase):
    pass


# Properties shared by models stored in DB
class BekpackItemListItemInDBBase(BekpackItemListItemBase):
    id: int
    parent_list_id: int
    bag_id: int
    list_index: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class BekpackItemListItem(BekpackItemListItemInDBBase):
    pass


# Additional properties stored in DB
class BekpackItemListItemInDB(BekpackItemListItemInDBBase):
    pass
