from src.adapters.user import UserAdapter
from src.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from src.utils.exceptions import Conflict
from src.utils.validators import validate_user_body, partial_validate_user_body


class User(Base, UserAdapter):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(15))

    admin = Column(Boolean, default=False)
    active = Column(Boolean, default=True)

    password = Column(String(500), nullable=False)
    salt = Column(String(500))

    session = Column(String(1024))
    session_create_time = Column(DateTime)

    @classmethod
    def get_users(cls, context):
        results = context.query(cls).all()
        return cls.to_json(results)

    @classmethod
    def create_user(cls, context, body):
        validate_user_body(body)
        if cls.get_user_by_email(context, body.get("email")):
            raise Conflict("This email address is already used", status=409)

        user = User()
        user.to_object(body)
        context.add(user)
        context.commit()

    @classmethod
    def update_user(cls, context, body, user_id):
        validate_user_body(body)
        user = cls.get_user_by_id(context, user_id)
        if not user:
            return Conflict("The user you are trying to update does not exist", status=404)
        if cls.get_user_by_email(context, body.get("email")):
            raise Conflict("This email address is already used", status=409)
        user.to_object(body)
        context.commit()

    @classmethod
    def partial_update_user(cls, context, body, user_id):
        partial_validate_user_body(body)
        user = cls.get_user_by_id(context, user_id)
        if not user:
            return Conflict("The user you are trying to update does not exist", status=404)
        if cls.get_user_by_email(context, body.get("email")):
            raise Conflict("This email address is already used", status=409)
        user.to_object(body)
        context.commit()

    @classmethod
    def deactivate(cls, context, user_id):
        user = cls.get_user_by_id(context, user_id)
        if not user:
            return Conflict("The user you are trying to delete does not exist", status=404)
        user.active = False
        context.commit()

    @classmethod
    def get_user_by_id(cls, context, user_id):
        return context.query(cls).filter_by(id=user_id).first()

    @classmethod
    def get_user_by_email(cls, context, email):
        return context.query(cls).filter_by(email=email).first()
