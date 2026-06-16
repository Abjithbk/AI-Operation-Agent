# PROJECT_INDEX.md

## Root Structure
```
ai-ops-agent/
├── backend/
├── frontend/
└── docs/ (Docusaurus)
```

## Backend Key Files
| File | Purpose |
|---|---|
| main.py | FastAPI app, CORS, router registration |
| database.py | SQLAlchemy engine + SessionLocal + Base |
| models.py | Log, Metric, ApiKey DB models |
| celery_app.py | Celery config + Beat schedule (300s) |
| tasks.py | analyse_logs_task, detect_anomalies_task |
| routes/logs.py | All API endpoints |
| services/ai_grouping.py | Pure LLM log grouping via Groq |
| services/anomaly_detection.py | Isolation Forest anomaly detection |
| services/correlation.py | Time-window metric+log correlation |
| services/chat_service.py | RAG-style log Q&A via Groq |
| services/slack_service.py | Slack webhook alerts |
| services/mock_generator.py | Mock log/metric generation |
| services/api_key_service.py | API key generation + verification |
| schemas/log.py | LogCreate, LogResponse |
| schemas/metric.py | MetricCreate, MetricResponse |
| schemas/chat.py | ChatRequest, ChatResponse |
| schemas/alert.py | SlackAlertRequest |
| dependencies/auth.py | require_api_key dependency |

## Frontend Key Files
| File | Purpose |
|---|---|
| app/page.tsx | Incidents dashboard (home) |
| app/metrics/page.tsx | Metrics charts + anomalies table |
| app/chat/page.tsx | Chat with logs interface |
| app/login/page.tsx | Login page |
| app/signup/page.tsx | Signup page |
| app/settings/api-keys/page.tsx | API key management |
| app/components/Navbar.tsx | Nav with profile dropdown + logout |
| app/components/IncidentCard.tsx | Incident card + Slack alert button |
| app/components/MetricCard.tsx | Recharts line chart card |
| app/components/AnomaliesTable.tsx | Anomalies data table |
| app/components/Filters.tsx | Incident filter sidebar |
| app/components/ChatSidebar.tsx | Chat history sidebar |
| app/components/StatCard.tsx | Dashboard stat cards |
| app/lib/axios.ts | Axios instance with baseURL |
| app/lib/supabase.ts | Supabase createBrowserClient |
| app/services/incidentService.ts | fetchIncidents, resendSlackAlert |
| app/services/metricService.ts | fetchAnomalies, fetchMetricReadings |
| app/services/chatService.ts | sendChatMessage |
| app/types/incident.ts | BackendIncident, Incident interfaces |
| app/types/metric.ts | Anomaly, AnomalyResponse interfaces |
| app/types/chat.ts | ChatMessage interface |
| proxy.ts | Route protection middleware |

## Environment Variables
### Backend (.env)
```
DATABASE_URL=postgresql://postgres.PROJECT_ID:PASSWORD@aws-0-ap-northeast-2.pooler.supabase.com:6543/postgres
GROQ_API_KEY=gsk_...
REDIS_URL=rediss://default:...@....upstash.io:6379
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_SUPABASE_URL=https://PROJECT_ID.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ... (anon key only!)
```