from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime
from sqlalchemy_utc import utcnow


class TimestampsMixin:
    time_created = Column(
        DateTime, default=utcnow(), server_default=utcnow(), nullable=False, index=True
    )
    time_updated = Column(DateTime, onupdate=utcnow(), index=True)
