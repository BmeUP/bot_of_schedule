from sqlalchemy import Column, Integer
from .base import Base

class BotUser(Base):
    __tablename__ = 'bot_user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
