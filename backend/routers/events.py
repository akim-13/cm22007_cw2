from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.deps import yield_db
from backend.schemas.events import TaskEventUpdate
from backend.services import events

router = APIRouter()


@router.get("/user/{username}/latest_standalone")
def get_latest_standalone_event(username: str, db: Session = Depends(yield_db)) -> dict:
    """Return the most recent standalone event for a user."""
    return events.get_latest_standalone_event(username, db)


@router.get("/from_task/{task_id}")
def list_events_from_task(task_id: int, db: Session = Depends(yield_db)) -> dict[str, list[dict]]:
    """Return all events linked to a given task."""
    return events.get_events_from_task(task_id, db)


@router.get("/from_user/{username}")
def list_events_from_user(username: str, db: Session = Depends(yield_db)) -> dict[str, list[dict]]:
    """Return all events belonging to a given user."""
    return events.get_all_events(username, db)


@router.delete("/from_task/{task_id}")
def delete_events_from_task(task_id: int, db: Session = Depends(yield_db)) -> dict:
    """Delete all events associated with a task."""
    return events.delete_events_from_task(task_id, db)


@router.put("/task_event/{edit_id}")
def update_task_event(
    edit_id: int,
    update: TaskEventUpdate,
    db: Session = Depends(yield_db),
) -> dict:
    """Update the start and end time of a specific task event."""
    return events.edit_task_event(edit_id, update.start, update.end, db)


@router.delete("/task_event/{task_event_id}")
def delete_task_event(task_event_id: int, db: Session = Depends(yield_db)) -> dict:
    """Delete all events associated with the given ID (likely a task event)."""
    return events.delete_events_from_task(task_event_id, db)
