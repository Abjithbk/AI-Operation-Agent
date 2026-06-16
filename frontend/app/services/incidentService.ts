import api from "../lib/axios";
import { BackendIncident } from "../types/incident";

export async function fetchIncidents(): Promise<BackendIncident[]> {

    const response = await api.get<BackendIncident[]>("/logs/analyse");
    console.log(response.data)
    return response.data
    
}

export async function resendSlackAlert(incident:BackendIncident):Promise<void> {

    await api.post('/alerts/slack',{
        group:incident.ai_summary.group,
        summary: incident.ai_summary.summary,
        severity: incident.ai_summary.severity,
        suggestion: incident.ai_summary.suggestion,
        log_count: incident.log_count
    })
    
}