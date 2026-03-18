from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from datetime import datetime
from config.db_config import Base
from datetime import datetime

class Clients(Base):
    __tablename__="clients"

    id = Column(Integer, primary_key=True, index=True)
    crNumber=Column(Integer, nullable=True)
    vatNumber=Column(Integer, nullable=True)
    vatPercentage=Column(Integer, nullable=True)
    isBlocked = Column(Integer, default=0)
    isDeleted = Column(Integer, default=0)
    lawyerId = Column(Integer, ForeignKey('documents.id'), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
