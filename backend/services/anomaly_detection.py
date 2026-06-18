from sqlalchemy.orm import Session
from models import Metric
from sklearn.ensemble import IsolationForest
import numpy as np

def detect_anomalies(db:Session , metric_name:str,user_id:str):
    metrics = db.query(Metric).filter(
        Metric.metric_name == metric_name,
        Metric.user_id == user_id
    ).order_by(Metric.timestamp).all()

    if len(metrics) < 10:
        return {"message": "Not enough data to detect anomalies"}
    
    values = np.array([m.value for m in metrics]).reshape(-1,1)

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    predictions = model.fit_predict(values)

    anomalies = []

    for i,pred in enumerate(predictions):

        if pred == -1:
            anomalies.append({
                "timestamp": metrics[i].timestamp,
                "service": metrics[i].service,
                "metric_name": metric_name,
                "value": metrics[i].value,
                "status": "ANOMALY"
            })
    return {
        "metric_name": metric_name,
        "total_readings": len(metrics),
        "anomalies_found": len(anomalies),
        "anomalies": anomalies
    }