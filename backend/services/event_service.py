from database.models import Event, Standalone_Event, Task, User
from sqlalchemy.orm import Session
from datetime import datetime
from tools import convertToJson


def get_events(username: str, interval: tuple[datetime, datetime], db: Session) -> dict:
    """Return list of achievements for the given user in json format"""
    user_events = db.query(User).filter(User.username == username).first().events
    
    events = [event for event in user_events if event.start > interval[0] and event.start < interval[1]]

    return {"events": [convertToJson(event) for event in events]}


def edit_event(eventID: int, new_start: datetime, new_end: datetime, db: Session):
    event = db.query(Event).filter(Event.eventID == eventID).first()
    event.start = new_start
    event.end = new_end
    db.commit()
    
    return {"success": True}
    


def get_standalone_events(username: int, interval: tuple[datetime, datetime], db: Session):
    events = db.query(Standalone_Event).filter(
        Standalone_Event.username == username, 
        Standalone_Event.start < interval[0], 
        Standalone_Event.start > interval[1]).all()

    return {"standalone_events": [convertToJson(event) for event in events]}


def get_events_from_task(taskID: int, db: Session):
    events = db.query(Task).filter(Task.taskID == taskID).first().events
    return {"events": [convertToJson(event) for event in events]}    
