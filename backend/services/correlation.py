from sqlalchemy.orm import Session
from models import Metric,Log
from services.anomaly_detection import detect_anomalies
from datetime import timedelta

def correlate_metrics_with_logs(db:Session,metric_name:str,user_id : str):

    anomaly_result = detect_anomalies(db,metric_name,user_id)

    if "anomalies" not in anomaly_result:
        return {"message": "No anomalies found"}
    
    anomalies = anomaly_result["anomalies"]

    correlated = []

    for anomaly in anomalies:
        anomaly_time = anomaly["timestamp"]

        # Look for error logs within 5 minutes of the anomaly
        time_from = anomaly_time - timedelta(minutes=5)
        time_to = anomaly_time + timedelta(minutes=5)

        related_logs = db.query(Log).filter(
            Log.level == "ERROR",
            Log.user_id == user_id,
            Log.timestamp >= time_from,
            Log.timestamp <= time_to
        ).all()

        if related_logs:
            correlated.append({
                "anomaly_time": anomaly_time,
                "metric_name": metric_name,
                "metric_value": anomaly["value"],
                "severity": "CRITICAL",
                "related_errors": [
                    {
                        "service": log.service,
                        "message": log.message,
                        "timestamp": log.timestamp
                    }
                    for log in related_logs
                ]
            })

    return {
        "metric_name": metric_name,
        "correlated_incidents": len(correlated),
        "incidents": correlated
    }