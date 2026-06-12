from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Log,Metric
from schemas.log import LogResponse
from schemas.metric import MetricResponse
from typing import List
from services.mock_generator import generate_mock_logs
from services.ai_grouping import group_and_summarise
from services.mock_generator import generate_mock_metrics
from services.anomaly_detection import detect_anomalies
from services.correlation import correlate_metrics_with_logs
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

@router.post("/metrics/generate")
def generate_metrics(db: Session = Depends(get_db)):
    metrics = generate_mock_metrics(200)
    for metric in metrics:
        new_metric = Metric(
            service=metric.service,
            metric_name=metric.metric_name,
            value=metric.value
        )
        db.add(new_metric)
    db.commit()
    return {"message": "600 mock metrics generated successfully!"}

@router.get("/metrics/anomalies/{metric_name}")
def get_anomalies(metric_name: str, db: Session = Depends(get_db)):
    results = detect_anomalies(db, metric_name)
    return results



@router.get("/correlate/{metric_name}")
def correlate(metric_name: str, db: Session = Depends(get_db)):
    results = correlate_metrics_with_logs(db, metric_name)
    return results

@router.get("/metrics/{metric_name}")
def get_metric_readings(metric_name: str, db: Session = Depends(get_db)):
    metrics = db.query(Metric).filter(
        Metric.metric_name == metric_name
    ).order_by(Metric.timestamp).all()
    
    return [
        {
            "timestamp": m.timestamp,
            "value": m.value,
            "service": m.service
        }
        for m in metrics
    ]