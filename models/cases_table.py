from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from datetime import datetime
from config.db_config import Base
from datetime import datetime

class Cases(Base):
    __tablename__   ="cases"

    id = Column(Integer, primary_key=True, index=True)
    caseNumber = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    type=Column(String(40),nullable=False)
    description = Column(String(255), nullable=False)
    caseStage=Column(String(50), nullable=False)
    caseCity=Column(String(50), nullable=False)
    status=Column(String(50), nullable=False)   
    caseClosedDate=Column(DateTime, nullable=True,default=None)
    clientId=Column(Integer, ForeignKey('clients.id'), nullable=True)
    isDeleted=Column(Boolean, default=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
