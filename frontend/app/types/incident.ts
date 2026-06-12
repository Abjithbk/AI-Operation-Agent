export interface BackendIncident {
  cluster_id: number;
  log_count: number;
  ai_summary: {
    group: string;
    summary: string;
    severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
    suggestion: string;
  };
}

export interface Incident extends BackendIncident {
    timestamp:string
}