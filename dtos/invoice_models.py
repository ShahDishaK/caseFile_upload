from typing import Optional
from decimal import Decimal
from pydantic import BaseModel

class InvoiceModel(BaseModel):
    totalHours: Decimal
    totalAmount: Decimal 
    clientId: int
    caseId: int
    companyId: int
    status: str
    
class UpdateInvoiceRequest(BaseModel):
    totalHours: Optional[Decimal] = None
    totalAmount: Optional[Decimal] = None
    clientId: Optional[int] = None
    caseId: Optional[int] = None
    companyId: Optional[int] = None
    lawyerId: Optional[int] = None