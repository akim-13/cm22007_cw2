from datetime import datetime
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from sqlalchemy.orm import Session

from database import models
from services import tasks_service, task_scheduler
from main import yield_db

router = APIRouter()

@router.post("/")
def create_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    duration: int = Form(...),
    priority: int = Form(...),
    deadline: datetime = Form(...),
    db: Session = Depends(yield_db),
):  # pragma: no cover
    if priority not in [0, 1, 2]:
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

    task_scheduler.break_down_add_events("joe", new_task.taskID, db)

    return response  # left as-is (matches original)

@router.put("/{taskID}")
def update_task(
    request: Request,
    editID: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    duration: int = Form(...),
    priority: int = Form(...),
    deadline: datetime = Form(...),
    db: Session = Depends(yield_db),
):  # pragma: no cover
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
def delete_task(request: Request, taskID: int, db: Session = Depends(yield_db)):
    response = tasks_service.delete_task(taskID, db)
    return response

@router.put("/{taskID}/complete")
def complete_task(request: Request, taskID: int, db: Session = Depends(yield_db)):
    response = tasks_service.set_task_complete(taskID, db)
    return response

@router.put("/{taskID}/incomplete")
def incomplete_task(request: Request, taskID: int, db: Session = Depends(yield_db)):
    response = tasks_service.set_task_incomplete(taskID, db)
    return response

@router.get("/user/{username}")
def list_user_tasks(request: Request, username: str, db: Session = Depends(yield_db)):
    response = tasks_service.get_user_tasks(username, db)
    return response

@router.get("/user/{username}/latest")
def get_latest_user_task(request: Request, username: str, db: Session = Depends(yield_db)):
    response = tasks_service.get_latest_user_task(username, db)
    return response
