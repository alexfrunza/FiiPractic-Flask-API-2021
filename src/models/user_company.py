from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from src.utils.validators import validate_company_assignment
from src.utils.exceptions import Conflict
from src.adapters.user_company import UserCompanyAdapter

from src.models.base import Base


class UserCompany(Base, UserCompanyAdapter):
    __tablename__ = 'user_company'
    __table_args__ = (PrimaryKeyConstraint('user_id', "company_id"), )

    user_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    @classmethod
    def get_company_users(cls, context, company_id):
        results = context.query(cls).filter_by(company_id=company_id).all()
        return cls.to_json(results)

    @classmethod
    def get_company_by_id(cls, context, company_id):
        return context.query(cls).filter_by(id=company_id).first()

    @classmethod
    def add_user_company_entry(cls, context, company_id, user_id):
        if context.query(cls).filter_by(user_id=user_id, company_id=company_id).first():
            raise Conflict("This user it's already assigned to this company.", status=400)
        uc = UserCompany()
        uc.user_id = user_id
        uc.company_id = company_id
        context.add(uc)
        context.commit()

    def assign_to_company(self, context, company_id, body):
        body['company'] = company_id
        validate_company_assignment(body)
        self.add_user_company_entry(context, company_id, body['user_id'])
        context.commit()
