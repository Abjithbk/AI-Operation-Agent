from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Log,Metric,ApiKey
from schemas.log import LogResponse,LogCreate
from schemas.metric import MetricResponse
from typing import Optional
from services.mock_generator import generate_mock_logs
from services.ai_grouping import group_and_summarise
from services.mock_generator import generate_mock_metrics
from services.anomaly_detection import detect_anomalies
from services.correlation import correlate_metrics_with_logs
from services.chat_service import chat_with_logs
from services.api_key_service import generate_api_key
from dependencies.auth import require_api_key
from schemas.chat import ChatRequest,ChatResponse
from tasks import analyse_log_task,detect_anomalies_task
from services.slack_notifier import send_slack_alert
from schemas.slack import SlackAlertRequest
router = APIRouter()

@router.post("/logs", response_model=LogResponse)
def create_log_single(
    log: LogCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    new_log = Log(
        level=log.level,
        service=log.service,
        message=log.message
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log
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
def get_losg(filter:Optional[str] = 'all',db:Session = Depends(get_db)):
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

@router.post("/chat",response_model=ChatResponse)
def chat(request:ChatRequest,db:Session = Depends(get_db)):
    answer = chat_with_logs(db,request.question)
    return {
        "answer":answer
    }

@router.post('/api-keys')
def create_api_key(name:str,db:Session = Depends(get_db)):
    api_key = generate_api_key(db,name)
    return {
        "id":api_key.id,
        "name":api_key.name,
        "key":api_key.key,
        "message":"Copy this key securely - it won't be shown again."
    }

@router.get('/api-keys')
def get_api_keys(db:Session = Depends(get_db)):
    keys = db.query(ApiKey).all()

    return [
        {
            "id": k.id,
            "name":k.name,
            "created_at":k.created_at,
        }
        for k in keys
    ]

@router.post('/logs/analyse/async')
def analyse_logs_async():
    task = analyse_log_task.delay()
    return {
        'message':'Analysis started in background',
        'task_id':task.id
    }

@router.get('/tasks/{task_id}')
def get_task_status(task_id:str):
    from celery_app import celery
    task = celery.AsyncResult(task_id)
    return {
        'task_id':task_id,
        'status':task.status,
        'result':task.result if task.ready() else None
    }

@router.post('/alerts/slack')
def resend_slack_alert(request:SlackAlertRequest):

    success = send_slack_alert(
        group=request.group,
        summary=request.summary,
        severity=request.severity,
        suggestion=request.suggestion,
        log_count=request.log_count
    )

    if success:
        return {
            "message":"Alert sent to Slack Successfully"
        }
    else:
        return {
            'message':'Failed to send alert'
        }
