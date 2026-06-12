import { Incident } from "../types/incident";
export const dummyIncidents: Incident[] = [
  {
    cluster_id: 0,
    log_count: 124,
    ai_summary: {
      group: "Database Connection Failure",
      summary:
        "Multiple connection timeouts detected in the auth-service pool. Latency spiked from 12ms to 2500ms over a 30-second window.",
      severity: "CRITICAL",
      suggestion:
        "Increase connection pool size or check network latency on the database cluster.",
    },
    timestamp: "2 mins ago",
  },
  {
    cluster_id: 1,
    log_count: 45,
    ai_summary: {
      group: "High Memory Eviction Rate",
      summary:
        "Cache eviction policy 'volatile-lru' is aggressively dropping keys. Hit rate dropped below 85% for production cluster.",
      severity: "HIGH",
      suggestion:
        "Upscale Redis node type or implement secondary cache layer for non-critical transient data.",
    },
    timestamp: "15 mins ago",
  },
  {
    cluster_id: 2,
    log_count: 12,
    ai_summary: {
      group: "Payment Gateway Timeout",
      summary:
        "Stripe API experiencing repeated timeouts when processing payment requests.",
      severity: "MEDIUM",
      suggestion:
        "Check Stripe API status and consider implementing retry logic with exponential backoff.",
    },
    timestamp: "1 hour ago",
  },
];

export const dummyStats = {
  totalIncidents: 24,
  criticalIssues: 3,
  activeServices: 112,
  systemHealth: 94,
};