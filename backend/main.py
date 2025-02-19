from datetime import datetime
import logging  # To debug -> Can't print, as the file isn't executed normally

# DB stuff
from sqlalchemy.orm import Session
from database import models, SessionLocal, engine, ORM_Base

# FastAPI stuff
from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
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
SessionLocal().add(models.User(username="joe", hashedPassword="x", streakDays=0, currentPoints=0, stressLevel=0))

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


# title is expected as a form parameter (purpose of ellipses ...)
@app.post("/add", response_class=HTMLResponse)
def add(request: Request, 
        title: str = Form(...), 
        description: str = Form(...),
        duration: int = Form(...),
        priority: int = Form(...), 
        deadline: datetime = Form(...), 
        db: Session = Depends(yield_db)):
    
    new_task = models.Task(
        title=title, 
        description=description, 
        duration=duration, 
        priority=priority, 
        deadline=deadline, 
        username="joe")
    
    db.add(new_task)
    db.commit()
    
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.delete("/delete/{task_id}", response_class=HTMLResponse)
def delete(request: Request, task_id: int, db: Session = Depends(yield_db)):
    task = db.query(models.Task).filter(models.Task.taskID == task_id).first()
    db.delete(task)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@app.put("/update/{task_id}", response_class=HTMLResponse)
def update(request: Request, task_id: int, db: Session = Depends(yield_db)):
    task = db.query(models.Task).filter(models.Task.taskID == task_id).first()
    task.isCompleted = not task.isCompleted
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)