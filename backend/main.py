from datetime import datetime
import logging  # To debug -> Can't print, as the file isn't executed normally

# DB stuff
from sqlalchemy.orm import Session
from database import models, SessionLocal, engine, ORM_Base, User
from database.models import Achievements
from services import achievements_service, tasks_service, task_scheduler, event_service

# FastAPI stuff
from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

ORM_Base.metadata.create_all(bind=engine)  # Create tables
global_db = SessionLocal()


# List of default achievements
default_achievements = [
    {
        "title": "Just Getting Started",
        "requiredPoints": 10,
        "description": "Completed the first 10 minutes of focused work.",
        "image_path": "/images/achievements/start.png",

    },
    {
        "title": "Half-Hour Hero",
        "requiredPoints": 30,
        "description": "Spent 30 minutes on a task. You're getting into the flow!",
        "image_path": "/images/achievements/half_hour.png"
    },
    {
        "title": "One-Hour Warrior",
        "requiredPoints": 60,
        "description": "Dedicated an hour to your task. Strong focus!",
        "image_path": "/images/achievements/one_hour.png"
    },
    {
        "title": "Time Master",
        "requiredPoints": 120,
        "description": "Worked for 2 hours in total. Your discipline is growing.",
        "image_path": "/images/achievements/time_master.png"
    },
    {
        "title": "Deep Focus Apprentice",
        "requiredPoints": 300,
        "description": "Spent 5 hours focused. Impressive commitment!",
        "image_path": "/images/achievements/deep_focus.png"
    },
    {
        "title": "Productivity Pro",
        "requiredPoints": 600,
        "description": "10 hours of total focus. You're a work machine!",
        "image_path": "/images/achievements/productivity_pro.png"
    },
    {
        "title": "Task Titan",
        "requiredPoints": 1200,
        "description": "20 hours spent on tasks. An unstoppable force!",
        "image_path": "/images/achievements/task_titan.png"
    },
    {
        "title": "Legend of Focus",
        "requiredPoints": 2400,
        "description": "40 hours of deep work. You’re in the hall of fame now!",
        "image_path": "/images/achievements/legend_of_focus.png"
    },
    {
        "title": "Master of Time",
        "requiredPoints": 5000,
        "description": "83+ hours in tasks. True dedication!",
        "image_path": "/images/achievements/master_of_time.png"
    },
    {
        "title": "God of Productivity",
        "requiredPoints": 10000,
        "description": "166+ hours. Beyond human limits!",
        "image_path": "/images/achievements/god_of_productivity.png"
    }
]


def initialize_achievements():
    """Check if achievements exist and insert them if missing."""
    if global_db.query(Achievements).count() == 0:  # Only add if table is empty
        for data in default_achievements:
            new_achievement = Achievements(**data)
            global_db.add(new_achievement)
        global_db.commit()
    
    else:
        print("Achievements already exist, skipping population.")
#Call it once to populate the achievements table
initialize_achievements()

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


@app.get("/check_achievements")
def check_achievements(db: Session = Depends(yield_db)):
    achievements = db.query(Achievements).all()
    return achievements


@app.get("/get_achievements_from_user/{username}", response_class=JSONResponse)
def get_achievements_from_user(request: Request, username: str, db: Session = Depends(yield_db)):
    response = achievements_service.get_from_user(username, db)
    return JSONResponse(status_code = 200, content = response)

@app.get("/get_user_points/{username}")
def get_user_points(username: str):
    return {"username": username, "points": 120}

# Isaac: For now, ive hard coded the amoount of points each user has but can someone create 
# a column for the points


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, access_log=True, log_level="debug")