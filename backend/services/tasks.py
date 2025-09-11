from typing import Any, Dict

from database.models import Task, User
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.services import achievements
from tools import convertToJson


def get_user_tasks(username: str, db: Session) -> Dict[str, Any]:
    """Return all tasks for a user as JSON, or an empty list if none exist."""

    tasks = db.query(Task).filter(Task.username == username).all()

    return {"tasks": [convertToJson(task) for task in tasks]} if tasks else {"tasks": []}


def get_latest_user_task(username: str, db: Session) -> Dict[str, Any]:
    """Return the most recent task for a user, or None if none exist."""

    latest_task = (
        db.query(Task)
        .filter(Task.username == username)
        .order_by(desc(Task.taskID))
        .first()
    )

    return {"latest_task": convertToJson(latest_task)} if latest_task else {"latest_task": None}


def edit_task(taskID: int, task_properties: Dict[str, Any], db: Session) -> Dict[str, bool]:
    """Update a task’s attributes if valid and types match; reject otherwise."""

    task = db.query(Task).filter(Task.taskID == taskID).first()
    for attribute, value in task_properties.items():
        if not hasattr(task, attribute) or attribute == "taskID":
            return {"success": False}
        if type(getattr(task, attribute)) != type(value):
            return {"success": False}
        setattr(task, attribute, value)

    db.merge(task)
    db.commit()

    return {"success": True}


def set_task_complete(task_id: int, db: Session) -> Dict[str, Any]:
    """Mark a task complete, add points, and update achievements."""

    task: Task = db.query(Task).filter(Task.taskID == task_id).first()
    if not task or task.isCompleted:
        return {"task_changed": False}

    task.user.currentPoints += task.duration
    task.isCompleted = True
    db.commit()

    return {"task_changed": True} | achievements.update_from_user(task.username, db)


def set_task_incomplete(task_id: int, db: Session) -> Dict[str, Any]:
    """Mark a task incomplete, remove points, and update achievements."""

    task: Task = db.query(Task).filter(Task.taskID == task_id).first()
    if not task or not task.isCompleted:
        return {"task_changed": False, "new_achievements": False}

    task.user.currentPoints -= task.duration
    task.isCompleted = False
    db.commit()

    return {"task_changed": True} | achievements.update_from_user(task.username, db)


def delete_task(task_id: int, db: Session) -> Dict[str, bool]:
    """Delete a task if it exists, otherwise return false."""

    task = db.query(Task).filter(Task.taskID == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return {"task_deleted": True}

    return {"task_deleted": False}
