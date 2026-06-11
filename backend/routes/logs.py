from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Log
from schemas.log import LogResponse
from typing import List
from services.mock_generator import generate_mock_logs
from services.ai_grouping import group_and_summarise
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

@router.get("/logs/analyse")
def get_losg(db:Session = Depends(get_db)):

    results = group_and_summarise(db)
    return results