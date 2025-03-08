import pytest
from datetime import datetime
from sqlalchemy import create_engine
import os, sys
from database.models import Task, User, Event
from services.task_scheduler import break_down_add_events
from services.tasks_service import get_user_tasks
from services.event_service import get_events_from_task

from database.dbsetup import ORM_Base, SessionLocal

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

engine = create_engine("sqlite:///./test_task_scheduler.db", connect_args={"check_same_thread": False})

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    ORM_Base.metadata.drop_all(bind=engine)
    ORM_Base.metadata.create_all(bind=engine)
    yield
    # Optional: drop again after all tests
    ORM_Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()


def test_task(db):
    # Create a test user with low points
    test_user = User(
        username="test_user",
        hashedPassword="fakeHashedPassword123",
        streakDays=0,
        currentPoints=0,
        stressLevel=0
    )    