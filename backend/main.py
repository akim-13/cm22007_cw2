# TODO: See what's needed from here.
#
# Fix verbs and forms for mutating endpoints (examples):
# 
# @app.post("/users")
# def create_user(payload: CreateUser, db: Session = Depends(yield_db)):
#     return user_service.create_user(payload.username, payload.password, db)
# 
# @app.post("/tasks")
# def add_task(form: AddTaskForm = Depends(), db: Session = Depends(yield_db)):
#     new_task = models.Task(...); db.add(new_task); db.commit(); db.refresh(new_task)
#     task_scheduler.break_down_add_events(form.username, new_task.taskID, db)
#     return {"success": True, "taskID": new_task.taskID}

# TODO: 
# - Return type annotations.
# - Replace long func signatures with Pydantic models, e.g.:
#   @router.put("/{taskID}")
#   def update_task(
#       payload: TaskUpdate,
#       db: Session = Depends(yield_db),
#   ) -> dict:
#       response = tasks_service.edit_task(
#           payload.editID,
#           {
#               "title": payload.title,
#               "description": payload.description,
#               "duration": payload.duration,
#               "priority": payload.priority,
#               "deadline": payload.deadline,
#           },
#           db,
#       )
#       task_scheduler.break_down_add_events("joe", payload.editID, db)
#       return response
#
# - Docstrings.


import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, ORM_Base, engine
from routers import users, achievements, tasks, events, calendars
from tools.startup import startup


@asynccontextmanager
async def lifespan(_: FastAPI):
    ORM_Base.metadata.create_all(bind=engine)  

    with SessionLocal() as db:
        startup(db)

    #↑ STARTUP CODE ↑
    yield   # App runs.
    #↓ SHUTDOWN CODE ↓

    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

# Allow requests from the frontend.
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], 
)


def run_app():  # pragma: no cover
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(achievements.router, prefix="/achievements", tags=["achievements"])
    app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
    app.include_router(events.router, prefix="/events", tags=["events"])
    app.include_router(calendars.router, prefix="/calendars", tags=["calendars"])

    return app


if __name__ == "__main__": # pragma: no cover
    uvicorn.run("backend.main:run_app", host="127.0.0.1", port=8000, reload=True, factory=True)
