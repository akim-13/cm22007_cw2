from datetime import datetime
from sqlalchemy import Boolean, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .dbsetup import ORM_Base


class User(ORM_Base):
    __tablename__ = "User"

    username: Mapped[str] = mapped_column(String, primary_key=True, index=True, nullable=False)
    hashedPassword: Mapped[str] = mapped_column(String, nullable=False)
    streakDays: Mapped[int] = mapped_column(Integer, nullable=False)
    currentPoints: Mapped[int] = mapped_column(Integer, nullable=False)
    stressLevel: Mapped[int] = mapped_column(Integer, nullable=False)

    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="user", cascade="all, delete"
    )
    standalone_events: Mapped[list["Standalone_Event"]] = relationship(
        "Standalone_Event", back_populates="user", cascade="all, delete"
    )
    achievements: Mapped[list["Achievements_to_User"]] = relationship(
        "Achievements_to_User", back_populates="user", cascade="all, delete"
    )

    @property
    def events(self) -> list["Event"]:
        """Return all events across all tasks for this user."""
        return [event for task in self.tasks for event in task.events]


class Task(ORM_Base):
    __tablename__ = "Task"

    taskID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    isCompleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)

    username: Mapped[str] = mapped_column(ForeignKey("User.username"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="tasks")
    events: Mapped[list["Event"]] = relationship(
        "Event", back_populates="task", cascade="all, delete"
    )


class Event(ORM_Base):
    __tablename__ = "Event"

    eventID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False)
    taskID: Mapped[int] = mapped_column(ForeignKey("Task.taskID"), nullable=False)
    start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    task: Mapped["Task"] = relationship("Task", back_populates="events")

    @property
    def user(self) -> "User":
        """Access the user through the related task."""
        return self.task.user


class Standalone_Event(ORM_Base):
    __tablename__ = "Standalone_Event"

    standaloneEventID: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    standaloneEventName: Mapped[str] = mapped_column(String, nullable=False)
    standaloneEventDescription: Mapped[str | None] = mapped_column(String, nullable=True)
    eventBy: Mapped[str | None] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(ForeignKey("User.username"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="standalone_events")


class Achievements(ORM_Base):
    __tablename__ = "Achievements"

    achievementID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False)
    requiredPoints: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    image_path: Mapped[str | None] = mapped_column(String, nullable=True)


class Achievements_to_User(ORM_Base):
    __tablename__ = "Achievements_to_User"

    username: Mapped[str] = mapped_column(
        ForeignKey("User.username"), primary_key=True, nullable=False
    )
    achievementID: Mapped[int] = mapped_column(
        ForeignKey("Achievements.achievementID"), primary_key=True, nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="achievements")