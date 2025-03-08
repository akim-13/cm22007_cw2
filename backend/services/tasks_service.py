from database.models import Task, User
from sqlalchemy.orm import Session
from sqlalchemy import desc
from services import achievements_service
from tools import convertToJson


def get_user_task_obj(username: str, db: Session) -> list[Task]:
    return db.query(Task).filter(Task.username == username).all()


def get_user_task(username: str, db: Session) -> dict:
    tasks = db.query(Task).filter(User.username == username).all()
    json_tasks = [convertToJson(task) for task in tasks]
    return {"tasks": json_tasks}


def get_latest_user_task(username: str, db: Session) -> dict:
    latest_task = db.query(Task).filter(User.username == username).order_by(desc(Task.taskID)).first()

    if latest_task:
        return {"latest_task": convertToJson(latest_task)}
    else:
        return {"latest_task": None}
    

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
    
