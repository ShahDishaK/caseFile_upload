from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from datetime import datetime
from config.db_config import Base
from datetime import datetime


class Lawyers(Base):
    __tablename__ = "lawyers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    specialization = Column(String(255), nullable=False)
    caseId = Column(Integer, ForeignKey('cases.id'), nullable=True)
    clientId = Column(Integer, ForeignKey('clients.id'), nullable=True)
    sessionId =Column(Integer, ForeignKey('courtSessions.id'), nullable=True)
    taskId = Column(Integer, ForeignKey('tasks.id'), nullable=True)
    invoiceId=Column(Integer, ForeignKey('invoices.id'), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
