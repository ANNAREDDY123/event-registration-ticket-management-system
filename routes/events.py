from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from datetime import date

from database import SessionLocal

from models.event import Event

from schemas.event import EventCreate

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):

    if event.event_date <= date.today():

        raise HTTPException(
            status_code=400,
            detail="Event date must be in future"
        )

    if event.total_seats <= 0:

        raise HTTPException(
            status_code=400,
            detail="Total seats must be greater than zero"
        )

    new_event = Event(
        event_name=event.event_name,
        description=event.description,
        location=event.location,
        event_date=event.event_date,
        total_seats=event.total_seats,
        available_seats=event.available_seats
    )

    db.add(new_event)

    db.commit()

    db.refresh(new_event)

    return new_event


@router.get("/")
def get_events(
    location: str = None,
    date_filter: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(Event)

    if location:

        query = query.filter(
            Event.location == location
        )

    return query.all()


@router.get("/{event_id}")
def get_event(
    event_id: int,
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

    return event


@router.put("/{event_id}")
def update_event(
    event_id: int,
    event: EventCreate,
    db: Session = Depends(get_db)
):

    db_event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not db_event:

        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    db_event.event_name = event.event_name
    db_event.description = event.description
    db_event.location = event.location
    db_event.event_date = event.event_date
    db_event.total_seats = event.total_seats
    db_event.available_seats = event.available_seats

    db.commit()

    return {
        "message":
        "Event updated"
    }


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
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

    db.delete(event)

    db.commit()

    return {
        "message":
        "Event deleted"
    }
