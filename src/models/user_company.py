from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint

import settings
from src.models.company import Company
from src.models.user import User
from src.services.email import EmailService
from src.utils.validators import validate_company_assignment
from src.utils.exceptions import Conflict, HTTPException
from src.adapters.user_company import UserCompanyAdapter
from sqlalchemy.exc import IntegrityError

from src.models.base import Base


class UserCompany(Base, UserCompanyAdapter):
    __tablename__ = 'user_company'
    __table_args__ = (PrimaryKeyConstraint('user_id', "company_id"), )

    user_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    @classmethod
    def get_users(cls, context, company_id):
        results = context.query(cls, User).join(User, cls.user_id == User.id).filter(cls.company_id == company_id).all()
        return cls.to_json(results)

    @classmethod
    def add_user(cls, context, company_id, user_id):
        user_company = UserCompany()
        user_company.company_id = company_id
        user_company.user_id = user_id

        try:
            context.add(user_company)
            context.commit()
        except IntegrityError:
            context.rollback()
            raise HTTPException("This user it's already associated with this company", status=400)

        user = User.get_user_by_id(context, user_id)
        company = Company.get_company_by_id(context, company_id)

        email_service = EmailService(api_key=settings.SENDGRID_API_KEY, sender=settings.EMAIL_ADDRESS)
        email_service.send_assignment_email(user, company)

    @classmethod
    def delete_user(cls, context, company_id, user_id):
        result = context.query(cls).filter_by(user_id=user_id, company_id=company_id).first()
        if not result:
            raise HTTPException("The resource you are trying to delete does not exists", status=404)
        context.delete(result)
        context.commit()
