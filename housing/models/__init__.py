from dotenv import load_dotenv
load_dotenv()
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings.
    Returns sqlalchemy engine instance
    """
    return create_engine(os.getenv("SQL_DB_URI"))


def create_tables(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)
