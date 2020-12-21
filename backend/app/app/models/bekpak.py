from typing import TYPE_CHECKING


from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy_utils.types import ColorType

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Associate_BekpakUser_BekPakTrip(Base):
    user_id = Column(Integer, ForeignKey("bekpakuser.id"), primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("bekpaktrip.id"), primary_key=True, index=True)


class BekpakUser(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    is_active = Column(Boolean(), default=True)
    joined_trips = relationship(
        "BekpakTrip",
        secondary=Associate_BekpakUser_BekPakTrip,
        back_populates="members",
    )
    owned_trips = relationship("BekpakTrip", back_populates="owner")
    owned_bags = relationship("BekpakBag", back_populates="owner")


class BekpakTrip(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_active = Column(Boolean(), default=True)
    owner_id = Column(Integer, ForeignKey(BekpakUser.id))
    color = Column(ColorType)
    owner = relationship(BekpakUser, back_populates=BekpakUser.owned_trips)
    members = relationship(
        BekpakUser,
        secondary=Associate_BekpakUser_BekPakTrip,
        back_populates=BekpakUser.joined_trips,
    )
    bags = relationship("BekpakBag", back_populates="owner_list")


class BekpakTripItemList(Base):
    id = Column(Integer, primary_key=True, index=True)
    parent_trip = Column(Integer, ForeignKey(BekpakTrip.id), primary_key=True)
    parent_user = Column(Integer, ForeignKey(BekpakUser.id), primary_key=True)
    name = Column(String)


class BekpakBag(Base):
    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(Integer, ForeignKey(BekpakUser.id), index=True)
    owner = relationship(BekpakUser, back_populates=BekpakUser.owned_bags)
    owner_trip_id = Column(Integer, ForeignKey(BekpakTrip.id), index=True)
    owner_trip = relationship(BekpakTrip, back_populates=BekpakTrip.bags)

    color = Column(ColorType)
    name = Column(String)
    items = relationship("BekpakListItem", back_populates="owner")


class BekpakListItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    bag_id = Column(Integer, ForeignKey(BekpakBag.id))
    bag = relationship(BekpakBag, back_populates=BekpakBag.items)
    parent_list = Column(Integer, ForeignKey(BekpakTripItemList.id))
    list_index = Column(Integer)
    quantity = Column(Integer)
    name = Column(String)
    description = Column(String)