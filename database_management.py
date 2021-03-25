import logging
import sqlalchemy

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

database_session = None


def build_sqlite_connection_string(db_file_path):
    return f'sqlite:///{db_file_path}'


def create_dependent_tables(engine):
    from src.models.base import Base
    from src.models.user import User
    from src.models.company import Company
    from src.models.user_company import UserCompany
    Base.metadata.create_all(engine)


def init_database_connection(connection_string):
    global database_session

    if not database_exists(connection_string):
        create_database(connection_string)

    engine = sqlalchemy.create_engine(connection_string)
    database_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    create_dependent_tables(engine)

    logger.info('Successful initiated the database')
    return engine, database_session


def get_database_session():
    return database_session()

# aplicatie de user management
