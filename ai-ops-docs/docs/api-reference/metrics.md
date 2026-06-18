---
sidebar_position: 5
---

# Metrics API

API endpoints for sending and analyzing application metrics.

## Generate Mock Metrics

```http
POST /api/metrics/generate
```

Generates 600 realistic mock metrics (200 readings × 3 metrics) for testing.

**Response:**
```json
{
  "message": "600 mock metrics generated successfully!"
}
```

---

## Get Metric Readings

```http
GET /api/metrics/{metric_name}
```

Returns all readings for a specific metric ordered by timestamp.

**Available metric names:**
- `cpu_usage`
- `memory_usage`
- `response_time`

**Response:**
```json
[
  {
    "timestamp": "2026-06-15T10:00:00",
    "value": 45.67,
    "service": "payment-service"
  },
  {
    "timestamp": "2026-06-15T10:01:00",
    "value": 46.23,
    "service": "auth-service"
  }
]
```

---

## Get Anomalies

```http
GET /api/metrics/anomalies/{metric_name}
```

Returns anomalies detected by Isolation Forest ML algorithm.

**Response:**
```json
{
  "metric_name": "cpu_usage",
  "total_readings": 200,
  "anomalies_found": 10,
  "anomalies": [
    {
      "timestamp": "2026-06-15T10:22:43",
      "service": "checkout-service",
      "metric_name": "cpu_usage",
      "value": 89.34,
      "status": "ANOMALY"
    }
  ]
}
```

---

## Get Correlated Incidents

```http
GET /api/correlate/{metric_name}
```

Returns metric anomalies correlated with related error logs within a ±5 minute window.

**Response:**
```json
{
  "metric_name": "cpu_usage",
  "correlated_incidents": 3,
  "incidents": [
    {
      "anomaly_time": "2026-06-15T10:22:43",
      "metric_name": "cpu_usage",
      "metric_value": 89.34,
      "severity": "CRITICAL",
      "related_errors": [
        {
          "service": "payment-service",
          "message": "Database connection failed: db-prod-1",
          "timestamp": "2026-06-15T10:22:41"
        }
      ]
    }
  ]
}
```

---

## Get Dashboard Stats

```http
GET /api/stats
```

Returns summary statistics for the dashboard stat cards.

**Response:**
```json
{
  "total_incidents": 1000,
  "critical_issues": 103,
  "active_services": 5,
  "system_health": 70
}
```