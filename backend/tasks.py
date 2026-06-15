from celery_app import celery
from database import SessionLocal
from services.ai_grouping import group_and_summarise
from services.anomaly_detection import detect_anomalies
import traceback
@celery.task(name='analyse_logs',bind=True)
def analyse_log_task(self):
    db = SessionLocal()

    try:
        results = group_and_summarise(db)
        return {
            'status': 'success',
            'incidents':len(results)
        }
    except Exception as e:
        print(f"Task failed: {str(e)}")
        print(traceback.format_exc())
        raise self.retry(exc=e, max_retries=0)
    finally:
        db.close()

@celery.task(name='detect_metric_anomalies',bind=True)
def detect_anomalies_task(self,metric_name:str):
    db = SessionLocal()

    try:
        results = detect_anomalies(db,metric_name)
        return {
            'status':'success',
            'anomalies':results['anomalies_found']
        }
    except Exception as e:
        print(f"Task failed: {str(e)}")
        print(traceback.format_exc())
        raise self.retry(exc=e, max_retries=0)
    finally:
        db.close()