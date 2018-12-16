from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
import datetime

from housing.models.Record import WebSites
from housing.models import DeclarativeBase

class Ad(DeclarativeBase):
    """
    SqlAlchemy model for an Ad
    """
    __tablename__ = "ads"

    id          = Column(String(128), primary_key=True, nullable=False)
    source_file = Column(String(255), comment="File name on S3 from which it was extracted", nullable=False)
    web_site    = Column(Enum(WebSites, create_type=False), comment="PAP or SeLoger", nullable=False)
    created_at  = Column(DateTime, default=datetime.datetime.utcnow, comment="Parsing date", nullable=False)

    price       = Column(Integer, nullable=False, comment="Price of the asset")
    area        = Column(Integer, nullable=False, comment="Area in m2 of the asset")
    postal_code = Column(String(16), nullable=False, comment="Postal code of the location of the asset")
    url         = Column(String(512), nullable=False, comment="url for the ad")

    def __repr__(self):
        return f'<{self.id}> '