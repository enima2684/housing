from housing.models import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, Enum
import datetime
import enum

class WebSites(enum.Enum):
    PAP     = 1
    SeLoger = 2

class Scrap_Metadata(DeclarativeBase):
    """Sql alchemy model for the metadata"""
    __tablename__ = "scrap_metadata"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    file_name      = Column(String(255), comment="File name on S3", nullable=False)
    web_site       = Column(Enum(WebSites), comment="PAP or SeLoger", nullable=False)
    created_at     = Column(DateTime, default=datetime.datetime.utcnow, comment="Extraction date", nullable=False)
    hash_doc       = Column(String(256))

