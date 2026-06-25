from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import (
    Base,
    engine
)

from models.user import User
from models.event import Event
from models.registration import Registration
from models.ticket import Ticket

from routes.auth import router as auth_router
from routes.events import router as event_router
from routes.registrations import router as registration_router
from routes.tickets import router as ticket_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Event Registration & Ticket Management System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(event_router)
app.include_router(registration_router)
app.include_router(ticket_router)


@app.get("/")
def home():

    return {
        "message":
        "Event Registration & Ticket Management System"
    }
