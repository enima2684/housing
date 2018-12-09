from dotenv import load_dotenv
load_dotenv()
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(os.getenv("SQL_DB_URI"))


def create_deals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

