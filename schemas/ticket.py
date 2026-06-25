from pydantic import BaseModel


class TicketResponse(BaseModel):

    ticket_number: str

    attendee_name: str

    event_name: str
