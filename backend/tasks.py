from celery_app import celery
from database import SessionLocal
from services.ai_grouping import group_and_summarise
from services.anomaly_detection import detect_anomalies
from services.slack_notifier import send_slack_alert 
import traceback

@celery.task(name='analyse_logs', bind=True)
def analyse_log_task(self):
    db = SessionLocal()

    try:
        results = group_and_summarise(db)
        incident_count = len(results)
        
        # 👈 NEW: Trigger Slack alert if any incidents were found
        if incident_count > 0:
            send_slack_alert(
                incident_title="Log Anomaly Clustered",
                severity="high",
                summary="AI has detected, grouped, and summarized new application errors.",
                incident_count=incident_count
            )

        return {
            'status': 'success',
            'incidents': incident_count
        }
    except Exception as e:
        print(f"Task failed: {str(e)}")
        print(traceback.format_exc())
        raise self.retry(exc=e, max_retries=3) # 👈 Changed max_retries to 3 so it actually retries on failure
    finally:
        db.close()


@celery.task(name='detect_metric_anomalies', bind=True)
def detect_anomalies_task(self, metric_name: str):
    db = SessionLocal()

    try:
        results = detect_anomalies(db, metric_name)
        anomaly_count = results.get('anomalies_found', 0)
        
        # 👈 NEW: Trigger Slack alert if any metric anomalies were found
        if anomaly_count > 0:
            send_slack_alert(
                incident_title=f"Metric Anomaly: {metric_name.replace('_', ' ').title()}",
                severity="critical",
                summary=f"Statistical anomaly detected in {metric_name} metrics by Isolation Forest.",
                incident_count=anomaly_count
            )

        return {
            'status': 'success',
            'anomalies': anomaly_count
        }
    except Exception as e:
        print(f"Task failed: {str(e)}")
        print(traceback.format_exc())
        raise self.retry(exc=e, max_retries=3) # 👈 Changed max_retries to 3
    finally:
        db.close()