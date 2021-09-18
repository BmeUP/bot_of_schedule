from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from .base import Base

class UserTime(Base):
    __tablename__ = 'user_time'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('schedule_table.id'))
    parent = relationship("ScheduleTable", back_populates="usr_tm")
    time = Column(String)
    date = Column(String)
