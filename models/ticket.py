from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from datetime import datetime

from database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(
        Integer,
        primary_key=True
    )

    registration_id = Column(
        Integer,
        ForeignKey("registrations.id")
    )

    ticket_number = Column(
        String,
        unique=True
    )

    attendee_name = Column(String)

    event_name = Column(String)

    registration_date = Column(
        DateTime,
        default=datetime.utcnow
    )
