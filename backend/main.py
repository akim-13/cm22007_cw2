import uvicorn

from datetime import datetime
from fastapi import HTTPException, Form
from config import default_achievements

# DB stuff
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import models, SessionLocal, engine, ORM_Base, User
from database.models import Achievements, Standalone_Event
from services import achievements_service, tasks_service, task_scheduler, event_service, user_service, autofill, standalone_event_service

# FastAPI stuff
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Routers
from routers import users, achievements, tasks, events, calendars


# Calendar stuff
import calendar_to_events
import repeat_weekly

from contextlib import asynccontextmanager

def get_all_external_cal_sources(db: Session):
    sources = [
        source
        for (source,) in (
            db.query(Standalone_Event.eventBy)
            .filter(Standalone_Event.eventBy.isnot(None))
            .distinct()
            .all()
        )
    ]
    return sources


def update_all_external_cals(db: Session):
    sources = get_all_external_cal_sources(db)
    for source in sources:
        repeat_weekly.sync_db_with_external_cal(source, db)

def initialise_achievements(db):
    """Check if achievements exist and insert them if missing."""
    if db.query(Achievements).count() == 0:
        for data in default_achievements:
            db.add(Achievements(**data))
        db.commit()
    else:
        print("Achievements already exist, skipping population.")


def seed_joe_user(db):
    user = db.query(User).filter(User.username == "joe").first()
    if not user:
        db.add(User(username="joe", hashedPassword="x", streakDays=0, currentPoints=0, stressLevel=0))
        db.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    ORM_Base.metadata.create_all(bind=engine)  

    with SessionLocal() as db:
        update_all_external_cals(db)
        initialise_achievements(db)
        seed_joe_user(db)

    #↑ STARTUP CODE ↑
    yield   # App runs.
    #↓ SHUTDOWN CODE ↓

    print("Shutting down...")

# TODO: See what's needed from here.
#
# Fix verbs and forms for mutating endpoints (examples):
# 
# @app.post("/users")
# def create_user(payload: CreateUser, db: Session = Depends(yield_db)):
#     return user_service.create_user(payload.username, payload.password, db)
# 
# @app.post("/tasks")
# def add_task(form: AddTaskForm = Depends(), db: Session = Depends(yield_db)):
#     new_task = models.Task(...); db.add(new_task); db.commit(); db.refresh(new_task)
#     task_scheduler.break_down_add_events(form.username, new_task.taskID, db)
#     return {"success": True, "taskID": new_task.taskID}

app = FastAPI(lifespan=lifespan)

# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# This creates new user db session each request
# A global db var introduces issues with multiple users accessing same db session
def yield_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def run_app():  # pragma: no cover
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(achievements.router, prefix="/achievements", tags=["achievements"])
    app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
    app.include_router(events.router, prefix="/events", tags=["events"])
    app.include_router(calendars.router, prefix="/calendars", tags=["calendars"])

    return app

if __name__ == "__main__": # pragma: no cover
    uvicorn.run("backend.main:run_app", host="127.0.0.1", port=8000, reload=True, factory=True)
