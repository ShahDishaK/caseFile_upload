from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from datetime import datetime
from config.db_config import Base
from datetime import datetime

class Documents(Base):
    __tablename__="documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    documentLink = Column(String(255), nullable=False)
    fileType = Column(String(50), nullable=False)
    caseId=Column(Integer,ForeignKey('cases.id'), nullable=True)
    userId=Column(Integer,ForeignKey('users.id'), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
