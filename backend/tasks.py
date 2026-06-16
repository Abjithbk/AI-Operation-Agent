from celery_app import celery
from database import SessionLocal
from services.ai_grouping import group_and_summarise
from services.anomaly_detection import detect_anomalies
from services.slack_notifier import send_slack_alert 
import json
import traceback

@celery.task(name='analyse_logs', bind=True)
def analyse_log_task(self):
    db = SessionLocal()

    try:
        results = group_and_summarise(db)
        for incident in results:
            summary = incident.get('ai_summary',{})
            if isinstance(summary,str):
                summary = json.loads(summary)
            severity = summary.get('severity','LOW')

            if severity in ["CRITICAL", "HIGH"]:
                send_slack_alert(
                    group=summary.get("group", "Unknown"),
                    summary=summary.get("summary", ""),
                    severity=severity,
                    suggestion=summary.get("suggestion", ""),
                    log_count=incident.get("log_count", 0)
                )

        return {
            'status': 'success',
            'incidents': len(results)
        }
    except Exception as e:
        print(f"Task failed: {str(e)}")
        print(traceback.format_exc())
        raise self.retry(exc=e, max_retries=0)
    finally:
        db.close()


@celery.task(name="detect_metric_anomalies", bind=True)
def detect_anomalies_task(self, metric_name: str):
    db = SessionLocal()
    try:
        results = detect_anomalies(db, metric_name)
        return {"status": "success", "anomalies": results["anomalies_found"]}
    except Exception as e:
        print(f"Task failed: {str(e)}")
        print(traceback.format_exc())
        raise self.retry(exc=e, max_retries=0)
    finally:
        db.close()