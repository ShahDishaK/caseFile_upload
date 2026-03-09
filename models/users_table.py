from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from enum import Enum
from datetime import datetime
from config.db_config import Base
from datetime import datetime, timezone
# from enum import Enum

class UserRole(str, Enum):
    LAWYER = "lawyer"
    ADMIN = "admin"
    STAFF = "staff"
    CLIENT = "client"

class TaskStatus(str, Enum):
    TODAY = "today"
    OVERDUE = "overdue"
    COMPLETED = "completed"
   

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name=Column(String(255), nullable=False)
    firstName=Column(String(255))
    lastName=Column(String(255))
    email = Column(String(255), nullable=False)
    phoneNumber=Column(String(15),nullable=True)
    password = Column(String(255), nullable=True)
    role = Column(SQLEnum(UserRole), nullable=True)
    companyId = Column(Integer, ForeignKey('companies.id'),nullable=True)
    isDeleted=Column(Boolean,default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# class Lawyers(Base):
#     __tablename__ = "lawyers"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     specialization = Column(String(255), nullable=False)
#     caseId = Column(Integer, ForeignKey('cases.id'), nullable=True)
#     clientId = Column(Integer, ForeignKey('clients.id'), nullable=True)
#     sessionId =Column(Integer, ForeignKey('courtSessions.id'), nullable=True)
#     taskId = Column(Integer, ForeignKey('tasks.id'), nullable=True)
#     invoiceId=Column(Integer, ForeignKey('invoices.id'), nullable=True)
#     createdAt = Column(DateTime, default=datetime.utcnow)
#     updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    lawyerId= Column(Integer,ForeignKey('lawyers.id'), nullable=True)
    documentId = Column(Integer, ForeignKey('documents.id'), nullable=True)
    taskId= Column(Integer,ForeignKey('tasks.id'),nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Clients(Base):
    __tablename__="clients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    caseId = Column(Integer, ForeignKey('cases.id'), nullable=True)
    documentId = Column(Integer, ForeignKey('documents.id'), nullable=True)
    invoiceId = Column(Integer, ForeignKey('invoices.id'), nullable=True)
    sessionId = Column(Integer, ForeignKey('courtSessions.id'), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Companies(Base):
    __tablename__="companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    Address = Column(String(255), nullable=False)
    phoneNumber=Column(String(15), nullable=False)
    email=Column(String(30),nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Tasks(Base):
    __tablename__="tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    caseId=Column(Integer,ForeignKey('cases.id'), nullable=True)
    assignedTo=Column(Integer,ForeignKey('users.id'), nullable=True)
    status=Column(SQLEnum(TaskStatus), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# class Cases(Base):
#     __tablename__   ="cases"

#     id = Column(Integer, primary_key=True, index=True)
#     caseNumber = Column(Integer, nullable=False)
#     title = Column(String(255), nullable=False)
#     type=Column(String(40),nullable=False)
#     description = Column(String(255), nullable=False)
#     staffId=Column(Integer,ForeignKey('staff.id'), nullable=True)
#     status=Column(String(50), nullable=False)   
#     createdAt = Column(DateTime, default=datetime.utcnow)
#     updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CourtSessions(Base):
    __tablename__="courtSessions"

    id = Column(Integer, primary_key=True, index=True)
    sessionDate=Column(DateTime, nullable=False)
    courtName=Column(String(255), nullable=False)
    caseId=Column(Integer,ForeignKey('cases.id'), nullable=False)
    lawyerId=Column(Integer,ForeignKey('lawyers.id'), nullable=True)
    clientId=Column(Integer,ForeignKey('clients.id'), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Documents(Base):
    __tablename__="documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    documentLink = Column(String(255), nullable=False)
    fileType = Column(String(50), nullable=False)
    caseId=Column(Integer,ForeignKey('cases.id'), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Invoices(Base):
    __tablename__="invoices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    clientId=Column(Integer,ForeignKey('clients.id'), nullable=False)
    lawyerId=Column(Integer,ForeignKey('lawyers.id'), nullable=False)
    caseId=Column(Integer,ForeignKey('cases.id'), nullable=True)
    invoiceLink = Column(String(255), nullable=False)
    caseId=Column(Integer,ForeignKey('cases.id'), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Payments(Base):
    __tablename__="payments"

    id = Column(Integer, primary_key=True, index=True)
    caseId=Column(Integer, ForeignKey('cases.id'), nullable=False)
    clientId=Column(Integer, ForeignKey('clients.id'), nullable=False)
    lawyerId=Column(Integer, ForeignKey('lawyers.id'), nullable=False)
    totalAmount = Column(Integer, nullable=False)
    paidAmount = Column(Integer, nullable=False)
    paymentDate = Column(DateTime, default=datetime.utcnow)
    paymentMethod=Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    invoiceId = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# # Importing libraries
# from sqlalchemy import Table, Column
# from sqlalchemy.sql.sqltypes import DateTime, Integer, Text, Boolean
# from config.db_config import meta

# # Initializing
# users_table = Table(
#     "users",
#     meta,
#     Column("id", Integer, primary_key=True),
#     Column("email", Text),
#     Column("password", Text),
#     Column("role", Text),
#     Column("created_at", DateTime),
#     Column("updated_at", DateTime),
#     extend_existing=True
# )


