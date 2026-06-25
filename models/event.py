from sqlalchemy import (
    Column,
    Integer,
    String,
    Date
)

from database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(
        Integer,
        primary_key=True
    )

    event_name = Column(String)

    description = Column(String)

    location = Column(String)

    event_date = Column(Date)

    total_seats = Column(Integer)

    available_seats = Column(Integer)
