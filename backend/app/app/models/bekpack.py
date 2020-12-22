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
    bags = relationship("BekpackBag", back_populates="owner_list")
    color = Column(ColorType)
    is_active = Column(Boolean(), default=True)
    members = relationship(
        BekpackUser,
        secondary=BekPackTrip_Members,
        back_populates=BekpackUser.joined_trips,
    )
    name = Column(String, index=True)
    owner = relationship(BekpackUser, back_populates=BekpackUser.owned_trips)
    owner_id = Column(Integer, ForeignKey(BekpackUser.id))


class BekpackTripItemList(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    parent_trip_id = Column(Integer, ForeignKey(BekpackTrip.id), primary_key=True)
    parent_user_id = Column(Integer, ForeignKey(BekpackUser.id), primary_key=True)


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
        Integer, ForeignKey(BekpackTripItemList.id), primary_key=True, index=True
    )
    quantity = Column(Integer)
