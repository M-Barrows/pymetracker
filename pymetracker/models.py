from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "task"
    task_id = Column(Integer, primary_key=True)
    client = Column(String)
    project = Column(String)
    description = Column(String)
    timers = relationship("Timer", backref=backref("task"))

class Timer(Base):
    __tablename__ = "timer"
    timer_id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task.task_id"))
    start = Column(DateTime)
    end = Column(DateTime)
