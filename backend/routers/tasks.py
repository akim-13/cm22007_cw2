from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import models
from backend.database.deps import yield_db
from backend.schemas.tasks import TaskCreateForm, TaskUpdateForm
from backend.services import task_scheduler, tasks

PRIORITY_LOW = 0
PRIORITY_MID = 1
PRIORITY_HIGH = 2

router = APIRouter()


@router.post("/")
def create_task(
    form_data: TaskCreateForm = Depends(TaskCreateForm.as_form),
    db: Session = Depends(yield_db),
) -> dict:  # pragma: no cover
    """Create a new task, save it in the database, and schedule events for it."""
    if form_data.priority not in [PRIORITY_LOW, PRIORITY_MID, PRIORITY_HIGH]:
        raise HTTPException(
            status_code=400,
            detail="Invalid priority value. Must be 0 (low), 1 (medium), or 2 (high).",
        )

    new_task = models.Task(
        title=form_data.title,
        description=form_data.description,
        duration=form_data.duration,
        priority=form_data.priority,
        deadline=form_data.deadline,
        username="joe",  # TODO: replace placeholder with authenticated user
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return task_scheduler.break_down_add_events("joe", new_task.taskID, db)


# TODO: Idk what's up with the taskID path param here, shouldn't it be in the function params?
@router.put("/{taskID}")
def update_task(
    form_data: TaskUpdateForm = Depends(TaskUpdateForm.as_form),
    db: Session = Depends(yield_db),
) -> dict:  # pragma: no cover
    """Update an existing task and reschedule its events."""
    response = tasks.edit_task(
        form_data.editID,
        {
            "title": form_data.title,
            "description": form_data.description,
            "duration": form_data.duration,
            "priority": form_data.priority,
            "deadline": form_data.deadline,
        },
        db,
    )
    task_scheduler.break_down_add_events("joe", form_data.editID, db)
    return response


@router.delete("/{taskID}")
def delete_task(taskID: int, db: Session = Depends(yield_db)) -> dict:
    """Delete a task and its events."""
    return tasks.delete_task(taskID, db)


@router.patch("/{taskID}/complete")
def complete_task(taskID: int, db: Session = Depends(yield_db)) -> dict:
    """Mark a task as complete and update achievements."""
    return tasks.set_task_complete(taskID, db)


@router.patch("/{taskID}/incomplete")
def incomplete_task(taskID: int, db: Session = Depends(yield_db)) -> dict:
    """Mark a task as incomplete and update achievements."""
    return tasks.set_task_incomplete(taskID, db)


@router.get("/user/{username}")
def list_user_tasks(username: str, db: Session = Depends(yield_db)) -> dict[str, Any]:
    """Return all tasks for a user."""
    return tasks.get_user_tasks(username, db)


@router.get("/user/{username}/latest")
def get_latest_user_task(username: str, db: Session = Depends(yield_db)) -> dict:
    """Return the most recent task for a user."""
    return tasks.get_latest_user_task(username, db)
