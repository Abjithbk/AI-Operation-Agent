---
sidebar_position: 4
---

# Logs API

API endpoints for sending and analyzing application logs.

## Send a Log

```http
POST /api/logs
```

Send a single log entry from your production app.

**Headers:**

X-API-Key: your_api_key_here

Content-Type: application/json

**Request Body:**
```json
{
  "level": "ERROR",
  "service": "payment-service",
  "message": "Database connection failed: db-prod-1"
}
```

**Fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| level | string | ✅ | INFO, WARNING, ERROR |
| service | string | ✅ | Name of your service |
| message | string | ✅ | The log message |

**Response:**
```json
{
  "id": "a3f8c2d1-9b4e-4f2a-b5c6",
  "level": "ERROR",
  "service": "payment-service",
  "message": "Database connection failed: db-prod-1",
  "timestamp": "2026-06-15T10:32:01"
}
```

---

## Analyse Logs (Async)

```http
POST /api/logs/analyse/async
```

Triggers AI analysis in background. Returns task ID immediately.

**Response:**
```json
{
  "message": "Analysis started in background!",
  "task_id": "8c43d52f-11aa-4921-a9b1"
}
```

---

## Get Analysis Results

```http
GET /api/logs/analyse
```

Returns AI-grouped incident cards from latest analysis.

**Response:**
```json
[
  {
    "cluster_id": 0,
    "log_count": 312,
    "ai_summary": {
      "group": "Database Connection Failure",
      "summary": "Production database db-prod-1 is unreachable",
      "severity": "CRITICAL",
      "suggestion": "Check db-prod-1 connectivity and restart if needed"
    }
  }
]
```

---

## Check Task Status

```http
GET /api/tasks/{task_id}
```

Check status of a background analysis task.

**Response:**
```json
{
  "task_id": "8c43d52f-11aa-4921-a9b1",
  "status": "SUCCESS",
  "result": {
    "status": "success",
    "incidents": 4
  }
}
```

**Task statuses:**

| Status | Meaning |
|---|---|
| PENDING | Task queued, waiting |
| STARTED | Worker processing |
| SUCCESS | Completed successfully |
| FAILURE | Something went wrong |

---

## Generate Mock Logs

```http
POST /api/logs/generate
```

Generates 1000 realistic mock logs for testing. No API key required.

**Response:**
```json
{
  "message": "1000 mocks created"
}
```

:::info
This endpoint is for demo/testing only. In V2 with the Python SDK, real logs will flow in automatically from your production app.
:::