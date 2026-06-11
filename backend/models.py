from sqlalchemy import Column,Float,String,DateTime
from sqlalchemy.sql import func
from database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())
class Log(Base):
    __tablename__ = "logs"

    id = Column(String,primary_key=True,index=True,default=generate_uuid)
    timestamp = Column(DateTime,default=func.now())
    level = Column(String)
    service = Column(String)
    message = Column(String)

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(String,primary_key=True,default=generate_uuid)
    timestamp = Column(DateTime,default=func.now())
    service = Column(String)
    metric_name = Column(String)
    value = Column(Float)