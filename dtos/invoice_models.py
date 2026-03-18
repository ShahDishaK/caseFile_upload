from typing import Optional
from unicodedata import decimal
from pydantic import BaseModel
from datetime import datetime


class InvoiceModel(BaseModel):
    totalHours :decimal
    totalAmount :decimal 
    clientId:str
    caseId : str
    companyId: str
    status:str
    
class UpdateInvoiceRequest(BaseModel):
    totalHours: Optional[decimal] = None
    totalAmount: Optional[decimal] = None
    clientId: Optional[int] = None
    caseId: Optional[int] = None
    companyId: Optional[int] = None
    status: Optional[str] = None
    lawyerId: Optional[int] = None