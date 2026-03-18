from sqlalchemy import Column, Integer, String, DateTime, Numeric,ForeignKey, Enum as SQLEnum
from datetime import datetime
from config.db_config import Base
from datetime import datetime
from enum import Enum


class InvoiceStatus(str, Enum):
    pending = "pending"
    paid = "paid"

class CaseStatusHistories(Base):
    __tablename__="caseStatusHistories"

    id = Column(Integer, primary_key=True, index=True)
    totalAmount=Column(Numeric(10,2), nullable=True)
    totalHours=Column(Numeric(10,2), nullable=True)
    status=Column(SQLEnum(InvoiceStatus), nullable=True)
    caseId = Column(Integer, ForeignKey('cases.id'), nullable=False)
    clientId = Column(Integer, ForeignKey('clients.id'), nullable=False)
    lawyerId = Column(Integer, ForeignKey('lawyers.id'), nullable=False)
    companyId = Column(Integer, ForeignKey('companies.id'), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
