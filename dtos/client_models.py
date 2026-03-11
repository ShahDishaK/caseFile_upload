from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ClientModel(BaseModel):
    user_id :int
    crNumber:int
    vatNumber:int
    vatPercentage:int
    caseId :int
    documentId :int
    