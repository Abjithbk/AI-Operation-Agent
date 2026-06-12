export interface Anomaly {
    timestamp:string;
    service:string;
    metric_name:string;
    value:number;
    status:string;
}

export interface AnomalyResponse {
  metric_name: string;
  total_readings: number;
  anomalies_found: number;
  anomalies: Anomaly[];
}