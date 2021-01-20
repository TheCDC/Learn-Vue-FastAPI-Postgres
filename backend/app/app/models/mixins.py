from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime
from sqlalchemy_utc import utcnow


class TimestampsMixin:
    time_created = Column(
        DateTime, default=utcnow(), server_default=utcnow(), nullable=False, index=True
    )
    time_updated = Column(
        DateTime,
        default=utcnow(),
        onupdate=utcnow(),
        server_default=utcnow(),
        index=True,
    )
