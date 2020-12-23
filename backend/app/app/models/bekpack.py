from typing import TYPE_CHECKING


from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy_utils.types import ColorType

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class BekPackTrip_Members(Base):
    trip_id = Column(
        Integer, ForeignKey("bekpacktrip.id"), primary_key=True, index=True
    )
    user_id = Column(
        Integer, ForeignKey("bekpackuser.id"), primary_key=True, index=True
    )


class BekpackUser(Base):
    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean(), default=True)
    joined_trips = relationship(
        "BekpackTrip",
        secondary=BekPackTrip_Members,
        back_populates="members",
    )
    owned_bags = relationship("BekpackBag", back_populates="owner")
    owned_trips = relationship("BekpackTrip", back_populates="owner")
    owner_id = Column(Integer, ForeignKey("user.id"))


class BekpackTrip(Base):
    id = Column(Integer, primary_key=True, index=True)
    bags = relationship("BekpackBag", back_populates="owner_trip")
    color = Column(ColorType)
    is_active = Column(Boolean(), default=True)
    members = relationship(
        BekpackUser,
        secondary=BekPackTrip_Members,
        back_populates=BekpackUser.joined_trips,
    )
    name = Column(String, index=True)
    owner = relationship(BekpackUser, back_populates=BekpackUser.owned_trips)
    owner_id = Column(Integer, ForeignKey(BekpackUser.id), index=True)
    items_lists = relationship("BekpackTripItemList", back_populates="parent_trip")


class BekpackTripItemList(Base):
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    parent_trip_id = Column(
        Integer, ForeignKey(BekpackTrip.id, ondelete="cascade"), index=True
    )
    parent_trip = relationship(BekpackTrip, back_populates=BekpackTrip.items_lists)
    parent_user_id = Column(
        Integer, ForeignKey(BekpackUser.id, ondelete="cascade"), primary_key=True
    )


class BekpackBag(Base):
    color = Column(ColorType)
    id = Column(Integer, primary_key=True, index=True)
    items = relationship("BekpackListItem", back_populates="owner")
    name = Column(String)
    owner = relationship(BekpackUser, back_populates=BekpackUser.owned_bags)
    owner_id = Column(Integer, ForeignKey(BekpackUser.id), index=True)
    owner_trip = relationship(BekpackTrip, back_populates=BekpackTrip.bags)
    owner_trip_id = Column(Integer, ForeignKey(BekpackTrip.id), index=True)


class BekpackListItem(Base):
    bag = relationship(BekpackBag, back_populates=BekpackBag.items)
    bag_id = Column(Integer, ForeignKey(BekpackBag.id))
    description = Column(String)
    id = Column(Integer, primary_key=True, index=True)
    list_index = Column(Integer)
    name = Column(String)
    parent_list_id = Column(
        Integer,
        ForeignKey(BekpackTripItemList.id, ondelete="cascade"),
        index=True,
        nullable=False,
    )
    quantity = Column(Integer)
