import datetime

import settings
from src.adapters.user import UserAdapter
from src.models.email_token import EmailToken
from src.models.rest import Rest
from src.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from src.services.email import EmailService
from src.utils.exceptions import Conflict, HTTPException
from src.utils.validators import validate_user_body, partial_validate_user_body


class User(Base, UserAdapter, Rest):
    __tablename__ = 'user'
    search_fields = ['email', 'first_name', 'last_name']

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(15))

    admin = Column(Boolean, default=False)
    active = Column(Boolean, default=False)

    password = Column(String(500), nullable=False)
    salt = Column(String(500))

    session = Column(String(1024))
    session_create_time = Column(DateTime)

    @classmethod
    def get_users(cls, context, request):
        query = context.query(cls)
        query = cls.add_search(query, request)
        total = query.count()
        query = query.order_by(cls.id)
        query = cls.add_pagination(query, request)
        results = query.all()
        return cls.to_json(total, results)

    @classmethod
    def create_user(cls, context, body):
        validate_user_body(body)
        if cls.get_user_by_email(context, body.get("email")):
            raise Conflict("This email address is already used", status=409)

        user = User()
        user.to_object(body)
        context.add(user)
        context.commit()

        email_token = EmailToken(user_id=user.id)
        email_token.generate_token()
        context.add(email_token)
        context.commit()

        email_service = EmailService(settings.SENDGRID_API_KEY, settings.EMAIL_ADDRESS)
        email_service.send_confirmation_email(user, email_token.token)

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

    @classmethod
    def get_user_by_session(cls, context, session_id):
        return context.query(cls).filter_by(session=session_id).first()

    @classmethod
    def login(cls, context, body):
        user = cls.get_user_by_email(context, body.get('email'))
        if not user:
            raise HTTPException("The email or the password is incorrect", status=400)

        password, _ = cls.generate_password(body.get('password'), user.salt.encode('utf-8'))
        if password != user.password:
            raise HTTPException("The email or the password is incorrect", status=400)

        session_id = cls.generate_session()
        user.session = session_id
        user.session_create_time = datetime.datetime.now()

        context.commit()
        return session_id

    @classmethod
    def logout(cls, context, session_id):
        user = User.get_user_by_session(context, session_id)
        if not user:
            raise HTTPException("User not found", status=404)

        user.session = None
        context.commit()

    @classmethod
    def activate_user(cls, context, token):
        token = EmailToken.get_email_token(context, token)
        user = cls.get_user_by_id(context, token.user_id)

        if not user:
            raise HTTPException("User not found", status=404)
        if user.active:
            raise HTTPException("This account it's already activated", status=400)

        user.active = True
        context.commit()

    @classmethod
    def resend_email_confirmation(cls, context, user_id):
        user = cls.get_user_by_id(context, user_id)
        if user.active:
            raise HTTPException("This account it's already activated", status=400)

        email_token = context.query(EmailToken).filter_by(user_id=user_id).first()
        email_token.generate_token()
        email_token.create_time = datetime.datetime.now()
        context.commit()

        email_service = EmailService(settings.SENDGRID_API_KEY, settings.EMAIL_ADDRESS)
        email_service.send_confirmation_email(user, email_token.token)








