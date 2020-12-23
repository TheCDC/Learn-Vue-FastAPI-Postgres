from typing import Set, Optional
from pydantic import BaseModel

# Shared properties
class BekpackListItemBase(BaseModel):
    bag_id: Optional[int]
    description: Optional[str]
    list_index: Optional[int]
    name: Optional[str]
    parent_list_id: Optional[int]
    quantity: Optional[int]


# Properties to receive via API on creation
class BekpackListItemCreate(BekpackListItemBase):
    description: str
    name: str
    parent_list_id: int
    quantity: str


# Properties to receive via API on update
class BekpackListItemUpdate(BekpackListItemBase):
    pass


# Properties shared by models stored in DB
class BekpackListItemInDBBase(BekpackListItemBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class BekpackListItem(BekpackListItemInDBBase):
    pass


# Additional properties stored in DB
class BekpackListItemInDB(BekpackListItemInDBBase):
    pass
