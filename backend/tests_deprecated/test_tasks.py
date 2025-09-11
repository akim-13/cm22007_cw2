import pytest, os, sys
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from backend.services import events, tasks, users
from database.dbsetup import ORM_Base
from database.models import Task, User

from services import task_scheduler

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
                       deadline=datetime(2025, 4, 6, 20), username=username),
            Task(title="Painting", 
                       description="Work on my painting project where im drawing a detailed picture of the eiffel tower", 
                       duration=500, 
                       priority=3, 
                       deadline=datetime(2025, 4, 17, 20), username=username)]
    for task in tasks:
        db_session.add(task)
    db_session.commit()
    return tasks


# ---------------------- TASK SERVICE ----------------------

def test_adding_tasks(db_session):
    """Add tasks, and check whether the user now has these tasks"""
    task1, task2 = add_tasks(db_session)

    tasks = tasks.get_user_tasks(username, db_session).get("tasks")
    assert tasks is not None
    assert len(tasks) == 2
    assert tasks[0]["title"] == task1.title
    assert tasks[1]["title"] == task2.title

def test_deleting_tasks(db_session):
    """Delete task, and check whether it's actually deleted, and then try deleting a task that doesn't exist"""
    task1, task2 = add_tasks(db_session)
    
    # delete task1
    assert tasks.delete_task(task1.taskID, db_session).get("task_deleted")
    tasks = tasks.get_user_tasks(username, db_session).get("tasks") 
    assert tasks is not None
    assert len(tasks) == 1
    assert tasks[0]["title"] == task2.title  # task2 should only be in the table now
    
    assert not tasks.delete_task(10, db_session).get("task_deleted") # Task with task id == 10 doesn't exist
    
def test_edit_task(db_session):
    """Edit task and see whether changes are made. Edit task that doesn't exist. edit various task fields. 
    Edit primary key of task"""
    task1, task2 = add_tasks(db_session)
    
    assert tasks.edit_task(task1.taskID, dict(title="CS Coursework", duration=1200), db_session).get("success")
    tasks = tasks.get_user_tasks(username, db_session).get("tasks")
    assert tasks[0]["title"] == "CS Coursework" 
    assert tasks[0]["duration"] == 1200
    
    # editing task that doesn't exist
    assert not tasks.edit_task(10, dict(title="CS coursework"), db_session).get("success")
    
    # editing fields that don't exist on a task that does exist
    assert not tasks.edit_task(task1.taskID, dict(humidity=23), db_session).get("success")
    
    # editing a valid field, but with wrong datatype
    assert not tasks.edit_task(task1.taskID, dict(title=23), db_session).get("success")
    tasks = tasks.get_user_tasks(username, db_session).get("tasks")
    assert tasks[0]["title"] == "CS Coursework"
    
    # editing the primary key of the task (shouldn't allow)
    assert not tasks.edit_task(task1.taskID, dict(taskID=23), db_session).get("success")
    tasks = tasks.get_user_tasks(username, db_session).get("tasks")
    assert tasks[0]["taskID"] == 1
    
def test_task_completion(db_session):
    """Mark tasks complete or incomplete, check user points have updated"""
    task1, task2 = add_tasks(db_session)
    
    tasks.set_task_complete(task1.taskID, db_session)
    tasks.set_task_complete(task2.taskID, db_session)
    points = users.get_user_points(username, db_session).get("points")
    assert points == task1.duration + task2.duration
    
    # Set task 2 to be incomplete and check points again
    tasks.set_task_incomplete(task2.taskID, db_session)
    points = users.get_user_points(username, db_session).get("points")
    assert points == task1.duration


# ---------------------- TASK SCHEDULER (some event services as well) ----------------------

@pytest.mark.external_api
def test_task_scheduler(db_session):
    """After breaking down a task, check whether events generated are valid"""
    task1, task2 = add_tasks(db_session)
    
    message = task_scheduler.break_down_add_events(username, task1.taskID, db_session)
    
    events = events.get_events_from_task(task1.taskID, db_session).get("events")
    assert events is not None
    assert len(events) == len(message["events_added"])
    
    # task1's description states I need to work at least 10 times, implying at least 10 events
    assert len(message["events_added"]) >= 10  
    
    # test whether the number of events added is the same as when we retrieve it from the task
    events = events.get_events_from_task(task1.taskID, db_session)["events"]
    assert len(events) == len(message["events_added"])
    
    # Check whether it handles tasks that haven't been broken down into events yet
    events = events.get_events_from_task(task2.taskID, db_session)["events"]
    assert events == []
    
    db_session.close()
    