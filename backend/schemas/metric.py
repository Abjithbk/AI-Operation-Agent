from pydantic import BaseModel
from datetime import datetime

class MetricCreate(BaseModel):
    service: str
    metric_name: str
    value: float

class MetricResponse(BaseModel):
    id: str
    timestamp: datetime
    service: str
    metric_name: str
    value: float

    class Config:
        from_attributes = True
