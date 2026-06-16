import api from "../lib/axios";
import { AnomalyResponse } from "../types/metric";

export interface MetricReading {
    timestamp:string;
    value:number;
    service:string;
}

export async function fetchAnomalies(metricName:string):Promise<AnomalyResponse> {
    const res = await api.get<AnomalyResponse>(`/metrics/anomalies/${metricName}`);
    if (!res.data || !Array.isArray(res.data.anomalies)) {
    return {
      metric_name: metricName,
      total_readings: 0,
      anomalies_found: 0,
      anomalies: []
    };
  }
    return res.data
}

export async function fetchMetricReadings(metricName:string):Promise<MetricReading[]> {
    const res = await api.get<MetricReading[]>(`/metrics/${metricName}`);
    if(!Array.isArray(res.data)) {
        return []
    }
    return res.data;

    
}