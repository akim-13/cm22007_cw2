from datetime import datetime
import logging  # To debug -> Can't print, as the file isn't executed normally

# DB stuff
from sqlalchemy.orm import Session
from database import models, SessionLocal, engine, ORM_Base, User
from services import achievements_service, tasks_service, task_scheduler, event_service

# FastAPI stuff
from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import calendar_to_events


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

# Allow frontend (js) to communicate with backend with CORS (Cross-Origin Resource Sharing)
# Middleware is a function that is passed through every request before it's passed through a path operation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")  #can't run when using backend/static so I have changed it to static.
templates = Jinja2Templates(directory="templates")

ORM_Base.metadata.create_all(bind=engine)  # Create tables
global_db = SessionLocal()

user = global_db.query(User).filter(User.username == "joe").all()

if not user:
    global_db.add(models.User(username="joe", hashedPassword="x", streakDays=0, currentPoints=0, stressLevel=0))
    global_db.commit()

# This creates new user db session each request
# A global db var introduces issues with multiple users accessing same db session
def yield_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/", name="home")
def home_page(request: Request, db: Session = Depends(yield_db)):
    tasks = tasks_service.get_user_task_obj("joe", db)
    
    return templates.TemplateResponse("home.html", {"request": request, "user_tasks": tasks})


@app.post("/add_task", response_class=HTMLResponse)
def add(request: Request, title: str = Form(...), description: str = Form(...),duration: int = Form(...),priority: int = Form(...), deadline: datetime = Form(...), db: Session = Depends(yield_db)):
    new_task = models.Task(title=title, description=description, duration=duration, priority=priority, deadline=deadline, username="joe")
    db.add(new_task)
    db.commit()
    
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.delete("/delete_task/{taskID}", response_class=HTMLResponse)
def delete_task(request: Request, taskID: int, db: Session = Depends(yield_db)):
    response = tasks_service.delete_task(taskID, db)
    return JSONResponse(status_code = 200, content = response)


@app.put("/complete_task/{taskID}", response_class=JSONResponse)
def complete_task(request: Request, taskID: int, db: Session = Depends(yield_db)):
    response = tasks_service.set_task_complete(taskID, db)
    return JSONResponse(status_code = 200, content = response)


@app.put("/incomplete_task/{taskID}", response_class=JSONResponse)
def incomplete_task(request: Request, taskID: int, db: Session = Depends(yield_db)):
    response = tasks_service.set_task_incomplete(taskID, db)
    return JSONResponse(status_code = 200, content = response)


@app.put("/breakdown_task/{taskID}", response_class=JSONResponse)
def breakdown_task(request: Request, taskID: int, db: Session = Depends(yield_db)):
    response = task_scheduler.break_down_add_events("joe", taskID, db)
    return JSONResponse(status_code = 200, content = response)


@app.get("/get_events_from_task/{taskID}", response_class=JSONResponse)
def get_events_from_task(request: Request, taskID: int, db: Session = Depends(yield_db)):
    response = event_service.get_events_from_task(taskID, db)
    return JSONResponse(status_code = 200, content = response)
    
@app.post("/add_calendar/", response_class=JSONResponse)
def add_calendar(request: Request, data:dict, db: Session = Depends(yield_db)):
    #Add check function what events were created by the same link.
    #this will delete all tasks linked to this link and re-sync


    url = data.get("ics_url")
    if not url:
        return {"error" : "No ics URL provided"}

    new_events = calendar_to_events.get_event(url)
    for i in new_events:
        new_event = models.Standalone_Event(start = i[1], end = i[2], standaloneEventName = i[0], standaloneEventDescription = i[3], username = "joe")
        db.add(new_event)
    db.commit()

    return JSONResponse(status_code=200, content="complete")
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, access_log=True, log_level="debug")