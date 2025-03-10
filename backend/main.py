from datetime import datetime
import logging  # To debug -> Can't print, as the file isn't executed normally
from fastapi import HTTPException
from config import default_achievements

# DB stuff
from sqlalchemy.orm import Session
from database import models, SessionLocal, engine, ORM_Base, User
from database.models import Achievements
from services import achievements_service, tasks_service, task_scheduler, event_service, autofill, standalone_event_service
# FastAPI stuff
from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

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
    
        

@app.get("/", name="home")
def home_page(request: Request, db: Session = Depends(yield_db)):
    tasks = tasks_service.get_user_task_obj("joe", db)
    
    return templates.TemplateResponse("home.html", {"request": request, "user_tasks": tasks})

@app.get("/get_tasks/{username}", response_class=JSONResponse)
def get_tasks(request: Request, username: str, db: Session = Depends(yield_db)):
    response = tasks_service.get_user_task(username, db)
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

@app.post("/add_task", response_class=HTMLResponse)
def add(request: Request, title: str = Form(...), description: str = Form(...), duration: int = Form(...),priority: int = Form(...), deadline: datetime = Form(...), db: Session = Depends(yield_db)):
    
    if priority not in [0, 1, 2]:
        raise HTTPException(status_code=400, detail="Invalid priority value. Must be 0 (low), 1 (medium), or 2 (high).")
    
    new_task = models.Task(title=title, description=description, duration=duration, priority=priority, deadline=deadline, username="joe")
    db.add(new_task)
    db.commit()
    
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.post("/edit_task", response_class=JSONResponse)
def add(request: Request, taskID: int, task_properties: dict, db: Session = Depends(yield_db)):
    response = tasks_service.edit_task(taskID,task_properties, db)
    return JSONResponse(status_code = 200, content = response)
    
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



# ---------- EVENT RELATED STUFF ----------

@app.get("/get_events_from_task/{taskID}", response_class=JSONResponse)
def get_events_from_task(request: Request, taskID: int, db: Session = Depends(yield_db)):
    response = event_service.get_events_from_task(taskID, db)
    return JSONResponse(status_code = 200, content = response)

@app.put("/edit_event/{eventID}", response_class=JSONResponse)
def complete_task(request: Request, eventID: int, start: datetime, end: datetime, db: Session = Depends(yield_db)):
    response = event_service.edit_event(eventID, start, end, db)
    return JSONResponse(status_code = 200, content = response)



# ---------- ACHIEVEMENTS RELATED STUFF ----------

@app.post("/add_standalone_event", response_class=HTMLResponse)
def add_standalone_event(request: Request, standaloneEventName: str = Form(...), standaloneEventDescription: str = Form(...), start: datetime = Form(...), end: datetime = Form(...), db: Session = Depends(yield_db)):
    new_standalone_event = models.Standalone_Event(standaloneEventName=standaloneEventName, standaloneEventDescription=standaloneEventDescription, start=start, end=end, username="joe")
    db.add(new_standalone_event)
    db.commit()
    
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.delete("/delete_standalone_event/{standaloneEventID}", response_class=HTMLResponse)
def delete_standalone_event(request: Request, standaloneEventID: int, db: Session = Depends(yield_db)):
    response = standalone_event_service.delete_user_standalone_event(standaloneEventID, db)
    return JSONResponse(status_code = 200, content = response)


@app.get("/get_standalone_events/{username}", response_class=JSONResponse)
def get_standalone_events(request: Request, username: str, db: Session = Depends(yield_db)):
    response = standalone_event_service.get_user_standalone_events(username, db)
    return JSONResponse(status_code = 200, content = response)


@app.get("/check_achievements")
def check_achievements(db: Session = Depends(yield_db)):
    achievements = db.query(Achievements).all()
    return achievements

@app.get("/get_achievements_from_user/{username}", response_class=JSONResponse)
def get_achievements_from_user(request: Request, username: str, db: Session = Depends(yield_db)):
    response = achievements_service.get_from_user(username, db)
    return JSONResponse(status_code = 200, content = response)



# ---------- USER RELATED STUFF ----------

@app.get("/get_user_points/{username}")
def get_user_points(request: Request, username: str, db: Session = Depends(yield_db)):
    response = user_service.get_user_points(username, db)
    return JSONResponse(status_code = 200, content = response)

@app.get("/autofill/{username}")
def autofill(request: Request, username: str, description: str, db: Session = Depends(yield_db)) -> autofill.Task:
    details = autofill.gen(description, datetime.now())
    return details

   
   
def run_app():
    import uvicorn
    initialize_achievements()
    user = global_db.query(User).filter(User.username == "joe").all()
    if not user:
        global_db.add(models.User(username="joe", hashedPassword="x", streakDays=0, currentPoints=0, stressLevel=0))
        global_db.commit()

    uvicorn.run(app, access_log=True, log_level="debug")   
   
 
if __name__ == "__main__":
    run_app()
