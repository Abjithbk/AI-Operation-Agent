import api from "../lib/axios";
import { AnomalyResponse } from "../types/metric";

export interface MetricReading {
    timestamp:string;
    value:number;
    service:string;
}

export async function fetchAnomalies(metricName:string):Promise<AnomalyResponse> {
    const res = await api.get<AnomalyResponse>(`/metrics/anomalies/${metricName}`);
    return res.data
}

export async function fetchMetricReadings(metricName:string):Promise<MetricReading[]> {
    const res = await api.get<MetricReading[]>(`/metrics/${metricName}`);
    return res.data;

    
}