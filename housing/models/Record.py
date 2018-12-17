from housing.models import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
import datetime
import enum


class WebSites(enum.Enum):
    PAP     = 1
    SeLoger = 2


class Record(DeclarativeBase):
    """Sql alchemy model for the metadata"""
    __tablename__ = "records"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    file_name      = Column(String(255), comment="File name on S3", nullable=False)
    web_site       = Column(Enum(WebSites, name='web_site', create_type=False), comment="PAP or SeLoger", nullable=False)
    created_at     = Column(DateTime, default=datetime.datetime.utcnow, comment="Extraction date", nullable=False)
    processed      = Column(Boolean, default=False)
