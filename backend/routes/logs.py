from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Log
from schemas.log import LogResponse
from typing import List
from services.mock_generator import generate_mock_logs
router = APIRouter()

@router.post("/logs/generate")

def create_log(db:Session = Depends(get_db)):
    logs = generate_mock_logs(1000)

    for log in logs:
        new_log = Log(
        level = log['level'],
        service = log['service'],
        message = log['message']
    )
        db.add(new_log)

    db.commit()
    return {
        "message":"1000 mocks created"
    }

@router.get("/logs",response_model=List[LogResponse])
def get_losg(db:Session = Depends(get_db)):

    logs = db.query(Log).all()
    return logs