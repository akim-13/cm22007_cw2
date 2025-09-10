from sqlalchemy.orm import Session
from database.models import Achievements, Standalone_Event, User
from config import default_achievements
from backend.tools import external_cal_sync 


def startup(db: Session):
    update_all_external_cals(db)
    initialise_achievements(db)
    seed_joe_user(db)


def get_all_external_cal_sources(db: Session):
    sources = [
        source
        for (source,) in (
            db.query(Standalone_Event.eventBy)
            .filter(Standalone_Event.eventBy.isnot(None))
            .distinct()
            .all()
        )
    ]
    return sources


def update_all_external_cals(db: Session):
    sources = get_all_external_cal_sources(db)
    for source in sources:
        external_cal_sync.sync_db_with_external_cal(source, db)


def initialise_achievements(db: Session):
    """Check if achievements exist and insert them if missing."""
    if db.query(Achievements).count() == 0:
        for data in default_achievements:
            db.add(Achievements(**data))
        db.commit()
    else:
        print("Achievements already exist, skipping population.")


def seed_joe_user(db: Session):
    user = db.query(User).filter(User.username == "joe").first()
    if not user:
        db.add(User(username="joe", hashedPassword="x", streakDays=0, currentPoints=0, stressLevel=0))
        db.commit()
