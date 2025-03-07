import pytest
from datetime import datetime
from sqlalchemy import create_engine
import os, sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from database.models import Task, User, Event
from services.task_scheduler import break_down_add_events
from services.tasks_service import get_user_tasks

from database.dbsetup import ORM_Base, SessionLocal

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
    
    db.add(test_user)
    db.commit()
    
    # Check if user is in db, to see if db works
    users = db.query(User).filter(User.username == "test_user").all()
    assert len(users) == 1
    assert users[0].username == "test_user"
    
    # Add 2 tasks
    task1 = Task(title="Maths coursework", 
                       description="important group maths coursework. I need to work on it at least 10 times before the deadline", 
                       duration=700, 
                       priority=1, 
                       deadline=datetime(2025, 4, 6, 20), username="test_user")
    
    task2 = Task(title="Painting", 
                       description="Work on my painting project where im drawing a detailed picture of the eiffel tower", 
                       duration=700, 
                       priority=3, 
                       deadline=datetime(2025, 4, 17, 20), username="test_user")
    db.add(task1)
    db.add(task2)
    db.commit()

    # Check whether the user has two tasks now
    tasks = get_user_tasks("test_user", db).get("tasks")
    assert tasks is not None
    assert len(tasks) == 2
    
    
    # Next: Break down one of the tasks and see if it:
    # - generates events for that task
    # - breaks it down into appropriately spaced events