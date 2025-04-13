import pytest, os, sys
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database.dbsetup import ORM_Base
from database.models import Task, User, Event, Standalone_Event

from services import event_service

username = "joe"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
engine = create_engine("sqlite:///:memory:", echo=False)

@pytest.fixture(scope="session")
def setup_db():
    ORM_Base.metadata.create_all(bind=engine)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    
    test_user = User(username=username, hashedPassword="123", streakDays=0, currentPoints=0, stressLevel=0)
    session.add(test_user)
    session.commit()
    
    yield Session
    
    ORM_Base.metadata.drop_all(bind=engine)
    
    
@pytest.fixture(scope="function")  # Create new db for each test function
def db_session(setup_db):
    session = setup_db()
    
    yield session  # Provide the session to tests
    
    session.rollback()  # Rollback any changes after a single test function
    session.close()
    
    ORM_Base.metadata.drop_all(bind=engine)
    ORM_Base.metadata.create_all(bind=engine)
    test_user = User(username=username, hashedPassword="123", streakDays=0, currentPoints=0, stressLevel=0)
    session.add(test_user)
    session.commit()
    
    
def add_tasks(db_session):
    tasks = [Task(title="Maths coursework", 
                       description="important group maths coursework. I need to work on it at least 10 times before the deadline", 
                       duration=1000, 
                       priority=1, 
                       deadline=datetime(2025, 5, 6, 20), username=username),
            Task(title="Painting", 
                       description="Work on my painting project where im drawing a detailed picture of the eiffel tower", 
                       duration=500, 
                       priority=3, 
                       deadline=datetime(2025, 5, 17, 20), username=username)]
    for task in tasks:
        db_session.add(task)
    db_session.commit()
    return tasks

def add_events(db_session):
    events = [
        Event(taskID=1, start=datetime(2025, 4, 20, 12), end=datetime(2025, 4, 20, 14)),
        Event(taskID=1, start=datetime(2025, 4, 20, 19), end=datetime(2025, 4, 20, 20)),
        Event(taskID=1, start=datetime(2025, 4, 22, 14), end=datetime(2025, 4, 20, 16)),
        Event(taskID=1, start=datetime(2025, 4, 25, 17), end=datetime(2025, 4, 20, 19)),
        
        Event(taskID=2, start=datetime(2025, 4, 27, 12), end=datetime(2025, 4, 20, 14)),
        Event(taskID=2, start=datetime(2025, 4, 28, 19), end=datetime(2025, 4, 20, 20)),
        Event(taskID=2, start=datetime(2025, 5, 5, 14), end=datetime(2025, 4, 20, 16)),
        Event(taskID=2, start=datetime(2025, 5, 10, 17), end=datetime(2025, 4, 20, 19))
        ]
    
    for event in events:
        db_session.add(event)
    db_session.commit()
    
    
def add_standalone_events(db_session):
    standalone_events = [
        Standalone_Event(username=username, start=datetime(2025, 4, 20, 10), end=datetime(2025, 4, 20, 11),
                         standaloneEventName="Pack suitcase", standaloneEventDescription="organise clothes and items in suitcase neatly for this afternoons journey"),
        Standalone_Event(username=username, start=datetime(2025, 5, 21, 11), end=datetime(2025, 5, 21, 13),
                         standaloneEventName="Boxing practice", standaloneEventDescription="go to boxing practice. remember to bring gloves")
        ]
    
    for standalone_event in standalone_events:
        db_session.add(standalone_event)
    db_session.commit()


# ---------------------- EVENT SERVICE (`get_events_from_task` tested in test_tasks.py) ----------------------

def test_get_events(db_session):
    """test whether filtering for a time interval works properly in the get_events function"""
    add_tasks(db_session); add_events(db_session)
    
    events = event_service.get_events(username, (datetime(2025, 1, 1), datetime(2026, 1, 1)), db_session).get("events")
    assert len(events) == 8
    
    events = event_service.get_events(username, (datetime(2025, 4, 22), datetime(2025, 4, 28)), db_session).get("events")
    assert len(events) == 3
    
def test_edit_event(db_session):
    """Edit an event to change its time slot"""
    add_tasks(db_session); add_events(db_session)
    
    events = event_service.get_events_from_task(1, db_session).get("events")
    assert len(events) == 4
    eventID = events[0]["eventID"]
    
    event_service.edit_task_event(eventID, datetime(2025, 4, 22, 12), datetime(2025, 4, 22, 14), db_session)
    
    # Should be 5 instead of 4 because we editing the event above to be in this time slot as well
    events = event_service.get_events(username, (datetime(2025, 4, 22), datetime(2025, 4, 29)), db_session).get("events")
    assert len(events) == 5
    
def test_get_standalone_event(db_session):
    add_standalone_events(db_session)
    sv = event_service.get_standalone_events(username, (datetime(2025, 1, 1), datetime(2026, 1, 1)), db_session).get("standalone_events")
    assert sv is not None
    assert len(sv) == 2
    
    sv = event_service.get_standalone_events(username, (datetime(2025, 5, 1), datetime(2026, 1, 1)), db_session).get("standalone_events")
    assert sv is not None
    assert len(sv) == 1
    assert sv[0]["standaloneEventName"] == "Boxing practice"
