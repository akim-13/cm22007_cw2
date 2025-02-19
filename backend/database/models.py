from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.dbsetup import ORM_Base


class User(ORM_Base):
    __tablename__ = "User"

    username = Column(String, primary_key=True, index=True, nullable=False)
    
    hashedPassword = Column(String, nullable=False)
    streakDays = Column(Integer, nullable=False)
    currentPoints = Column(Integer, nullable=False)
    stressLevel = Column(Integer, nullable=False)
    
    # User.tasks will give back an array of all the tasks a user (This is done through inner join automatically)
    # user = db.query(User).first()
    # print(user.tasks)
    tasks = relationship("Task", back_populates="user")  # python-side ORM Relationship
    standalone_events = relationship("Standalone_event", back_populates="user")
    achievements = relationship("Achievements_to_User", back_populates="user")
    
    @property
    def events(self):
        [event for task in self.tasks for event in task.events]  # returns all events related to this user    
    


class Task(ORM_Base):
    __tablename__ = "Task"

    taskID = Column(Integer, primary_key=True, index=True, nullable=False)
    
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    deadline = Column(DateTime, nullable=False)
    isCompleted = Column(Boolean, default=False, nullable=False)
    priority = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    
    username = Column(String, ForeignKey("User.username"), nullable=False)
    
    user = relationship("User", back_populates="tasks")
    events = relationship("Task", back_populates="task")
    


class Event(ORM_Base):
    __tablename__ = "Event"
    
    eventID = Column(Integer, primary_key=True, index=True, nullable=False)
    
    taskID = Column(Integer, ForeignKey("Task.taskID"), nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)    
    
    task = relationship("Task", back_populates="events")
    
    @property
    def user(self):
        return self.task.user  # Access the user through the task without using extra joins

    

class Standalone_Event(ORM_Base):
    __tablename__ = "Standalone_Event"
    
    standaloneEventID = Column(Integer, primary_key=True, nullable=False)
    
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    standaloneEventName = Column(String, nullable=False)
    
    username = Column(String, ForeignKey("User.username"), nullable=False)
    
    user = relationship("User", back_populates="standalone_events")
    


class Achievements(ORM_Base):
    __tablename__ = "Achievements"
    
    achievementID = Column(Integer, primary_key=True, index=True, nullable=False)
    
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
    

class Achievements_to_User(ORM_Base):
    __tablename__ = "Achievements_to_User"
    
    username = Column(String, ForeignKey("User.username"), primary_key=True, nullable=False)
    achievementID = Column(Integer, ForeignKey("Achievements.achievementID"), primary_key=True, nullable=False)
    
    user = relationship("User", back_populates="achievements")
