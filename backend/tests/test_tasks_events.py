from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os, sys
from database.models import Task, User, Event
from services.task_scheduler import break_down_add_events
from services.tasks_service import get_user_tasks, set_task_complete, set_task_incomplete
from services.event_service import get_events_from_task

from services.event_service import get_events_from_task

from database.dbsetup import ORM_Base

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

engine = create_engine("sqlite:///./test_task_scheduler.db", connect_args={"check_same_thread": False})
ORM_Base.metadata.drop_all(bind=engine)
ORM_Base.metadata.create_all(bind=engine)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = session()

current_username = "joe"

def test_task():
    # Create a test user
    test_user = User(
        username=current_username,
        hashedPassword="fakeHashedPassword123",
        streakDays=0,
        currentPoints=0,
        stressLevel=0
    )
    
    db.add(test_user)
    db.commit()
    
    # Check if user is in db, to see if db works
    users = db.query(User).filter(User.username == current_username).all()
    assert len(users) == 1
    user = users[0]
    assert user.username == current_username
    
    # Add 2 tasks
    task1 = Task(title="Maths coursework", 
                       description="important group maths coursework. I need to work on it at least 10 times before the deadline", 
                       duration=1000, 
                       priority=1, 
                       deadline=datetime(2025, 4, 6, 20), username=current_username)
    
    task2 = Task(title="Painting", 
                       description="Work on my painting project where im drawing a detailed picture of the eiffel tower", 
                       duration=500, 
                       priority=3, 
                       deadline=datetime(2025, 4, 17, 20), username=current_username)
    db.add(task1)
    db.add(task2)
    db.commit()

    # Check whether the user has two tasks now
    tasks = get_user_tasks(current_username, db).get("tasks")
    assert tasks is not None
    assert len(tasks) == 2
    
    # Break down a task, and:
    # - check whether no. of events is >= how many we specified in the description of first task
    # - check that the events have been added to the db by quering them
    message = break_down_add_events(current_username, taskID=1, db=db)
    assert message["events_added"] >= 10
    
    events = get_events_from_task(taskID=1, db=db).get("events")
    assert events is not None
    assert len(events) == message["events_added"]
    
    # Assign tasks to be complete, then check that the user points have increased
    set_task_complete(task1.taskID, db)
    set_task_complete(task2.taskID, db)
    user = db.query(User).filter(User.username == current_username).first()
    assert user.currentPoints == task1.duration + task2.duration
    
    # Set task 2 to be incomplete and check points again
    set_task_incomplete(task2.taskID, db)
    user = db.query(User).filter(User.username == current_username).first()
    assert user.currentPoints == task1.duration
    
    # test whether the number of events added is the same as when we retrieve it from the task
    events = get_events_from_task(task1.taskID, db)["events"]
    assert len(events) == message["events_added"]
    
    # Check whether it handles tasks that haven't been broken down into events yet
    events = get_events_from_task(task2.taskID, db)["events"]
    assert events == []
    
    db.close()
    