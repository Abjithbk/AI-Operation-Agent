from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Log
from schemas.log import LogCreate,LogResponse
from typing import List

router = APIRouter()

@router.post("/logs",response_model=LogCreate)

def create_log(log:LogCreate,db:Session = Depends(get_db)):

    new_log = Log(
        level = log.level,
        service = log.service,
        message = log.message
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log

@router.get("logs",response_model=List[LogResponse])
def get_losg(db:Session = Depends(get_db)):

    logs = db.query(Log).all()
    return logs