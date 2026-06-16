# ARCHITECTURE.md

## System Overview
AI-powered observability platform. Production apps send logs/metrics → AI analyzes → engineers see insights on dashboard.

## Data Flow
```
Production App
  → POST /api/logs (X-API-Key header required)
  → PostgreSQL (Supabase)
  → Celery Beat (every 5 mins auto-trigger)
  → Groq LLM groups + summarises logs
  → Slack alert if CRITICAL/HIGH
  → Next.js dashboard shows incidents
```

## Services
| Service | Purpose | Tool |
|---|---|---|
| Log ingestion | Receive logs from apps | FastAPI POST /api/logs |
| Log grouping | Group similar errors | Groq LLM (pure LLM, no sentence-transformers) |
| Anomaly detection | Detect metric spikes | Isolation Forest (scikit-learn) |
| Correlation | Link spikes to errors | Time-window matching (±5 mins) |
| Async processing | Background AI tasks | Celery + Upstash Redis |
| Scheduling | Auto-run analysis | Celery Beat (every 300s) |
| Alerts | Notify team | Slack Incoming Webhooks |
| Auth | User login | Supabase Auth |
| API Security | Protect ingestion | API Keys (X-API-Key header) |

## Key Architecture Decisions
- **No sentence-transformers**: Removed to fit Render free tier (512MB). Pure LLM grouping via Groq instead.
- **Supabase pooler**: Direct connection (5432) causes issues. Always use pooler (6543).
- **Cookie-based sessions**: Using @supabase/ssr createBrowserClient for middleware compatibility.
- **Celery Beat**: 3 processes needed (uvicorn + worker + beat).
- **V1 uses mock data**: Real SDK integration planned for V2.

## Deployment Target
- Backend: Render (free tier) — needs runtime.txt (python-3.12.0)
- Frontend: Vercel (free)
- Docs: Vercel (free)
- DB: Supabase (free)
- Redis: Upstash (free)
- Keep-alive: UptimeRobot (prevents Render sleep)