from datetime import datetime
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from database import models
from services import tasks_service, task_scheduler
from backend.database.deps import yield_db

PRIORITY_LOW = 0
PRIORITY_MID = 1
PRIORITY_HIGH = 2

router = APIRouter()


@router.post("/")
def create_task(
    title: str = Form(...),
    description: str = Form(...),
    duration: int = Form(...),
    priority: int = Form(...),
    deadline: datetime = Form(...),
    db: Session = Depends(yield_db),
) -> dict:  # pragma: no cover
    if priority not in [PRIORITY_LOW, PRIORITY_MID, PRIORITY_HIGH]:
        raise HTTPException(status_code=400, detail="Invalid priority value. Must be 0 (low), 1 (medium), or 2 (high).")
    
    new_task = models.Task(
        title=title,
        description=description,
        duration=duration,
        priority=priority,
        deadline=deadline,
        username="joe",
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    response = task_scheduler.break_down_add_events("joe", new_task.taskID, db)

    return response  


@router.put("/{taskID}")
def update_task(
    editID: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    duration: int = Form(...),
    priority: int = Form(...),
    deadline: datetime = Form(...),
    db: Session = Depends(yield_db),
) -> dict:  # pragma: no cover
    response = tasks_service.edit_task(
        editID,
        {
            "title": title,
            "description": description,
            "duration": duration,
            "priority": priority,
            "deadline": deadline,
        },
        db,
    )
    task_scheduler.break_down_add_events("joe", editID, db)
    return response


@router.delete("/{taskID}")
def delete_task(
    taskID: int,
    db: Session = Depends(yield_db),
) -> dict:
    response = tasks_service.delete_task(taskID, db)
    return response


@router.put("/{taskID}/complete")
def complete_task(
    taskID: int,
    db: Session = Depends(yield_db),
) -> dict:
    response = tasks_service.set_task_complete(taskID, db)
    return response


@router.put("/{taskID}/incomplete")
def incomplete_task(
    taskID: int,
    db: Session = Depends(yield_db),
) -> dict:
    response = tasks_service.set_task_incomplete(taskID, db)
    return response


@router.get("/user/{username}")
def list_user_tasks(
    username: str,
    db: Session = Depends(yield_db),
) -> list[dict]:
    response = tasks_service.get_user_tasks(username, db)
    return response


@router.get("/user/{username}/latest")
def get_latest_user_task(
    username: str,
    db: Session = Depends(yield_db),
) -> dict:
    response = tasks_service.get_latest_user_task(username, db)
    return response
