from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class ScheduleTable(Base):
    __tablename__ = 'schedule_table'

    id = Column(Integer, primary_key=True)
    fullname = Column(String)
    position = Column(String)
    usr_tm = relationship("UserTime", back_populates="parent")
