from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    BackgroundTasks
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.event import Event
from models.user import User
from models.registration import Registration
from models.ticket import Ticket

from services.ticket_service import generate_ticket

router = APIRouter(
    tags=["Registrations"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def send_email():

    print("Registration confirmation email sent")


@router.post("/events/{event_id}/register")
def register_event(
    event_id: int,
    user_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:

        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing = db.query(Registration).filter(
        Registration.user_id == user_id,
        Registration.event_id == event_id
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Already registered"
        )

    if event.available_seats <= 0:

        raise HTTPException(
            status_code=400,
            detail="No seats available"
        )

    registration = Registration(
        user_id=user_id,
        event_id=event_id
    )

    db.add(registration)

    event.available_seats -= 1

    db.commit()

    db.refresh(registration)

    ticket = Ticket(
        registration_id=registration.id,
        ticket_number=generate_ticket(),
        attendee_name=user.username,
        event_name=event.event_name
    )

    db.add(ticket)

    db.commit()

    background_tasks.add_task(
        send_email
    )

    return {
        "message":
        "Registration successful"
    }


@router.get("/events/{event_id}/attendees")
def get_attendees(
    event_id: int,
    db: Session = Depends(get_db)
):

    return db.query(Registration).filter(
        Registration.event_id == event_id
    ).all()


@router.delete("/events/{event_id}/cancel-registration")
def cancel_registration(
    event_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    registration = db.query(Registration).filter(
        Registration.event_id == event_id,
        Registration.user_id == user_id
    ).first()

    if not registration:

        raise HTTPException(
            status_code=404,
            detail="Registration not found"
        )

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    event.available_seats += 1

    db.delete(registration)

    db.commit()

    return {
        "message":
        "Registration cancelled"
    }
