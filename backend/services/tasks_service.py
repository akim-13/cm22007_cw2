from database.models import Task, User
from sqlalchemy.orm import Session
from services import achievements_service
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)
            
            
def set_task_complete(task_id: int, db: Session) -> dict:
    task: Task = db.query(Task).filter(Task.taskID == task_id).first()
    
    if not task or task.isCompleted:  
        return {"task_changed": False}
    
    task.user.currentPoints += task.duration
    task.isCompleted = True
    
    db.commit()
    
    return {"task_changed": True} | achievements_service.update_from_user(task.username, db)


def set_task_incomplete(task_id: int, db: Session) -> dict:
    task: Task = db.query(Task).filter(Task.taskID == task_id).first()
    
    if not task or not task.isCompleted:  
        return {"task_changed": False, "new_achievements": False}
    
    task.user.currentPoints -= task.duration
    task.isCompleted = False
    
    db.commit()
    
    return {"task_changed": True} | achievements_service.update_from_user(task.username, db)


def delete_task(task_id: int, db: Session) -> dict:
    task = db.query(Task).filter(Task.taskID == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return {"task_deleted": True}
    else:
        {"task_deleted": False}
    