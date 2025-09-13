from typing import TypeAlias

from sqlalchemy_to_pydantic import sqlalchemy_to_pydantic

from backend.database.models import (
    Achievements,
    Achievements_to_User,
    Event,
    Standalone_Event,
    Task,
    User,
)

AchievementsSchema: TypeAlias = sqlalchemy_to_pydantic(Achievements)  # type: ignore
AchievementsToUserSchema: TypeAlias = sqlalchemy_to_pydantic(Achievements_to_User)  # type: ignore
TaskSchema: TypeAlias = sqlalchemy_to_pydantic(Task)  # type: ignore
EventSchema: TypeAlias = sqlalchemy_to_pydantic(Event)  # type: ignore
UserSchema: TypeAlias = sqlalchemy_to_pydantic(User)  # type: ignore
StandaloneEventSchema: TypeAlias = sqlalchemy_to_pydantic(Standalone_Event)  # type: ignore
