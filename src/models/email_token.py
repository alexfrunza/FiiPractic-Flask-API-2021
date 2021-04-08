from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
import hashlib
from numpy import random
import datetime

from src.models.base import Base
from src.utils.exceptions import HTTPException


class EmailToken(Base):
    __tablename__ = 'email_token'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    token = Column(Text)
    create_time = Column(DateTime, default=func.now())

    def generate_token(self):
        self.token = hashlib.sha256(random.bytes(2048)).hexdigest()

    @classmethod
    def get_email_token(cls, context, token):
        result = context.query(cls).filter_by(token=token).first()
        if not result:
            raise HTTPException("Invalid token", status=400)

        if datetime.datetime.now() - result.create_time > datetime.timedelta(minutes=15):
            raise HTTPException("The token has expired", status=400)

        return result
