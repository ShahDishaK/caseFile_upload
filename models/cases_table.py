from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum,Boolean
from datetime import datetime
from config.db_config import Base
from datetime import datetime
from enum import Enum


class CaseStatus(str, Enum):
    closed = "closed"
    open = "open"


class Cases(Base):
    __tablename__   ="cases"

    id = Column(Integer, primary_key=True, index=True)
    caseNumber = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    type=Column(String(40),nullable=False)
    description = Column(String(255), nullable=False)
    caseStage=Column(String(50), nullable=False)
    caseCity=Column(String(50), nullable=False)
    status=Column(SQLEnum(CaseStatus), nullable=False)   
    caseClosedDate=Column(DateTime, nullable=True,default=None)
    clientId=Column(Integer, ForeignKey('clients.id'), nullable=True)
    lawyerId=Column(Integer, ForeignKey('lawyers.id'), nullable=True)
    isDeleted=Column(Integer, default=0)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
