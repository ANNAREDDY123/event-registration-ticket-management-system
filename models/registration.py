from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime
)

from datetime import datetime

from database import Base


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    event_id = Column(
        Integer,
        ForeignKey("events.id")
    )

    registration_date = Column(
        DateTime,
        default=datetime.utcnow
    )
