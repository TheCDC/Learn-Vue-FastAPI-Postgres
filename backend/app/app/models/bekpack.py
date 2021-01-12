from typing import TYPE_CHECKING
from app.models.mixins import TimestampsMixin


from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy_utils.types import ColorType

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class BekPackTrip_Members(Base):
    id = Column(Integer, primary_key=True)
    trip = relationship("BekpackTrip")
    trip_id = Column(
        Integer, ForeignKey("bekpacktrip.id", ondelete="CASCADE"), index=True
    )
    user = relationship("BekpackUser")
    user_id = Column(
        Integer, ForeignKey("bekpackuser.id", ondelete="CASCADE"), index=True
    )


class BekpackUser(Base):
    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean(), default=True)
    joined_trips = relationship(
        "BekpackTrip",
        secondary=BekPackTrip_Members.__table__,
        back_populates="members",
    )
    owned_bags = relationship("BekpackBag", back_populates="owner")
    owned_trips = relationship("BekpackTrip", back_populates="owner")
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), unique=True)


class BekpackTrip(Base, TimestampsMixin):
    id = Column(Integer, primary_key=True, index=True)
    bags = relationship("BekpackBag", back_populates="owner_trip")
    color = Column(String)
    description = Column(String)
    is_active = Column(Boolean(), default=True)
    members = relationship(
        BekpackUser,
        secondary=BekPackTrip_Members.__table__,
        back_populates="joined_trips",
    )
    name = Column(String, index=True)
    owner = relationship(BekpackUser, back_populates="owned_trips")
    owner_id = Column(
        Integer, ForeignKey(BekpackUser.id, ondelete="CASCADE"), index=True
    )
    items_lists = relationship("BekpackTripItemList", back_populates="parent_trip")


class BekpackTripItemList(Base):
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    parent_trip_id = Column(
        Integer, ForeignKey(BekpackTrip.id, ondelete="cascade"), index=True
    )
    parent_trip = relationship(BekpackTrip, back_populates="items_lists")
    parent_user_id = Column(
        Integer, ForeignKey(BekpackUser.id, ondelete="cascade"), primary_key=True
    )


class BekpackBag(Base):
    color = Column(String)
    id = Column(Integer, primary_key=True, index=True)
    items = relationship("BekpackListItem", backref="bag")
    name = Column(String)
    owner = relationship(BekpackUser, back_populates="owned_bags")
    owner_id = Column(
        Integer, ForeignKey(BekpackUser.id, ondelete="CASCADE"), index=True
    )
    owner_trip = relationship(BekpackTrip, back_populates="bags")
    owner_trip_id = Column(
        Integer, ForeignKey(BekpackTrip.id, ondelete="CASCADE"), index=True
    )


class BekpackListItem(Base):
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
