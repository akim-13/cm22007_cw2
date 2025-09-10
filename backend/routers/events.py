from datetime import datetime
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session

from services import event_service
from main import yield_db

router = APIRouter()

@router.get("/user/{username}/latest_standalone")
def get_latest_standalone_event(request: Request, username: str, db: Session = Depends(yield_db)):
    response = event_service.get_latest_standalone_event(username, db)
    return response

@router.get("/from_task/{taskID}")
def list_events_from_task(request: Request, taskID: int, db: Session = Depends(yield_db)):
    return event_service.get_events_from_task(taskID, db)

@router.get("/from_user/{username}")
def list_events_from_user(request: Request, username: str, db: Session = Depends(yield_db)):
    return event_service.get_all_events(username, db)

@router.delete("/from_task/{taskID}")
def delete_events_from_task(request: Request, taskID: int, db: Session = Depends(yield_db)):
    return event_service.delete_events_from_task(taskID, db)

@router.put("/task_event/{editID}")
def update_task_event(
    request: Request,
    editID: int = Form(),
    start: datetime = Form(),
    end: datetime = Form(),
    db: Session = Depends(yield_db),
):
    return event_service.edit_task_event(editID, start, end, db)

@router.delete("/task_event/{taskEvId}")
def delete_task_event(request: Request, taskEvId: int, db: Session = Depends(yield_db)):
    return event_service.delete_events_from_task(taskEvId, db)
