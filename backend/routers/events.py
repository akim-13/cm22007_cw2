from datetime import datetime
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from services import event_service
from backend.database.deps import yield_db

router = APIRouter()


@router.get("/user/{username}/latest_standalone")
def get_latest_standalone_event(
    username: str,
    db: Session = Depends(yield_db),
) -> dict:
    return event_service.get_latest_standalone_event(username, db)


@router.get("/from_task/{taskID}")
def list_events_from_task(
    taskID: int,
    db: Session = Depends(yield_db),
) -> dict[str, list[dict]]:
    return event_service.get_events_from_task(taskID, db)


@router.get("/from_user/{username}")
def list_events_from_user(
    username: str,
    db: Session = Depends(yield_db),
) -> dict[str, list[dict]]:
    return event_service.get_all_events(username, db)


@router.delete("/from_task/{taskID}")
def delete_events_from_task(
    taskID: int,
    db: Session = Depends(yield_db),
) -> dict:
    return event_service.delete_events_from_task(taskID, db)


@router.put("/task_event/{editID}")
def update_task_event(
    editID: int = Form(),
    start: datetime = Form(),
    end: datetime = Form(),
    db: Session = Depends(yield_db),
) -> dict:
    return event_service.edit_task_event(editID, start, end, db)


@router.delete("/task_event/{taskEvId}")
def delete_task_event(
    taskEvId: int,
    db: Session = Depends(yield_db),
) -> dict:
    return event_service.delete_events_from_task(taskEvId, db)
