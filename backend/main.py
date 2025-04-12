from datetime import datetime
from fastapi import HTTPException, Form
from config import default_achievements
import uvicorn

# DB stuff
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import models, SessionLocal, engine, ORM_Base, User
from database.models import Achievements, Standalone_Event
from services import achievements_service, tasks_service, task_scheduler, event_service, user_service, autofill, standalone_event_service


# FastAPI stuff
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Calendar stuff
import calendar_to_events
import repeat_weekly

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    repeated_values = (
    global_db.query(Standalone_Event.eventBy, func.count(Standalone_Event.eventBy).label("num_repeated"))
    .group_by(Standalone_Event.eventBy)
    .having(func.count(Standalone_Event.eventBy) > 1).all()
    )
    
    for i in enumerate(repeated_values):
        repeated_values[i[0]] = list(i[1])

    for i in repeated_values:
        repeat_weekly.update(i[0], global_db)
        
    yield 

    print("Synchronised")

app = FastAPI(lifespan=lifespan)

# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


ORM_Base.metadata.create_all(bind=engine)  
global_db = SessionLocal()

def initialize_achievements():
    """Check if achievements exist and insert them if missing."""
    if global_db.query(Achievements).count() == 0:  
        for data in default_achievements:
            new_achievement = Achievements(**data)
            global_db.add(new_achievement)
        global_db.commit()
    
    else:
        print("Achievements already exist, skipping population.")

# This creates new user db session each request
# A global db var introduces issues with multiple users accessing same db session
def yield_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/get_user_tasks/{username}", response_class=JSONResponse)
def get_user_tasks(request: Request, username: str, db: Session = Depends(yield_db)):
    response = tasks_service.get_user_tasks(username, db)
    return JSONResponse(status_code = 200, content = response)


@app.get("/get_latest_user_task/{username}", response_class=JSONResponse)
def get_latest_user_task(request: Request, username: str, db: Session = Depends(yield_db)):
    response = tasks_service.get_latest_user_task(username, db)
    return JSONResponse(status_code = 200, content = response)


@app.get("/get_latest_standalone_event/{username}", response_class=JSONResponse)
def get_latest_standalone_event(request: Request, username: str, db: Session = Depends(yield_db)):
    response = event_service.get_latest_standalone_event(username, db)
    return JSONResponse(status_code = 200, content = response)

## ---------- TASK RELATED STUFF ----------

@app.post("/add_task", response_class=JSONResponse)
def add_task(request: Request, title: str = Form(...), description: str = Form(...), duration: int = Form(...),priority: int = Form(...), deadline: datetime = Form(...), db: Session = Depends(yield_db)): # pragma: no cover
    if priority not in [0, 1, 2]:
        raise HTTPException(status_code=400, detail="Invalid priority value. Must be 0 (low), 1 (medium), or 2 (high).")
    
    new_task = models.Task(title=title, description=description, duration=duration, priority=priority, deadline=deadline, username="joe")
    db.add(new_task)
    db.commit()
    return  JSONResponse(status_code = 200, content = {"success": True})

@app.post("/edit_task", response_class=JSONResponse)
def edit_task(request: Request, editID: int = Form(...), title: str = Form(...), description: str = Form(...), duration: int = Form(...), priority: int = Form(...), deadline: datetime = Form(...), db: Session = Depends(yield_db)): # pragma: no cover
    response = tasks_service.edit_task(editID, {
        "title": title,
        "description": description,
        "duration": duration,
        "priority": priority,
        "deadline": deadline
    }, db)
    return JSONResponse(status_code = 200, content = response)

@app.delete("/delete_task/{taskID}", response_class=JSONResponse)
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
def breakdown_task(request: Request, taskID: int, db: Session = Depends(yield_db)): # pragma: no cover
    response = task_scheduler.break_down_add_events("joe", taskID, db)
    return JSONResponse(status_code = 200, content = response)



# ---------- EVENT RELATED STUFF ----------

@app.get("/get_events_from_task/{taskID}", response_class=JSONResponse)
def get_events_from_task(request: Request, taskID: int, db: Session = Depends(yield_db)):
    response = event_service.get_events_from_task(taskID, db)
    return JSONResponse(status_code = 200, content = response)

@app.get("/get_events_from_user/{username}", response_class=JSONResponse)
def get_events_from_user(request: Request, username: str, db: Session = Depends(yield_db)):
    response = event_service.get_all_events(username, db)
    print(response)
    
    return JSONResponse(status_code = 200, content = response)

@app.delete("/delete_events_from_task/{taskID}", response_class=JSONResponse)
def delete_events_from_task(request: Request, taskID: int, db: Session = Depends(yield_db)):
    response = event_service.delete_events_from_task(taskID, db)
    return JSONResponse(status_code = 200, content = response)


@app.post("/edit_task_event", response_class=JSONResponse)
def edit_event(request: Request, editID: int = Form(), start: datetime = Form(), end: datetime = Form(), db: Session = Depends(yield_db)):
    response = event_service.edit_event(editID, start, end, db)
    return JSONResponse(status_code = 200, content = response)



# ---------- ACHIEVEMENTS RELATED STUFF ----------

@app.post("/add_standalone_event", response_class=JSONResponse)
def add_standalone_event(request: Request, standaloneEventName: str = Form(), standaloneEventDescription: str = Form(), start: datetime = Form(), end: datetime = Form(), db: Session = Depends(yield_db)): # pragma: no cover
    new_standalone_event = models.Standalone_Event(standaloneEventName=standaloneEventName, standaloneEventDescription=standaloneEventDescription, start=start, end=end, username="joe")
    db.add(new_standalone_event)
    db.commit()
    
    return JSONResponse(status_code = 200, content = {"success": True})


@app.delete("/delete_standalone_event/{standaloneEventID}", response_class=JSONResponse)
def delete_standalone_event(request: Request, standaloneEventID: int, db: Session = Depends(yield_db)):
    response = standalone_event_service.delete_user_standalone_event(standaloneEventID, db)
    return JSONResponse(status_code = 200, content = response)


@app.get("/get_standalone_events/{username}", response_class=JSONResponse)
def get_standalone_events(request: Request, username: str, db: Session = Depends(yield_db)):
    response = standalone_event_service.get_user_standalone_events(username, db)
    return JSONResponse(status_code = 200, content = response)

@app.post("/edit_standalone_event", response_class=JSONResponse)
def edit_standalone_event(request: Request, editID: int = Form(), standaloneEventName: str = Form(), standaloneEventDescription: str = Form(), start: datetime = Form(), end: datetime = Form(), db: Session = Depends(yield_db)): # pragma: no cover
    response = standalone_event_service.edit_standalone_event(editID, standaloneEventName, standaloneEventDescription, start, end, db)
    return JSONResponse(status_code = 200, content = response)

@app.get("/check_achievements")
def check_achievements(db: Session = Depends(yield_db)):  # pragma: no cover
    achievements = db.query(Achievements).all()
    return achievements

@app.get("/get_achievements_from_user/{username}", response_class=JSONResponse)
def get_achievements_from_user(request: Request, username: str, db: Session = Depends(yield_db)):
    response = achievements_service.get_from_user(username, db)
    return JSONResponse(status_code = 200, content = response)



@app.post("/add_calendar/", response_class=JSONResponse)
def add_calendar(request: Request, data:dict, db: Session = Depends(yield_db)):

    url = data.get("ics_url")
    if not url:
        return {"Error" : "No ics URL provided"}

    #Add check function what events were created by the same link.
    #this will delete all tasks linked to this link and re-sync

    cal_events = db.query(Standalone_Event).filter(Standalone_Event.eventBy == url).delete()
    db.commit()
    
    new_events = calendar_to_events.get_event(url)
    
    if "Valid link" in new_events:
        new_events = new_events.get("Valid link")
        for i in new_events:
            new_event = Standalone_Event(start = i[1], end = i[2], standaloneEventName = i[0], standaloneEventDescription = i[3], eventBy = i[4], username = "joe")
            db.add(new_event)
        db.commit()

        return JSONResponse(status_code=200, content="complete")
    else:
        return JSONResponse(status_code=400, content=new_events.get("Error"))

@app.get("/manual_update")
def manual_update(db: Session = Depends(yield_db)):
    repeated_values = (
    db.query(Standalone_Event.eventBy, func.count(Standalone_Event.eventBy).label("num_repeated"))
    .group_by(Standalone_Event.eventBy)
    .having(func.count(Standalone_Event.eventBy) > 1).all()
    )

    for i in enumerate(repeated_values):
        repeated_values[i[0]] = list(i[1])

    for i in repeated_values:
        repeat_weekly.update(i[0], db)
    return JSONResponse(status_code=200, content=repeated_values)


# ---------- USER RELATED STUFF ----------

@app.get("/get_user_points/{username}")
def get_user_points(request: Request, username: str, db: Session = Depends(yield_db)):
    response = user_service.get_user_points(username, db)
    return JSONResponse(status_code = 200, content = response)

@app.get("/autofill/{username}")
def autofill_gen(request: Request, username: str, description: str, db: Session = Depends(yield_db)) -> autofill.Task | autofill.Event:  # pragma: no cover
    details = autofill.gen(description, datetime.now())
    return details

@app.get("/authenticate_user/")
def authenticate_user(request: Request, username: str, password: str, db: Session = Depends(yield_db)):
    response = user_service.authenticate_user(username, password, db)
    return JSONResponse(status_code = 200, content = response)

@app.get("/create_user/")
def create_user(request: Request, username: str, password: str, db: Session = Depends(yield_db)):
    response = user_service.create_user(username, password, db)
    return JSONResponse(status_code = 200, content = response)

   
def run_app(): # pragma: no cover
    initialize_achievements()

    user = global_db.query(User).filter(User.username == "joe").all()
    if not user:
        global_db.add(models.User(username="joe", hashedPassword="x", streakDays=0, currentPoints=0, stressLevel=0))
        global_db.commit()

    return app 
   
 
if __name__ == "__main__": # pragma: no cover
    uvicorn.run("backend.main:run_app", host="127.0.0.1", port=8000, reload=True, factory=True)
