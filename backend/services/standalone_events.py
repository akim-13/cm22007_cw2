from datetime import datetime

from sqlalchemy.orm import Session

from backend.database.models import Standalone_Event
from backend.tools.jsonify import convertToJson


def get_user_standalone_event_obj(username: str, db: Session) -> list[Standalone_Event]:
    """Return a list of standalone event ORM objects for the given user."""
    return db.query(Standalone_Event).filter(Standalone_Event.username == username).all()


def get_user_standalone_events(username: str, db: Session) -> dict:
    """Return all standalone events for a user in JSON format."""
    standalone_events = get_user_standalone_event_obj(username, db)
    json_standalone_events = [
        convertToJson(standalone_event) for standalone_event in standalone_events
    ]
    return {"standalone_events": json_standalone_events}


def delete_user_standalone_events(username: str, db: Session) -> dict:
    """Delete all standalone events for the given user."""
    standalone_events = get_user_standalone_event_obj(username, db)
    for standalone_event in standalone_events:
        db.delete(standalone_event)
    db.commit()
    return {"message": "All standalone events deleted"}


def edit_standalone_event(
    standaloneEventID: int,
    standaloneEventName: str,
    standaloneEventDescription: str,
    start: datetime,
    end: datetime,
    db: Session,
) -> dict:
    """Edit an existing standalone event if found, otherwise return an error message."""
    standalone_event = (
        db.query(Standalone_Event)
        .filter(Standalone_Event.standaloneEventID == standaloneEventID)
        .first()
    )
    if standalone_event is None:
        return {"success": False, "message": "Event not found"}

    standalone_event.standaloneEventName = standaloneEventName
    standalone_event.standaloneEventDescription = standaloneEventDescription
    standalone_event.start = start
    standalone_event.end = end
    db.commit()

    return {"success": True}


def delete_user_standalone_event(standaloneEventID: int, db: Session) -> dict:
    """Delete a single standalone event by its ID."""
    standalone_event = (
        db.query(Standalone_Event)
        .filter(Standalone_Event.standaloneEventID == standaloneEventID)
        .first()
    )
    if standalone_event:
        db.delete(standalone_event)
        db.commit()
        return {"standalone_event_deleted": True}
    else:
        return {"standalone_event_deleted": False}
