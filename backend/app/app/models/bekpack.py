from typing import TYPE_CHECKING


from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy_utils.types import ColorType

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class BekPackTrip_Members(Base):
    user_id = Column(
        Integer, ForeignKey("bekpackuser.id"), primary_key=True, index=True
    )
    trip_id = Column(
        Integer, ForeignKey("bekpacktrip.id"), primary_key=True, index=True
    )


class BekpackUser(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    is_active = Column(Boolean(), default=True)
    joined_trips = relationship(
        "BekpackTrip",
        secondary=BekPackTrip_Members,
        back_populates="members",
    )
    owned_trips = relationship("BekpackTrip", back_populates="owner")
    owned_bags = relationship("BekpackBag", back_populates="owner")


class BekpackTrip(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_active = Column(Boolean(), default=True)
    owner_id = Column(Integer, ForeignKey(BekpackUser.id))
    color = Column(ColorType)
    owner = relationship(BekpackUser, back_populates=BekpackUser.owned_trips)
    members = relationship(
        BekpackUser,
        secondary=BekPackTrip_Members,
        back_populates=BekpackUser.joined_trips,
    )
    bags = relationship("BekpackBag", back_populates="owner_list")


class BekpackTripItemList(Base):
    id = Column(Integer, primary_key=True, index=True)
    parent_trip = Column(Integer, ForeignKey(BekpackTrip.id), primary_key=True)
    parent_user = Column(Integer, ForeignKey(BekpackUser.id), primary_key=True)
    name = Column(String)


class BekpackBag(Base):
    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(Integer, ForeignKey(BekpackUser.id), index=True)
    owner = relationship(BekpackUser, back_populates=BekpackUser.owned_bags)
    owner_trip_id = Column(Integer, ForeignKey(BekpackTrip.id), index=True)
    owner_trip = relationship(BekpackTrip, back_populates=BekpackTrip.bags)

    color = Column(ColorType)
    name = Column(String)
    items = relationship("BekpackListItem", back_populates="owner")


class BekpackListItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    bag_id = Column(Integer, ForeignKey(BekpackBag.id))
    bag = relationship(BekpackBag, back_populates=BekpackBag.items)
    parent_list = Column(Integer, ForeignKey(BekpackTripItemList.id))
    list_index = Column(Integer)
    quantity = Column(Integer)
    name = Column(String)
    description = Column(String)
