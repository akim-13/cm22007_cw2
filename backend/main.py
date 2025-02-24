from datetime import datetime
import logging  # To debug -> Can't print, as the file isn't executed normally

# DB stuff
from sqlalchemy.orm import Session
from database import models, SessionLocal, engine, ORM_Base, User
from services import achievements_service, tasks_service

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
    user_tasks = db.query(models.Task).all()
    logger.debug(user_tasks)
    logger.debug(len(user_tasks))
    return templates.TemplateResponse("home.html", {"request": request, "user_tasks": user_tasks})


@app.post("/add_task", response_class=HTMLResponse)
def add(request: Request, title: str = Form(...), description: str = Form(...),duration: int = Form(...),priority: int = Form(...), deadline: datetime = Form(...), db: Session = Depends(yield_db)):
    new_task = models.Task(title=title, description=description, duration=duration, priority=priority, deadline=deadline, username="joe")
    db.add(new_task)
    db.commit()
    
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.delete("/delete_task/{task_id}", response_class=HTMLResponse)
def delete_task(request: Request, task_id: int, db: Session = Depends(yield_db)):
    response = tasks_service.delete_task(task_id, db)
    return JSONResponse(status_code = 200, content = response)


@app.put("/complete_task/{task_id}", response_class=JSONResponse)
def complete_task(request: Request, task_id: int, db: Session = Depends(yield_db)):
    response = tasks_service.set_task_complete(task_id, db)
    return JSONResponse(status_code = 200, content = response)


@app.put("/incomplete_task/{task_id}", response_class=JSONResponse)
def incomplete_task(request: Request, task_id: int, db: Session = Depends(yield_db)):
    response = tasks_service.set_task_incomplete(task_id, db)
    return JSONResponse(status_code = 200, content = response)
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, access_log=True, log_level="debug")