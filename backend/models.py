from sqlalchemy import Column,Integer,String,DateTime
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