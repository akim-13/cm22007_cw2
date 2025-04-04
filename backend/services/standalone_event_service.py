from database.models import Standalone_Event
from sqlalchemy.orm import Session
from tools import convertToJson


def get_user_standalone_event_obj(username: str, db: Session) -> list[Standalone_Event]:
    return db.query(Standalone_Event).filter(Standalone_Event.username == username).all()


def get_user_standalone_events(username: str, db: Session) -> dict:
    standalone_events = get_user_standalone_event_obj(username, db)
    json_standalone_events = [convertToJson(standalone_event) for standalone_event in standalone_events]
    return {"standalone_events": json_standalone_events}


def delete_user_standalone_events(username: str, db: Session) -> dict:
    standalone_events = get_user_standalone_event_obj(username, db)
    for standalone_event in standalone_events:
        db.delete(standalone_event)
    db.commit()
    return {"message": "All standalone events deleted"}


def delete_user_standalone_event(standaloneEventID: int, db: Session) -> dict:
    standalone_event = db.query(Standalone_Event).filter(Standalone_Event.standaloneEventID == standaloneEventID).first()
    if standalone_event:
        db.delete(standalone_event)
        db.commit()
        return {"standalone_event_deleted": True}
    else:
        return {"standalone_event_deleted": False} 