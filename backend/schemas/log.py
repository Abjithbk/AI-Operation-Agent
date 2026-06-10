from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogCreate(BaseModel):
    level:str
    service:str
    message:str

class LogResponse(BaseModel):
    id:str
    timestamp:datetime
    level:str
    service:str
    message:str

    class Config:
        from_attributes = True
