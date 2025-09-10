from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import Standalone_Event
import backend.tools.calendar_to_events as calendar_to_events
from backend.tools import external_cal_sync
from backend.database.deps import yield_db

router = APIRouter()

@router.post("/", status_code=200)
def add_calendar(request: Request, data: dict, db: Session = Depends(yield_db)):
    url = data.get("ics_url")
    if not url:
        return {"Error": "No ics URL provided"}

    db.query(Standalone_Event).filter(Standalone_Event.eventBy == url).delete()
    db.commit()
    
    new_events = calendar_to_events.get_events_from_external_cal_link(url)
    if "Valid link" in new_events:
        new_events = new_events.get("Valid link")
        for i in new_events:
            new_event = Standalone_Event(
                start=i[1],
                end=i[2],
                standaloneEventName=i[0],
                standaloneEventDescription=i[3],
                eventBy=i[4],
                username="joe",
            )
            db.add(new_event)
        db.commit()
        return {"status": "complete"}
    else:
        raise HTTPException(status_code=400, detail=new_events.get("Error"))

@router.get("/manual_update")
def manual_update(db: Session = Depends(yield_db)):
    repeated_values = (
        db.query(Standalone_Event.eventBy, func.count(Standalone_Event.eventBy).label("num_repeated"))
        .group_by(Standalone_Event.eventBy)
        .having(func.count(Standalone_Event.eventBy) > 1)
        .all()
    )

    for i in enumerate(repeated_values):
        repeated_values[i[0]] = list(i[1])

    for i in repeated_values:
        external_cal_sync.sync_db_with_external_cal(i[0], db)

    return repeated_values
