from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy_utils.types import ColorType

from app.db.base_class import Base
from app.models.mixins import TimestampsMixin

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class BekpackTrip_Members(Base):
    id = Column(Integer, primary_key=True)
    trip_id = Column(
        Integer, ForeignKey("bekpacktrip.id", ondelete="CASCADE"), index=True
    )
    user_id = Column(
        Integer, ForeignKey("bekpackuser.id", ondelete="CASCADE"), index=True
    )
    trip = relationship("BekpackTrip")
    user = relationship("BekpackUser")


class BekpackUser(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), unique=True)
    is_active = Column(Boolean(), default=True)
    joined_trips = relationship(
        "BekpackTrip",
        secondary=BekpackTrip_Members.__table__,
        back_populates="members",
    )
    owned_bags = relationship("BekpackBag", back_populates="owner")
    owned_trips = relationship("BekpackTrip", back_populates="owner")
    owner = relationship("User")


class BekpackTrip(Base, TimestampsMixin):
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(
        Integer, ForeignKey(BekpackUser.id, ondelete="CASCADE"), index=True
    )
    color = Column(String)
    description = Column(String)
    is_active = Column(Boolean(), default=True)
    name = Column(String, index=True)
    bags = relationship("BekpackBag", back_populates="owner_trip")
    members = relationship(
        BekpackUser,
        secondary=BekpackTrip_Members.__table__,
        back_populates="joined_trips",
    )
    owner = relationship(BekpackUser, back_populates="owned_trips")
    item_lists = relationship("BekpackItemList", back_populates="parent_trip")


class BekpackItemList(Base):
    id = Column(Integer, primary_key=True, index=True)
    parent_trip_id = Column(
        Integer, ForeignKey(BekpackTrip.id, ondelete="cascade"), index=True
    )
    parent_user_id = Column(
        Integer, ForeignKey(BekpackUser.id, ondelete="cascade"), index=True
    )
    color = Column(String)
    name = Column(String)
    parent_trip = relationship(BekpackTrip, back_populates="item_lists")


class BekpackBag(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(
        Integer, ForeignKey(BekpackUser.id, ondelete="CASCADE"), index=True
    )
    owner_trip_id = Column(
        Integer, ForeignKey(BekpackTrip.id, ondelete="CASCADE"), index=True
    )
    color = Column(String)
    name = Column(String)
    items = relationship("BekpackItemListItem", backref="bag")
    owner = relationship(BekpackUser, back_populates="owned_bags")
    owner_trip = relationship(BekpackTrip, back_populates="bags")


class BekpackItemListItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    bag_id = Column(Integer, ForeignKey(BekpackBag.id))
    parent_list_id = Column(
        Integer,
        ForeignKey(BekpackItemList.id, ondelete="cascade"),
        index=True,
        nullable=False,
    )
    description = Column(String)
    list_index = Column(Integer)
    name = Column(String)
    quantity = Column(Integer)
