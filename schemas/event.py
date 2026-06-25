from pydantic import BaseModel
from datetime import date


class EventCreate(BaseModel):

    event_name: str

    description: str

    location: str

    event_date: date

    total_seats: int

    available_seats: int
