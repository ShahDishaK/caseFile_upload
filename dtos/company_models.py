from typing import Optional
from pydantic import BaseModel

class CompanyModel(BaseModel):
    name :str
    Address:str
    phoneNumber:str
    email:str

class UpdateCompanyRequest(BaseModel):
    name:Optional[str]=None
    Address:Optional[str]=None
    phoneNumber:Optional[str]=None
    email:Optional[str]=None
    