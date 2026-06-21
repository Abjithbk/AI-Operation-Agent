from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime
from models import Log, Metric, ApiKey,Profile
from schemas.log import LogResponse, LogCreate
from dependencies.auth import get_current_user_id, require_api_key
from services.mock_generator import generate_mock_logs, generate_mock_metrics
from services.ai_grouping import group_and_summarise
from services.anomaly_detection import detect_anomalies
from services.correlation import correlate_metrics_with_logs
from services.chat_service import chat_with_logs
from services.api_key_service import generate_api_key
from schemas.chat import ChatRequest, ChatResponse
from schemas.slack import SlackWebhookRequest
from tasks import analyse_log_task
from services.slack_notifier import send_slack_alert
from schemas.slack import SlackAlertRequest
from websocket_manager import ws_manager

router = APIRouter()

# ==========================================
# LOGS (Ingestion & Dashboard)
# ==========================================

@router.post("/logs", response_model=LogResponse)
def create_log_single(
    log: LogCreate,
    db: Session = Depends(get_db),
    # SDK uses API Key. require_api_key MUST return the user_id tied to that key!
    user_id: str = Depends(require_api_key) 
):
    new_log = Log(
        level=log.level,
        service=log.service,
        message=log.message,
        user_id=user_id  # <-- Multi-tenancy: tie to user
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.post("/logs/generate")
def create_mock_logs(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id) # Dashboard action
):
    logs = generate_mock_logs(1000)
    for log in logs:
        new_log = Log(
            level=log['level'],
            service=log['service'],
            message=log['message'],
            user_id=user_id  # <-- Multi-tenancy
        )
        db.add(new_log)
    db.commit()
    return {"message": "1000 mocks created for your account"}

@router.get("/logs/analyse")
async def get_logs_analysis(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    
    results = group_and_summarise(db, user_id=user_id) 
    for incident in results:
        await ws_manager.broadcast({
            'type':'new_incident',
            'data':incident
        })
    return results


# METRICS

@router.post('/metrics')
def receive_sdk_metric(
    metric_data: dict,
    db: Session = Depends(get_db),
    user_id: str = Depends(require_api_key)
):
    """
    Receive a single metric from the SDK
    Expected format:
    {
        "metric_name": "cpu_usage",
        "value": 45.2,
        "service": "system"
    }
    """
    try:
        new_metric = Metric(
            metric_name=metric_data["metric_name"],
            value=metric_data["value"],
            service=metric_data.get("service", "default"),
            timestamp=datetime.utcnow(),
            user_id=user_id
        )
        
        db.add(new_metric)
        db.commit()
        db.refresh(new_metric)
        
        return {"status": "success", "metric_id": new_metric.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save metric: {str(e)}")
@router.post("/metrics/generate")
def generate_metrics(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    metrics = generate_mock_metrics(200)
    for metric in metrics:
        new_metric = Metric(
            service=metric.service,
            metric_name=metric.metric_name,
            value=metric.value,
            user_id=user_id  
        )
        db.add(new_metric)
    db.commit()
    return {"message": "600 mock metrics generated successfully!"}

@router.get("/metrics/anomalies/{metric_name}")
def get_anomalies(
    metric_name: str, 
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    results = detect_anomalies(db, metric_name, user_id=user_id)
    return results

@router.get("/metrics/{metric_name}")
def get_metric_readings(
    metric_name: str, 
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    metrics = db.query(Metric).filter(
        Metric.metric_name == metric_name,
        Metric.user_id == user_id  
    ).order_by(Metric.timestamp).all()
    
    return [
        {
            "timestamp": m.timestamp,
            "value": m.value,
            "service": m.service
        }
        for m in metrics
    ]


# CORRELATION & CHAT


@router.get("/correlate/{metric_name}")
def correlate(
    metric_name: str, 
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    results = correlate_metrics_with_logs(db, metric_name, user_id=user_id)
    return results

@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
   
    answer = chat_with_logs(db, request.question, user_id=user_id)
    return {"answer": answer}


# API KEYS (Multi-tenant Management)


@router.post('/api-keys')
def create_api_key(
    name: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id) 
):
    api_key = generate_api_key(db, name, user_id=user_id)
    return {
        "id": api_key.id,
        "name": api_key.name,
        "key": api_key.key,
        "message": "Copy this key securely - it won't be shown again."
    }

@router.get('/api-keys')
def get_api_keys(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id) 
):
    keys = db.query(ApiKey).filter(ApiKey.user_id == user_id).all()

    return [
        {
            "id": k.id,
            "name": k.name,
            "created_at": k.created_at,
        }
        for k in keys
    ]


# BACKGROUND TASKS & ALERTS


@router.post('/logs/analyse/async')
def analyse_logs_async(
    user_id: str = Depends(get_current_user_id)
):

    task = analyse_log_task.delay(user_id=user_id)
    return {
        'message': 'Analysis started in background',
        'task_id': task.id
    }

@router.get('/tasks/{task_id}')
def get_task_status(task_id: str):
    from celery_app import celery
    task = celery.AsyncResult(task_id)
    return {
        'task_id': task_id,
        'status': task.status,
        'result': task.result if task.ready() else None
    }

@router.post('/alerts/slack')
def resend_slack_alert(
    request: SlackAlertRequest,
    db:Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    try:
        profile = db.query(Profile).filter(Profile.id == user_id).first()
        # Note: Phase 3 will use the user's specific webhook URL. 
        # For now, we just pass the user_id for future-proofing.
        success = send_slack_alert(
            group=request.group,
            summary=request.summary,
            severity=request.severity,
            suggestion=request.suggestion,
            log_count=request.log_count,
            user_slack_webhook_url=profile.slack_webhook_url if profile else None
        )

        if success:
            return {"message": "Alert sent to Slack Successfully"}
        else:
            return {'message': 'Failed to send alert'}
    except Exception as e:
        return {
            'message':f"Error: {str(e)}"
        }
    

# STATS (Dashboard)


@router.get('/stats')
def get_stats(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    # STRICTLY filter by user_id so User A doesn't see User B's stats
    total_logs = db.query(Log).filter(Log.user_id == user_id).count()
    error_logs = db.query(Log).filter(Log.user_id == user_id, Log.level == 'ERROR').count()
    info_logs = db.query(Log).filter(Log.user_id == user_id, Log.level == 'INFO').count()
    services = db.query(Log.service).filter(Log.user_id == user_id).distinct().count()

    health = round((info_logs / total_logs * 100)) if total_logs > 0 else 100

    return {
        'total_incidents': total_logs,
        'critical_issues': error_logs,
        'active_services': services,
        'system_health': health
    }

@router.post('/slack')
def save_slack_webhook(data: SlackWebhookRequest,db:Session = Depends(get_db),current_user_id = Depends(get_current_user_id)):

    profile = db.query(Profile).filter(Profile.id == current_user_id).first()

    if not profile:
        raise HTTPException(status_code=404,detail='Profile not found')
    profile.slack_webhook_url = data.slack_webhook_url
    db.commit()

    return {
        'message':'Slack webhook URL saved successfully'
    }

@router.get('/slack')
def get_slack_webhook(db:Session = Depends(get_db),current_user_id = Depends(get_current_user_id)):
    profile = db.query(Profile).filter(Profile.id == current_user_id).first()

    if not profile:
        raise HTTPException(status_code=404,detail='Profile not found')
    
    return {
        'slack_webhook_url':profile.slack_webhook_url
    }
