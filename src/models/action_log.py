from src.models.base import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text
from sqlalchemy.sql import func


class ActionLog(Base):
    __tablename__ = 'action_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    timestamp = Column(DateTime, default=func.now())

    action = Column(String(300))
    body = Column(Text)





