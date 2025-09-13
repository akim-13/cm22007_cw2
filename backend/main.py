from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.dbsetup import SessionLocal, engine
from backend.database.models import ORM_Base
from backend.routers import achievements, calendars, events, tasks, users
from backend.tools.startup import startup

# TODO:
# - Docstrings enforcement.
# - Logging.


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    ORM_Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        startup(db)

    # ↑ STARTUP CODE ↑
    yield  # App runs.
    # ↓ SHUTDOWN CODE ↓

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


def run_app() -> FastAPI:  # pragma: no cover
    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(achievements.router, prefix="/achievements", tags=["Achievements"])
    app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
    app.include_router(events.router, prefix="/events", tags=["Events"])
    app.include_router(calendars.router, prefix="/calendars", tags=["Calendars"])

    return app


if __name__ == "__main__":  # pragma: no cover
    uvicorn.run("backend.main:run_app", host="127.0.0.1", port=8000, reload=True, factory=True)
