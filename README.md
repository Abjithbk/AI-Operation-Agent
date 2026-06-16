# 🤖 AI Ops Agent

An AI-powered operational intelligence platform that automatically monitors your production applications, detects anomalies, and explains what went wrong — in plain English.

## 🚀 Features

- **Log Grouping** — NLP clustering groups thousands of similar logs into clean incident cards
- **Anomaly Detection** — Isolation Forest detects CPU, memory, and response time spikes
- **Correlation Engine** — Links metric anomalies to related error logs automatically
- **AI Summarization** — Groq LLM explains root causes in plain English
- **Chat with Logs** — Ask questions about your logs in natural language
- **Slack Alerts** — Auto-notifies team on CRITICAL/HIGH incidents
- **Async Processing** — Redis/Celery queue handles heavy AI tasks in background
- **API Key Auth** — Secure log ingestion with API keys
- **User Auth** — Supabase authentication for dashboard access

## 🛠️ Tech Stack

**Backend**
- FastAPI (Python)
- PostgreSQL (Supabase)
- SQLAlchemy
- Celery + Redis (Upstash)
- LangChain + Groq LLM
- Sentence Transformers (NLP)
- Scikit-learn (Isolation Forest)

**Frontend**
- Next.js 16 (TypeScript)
- Tailwind CSS
- Recharts
- Supabase Auth

**Docs**
- Docusaurus

## 📁 Project Structure
ai-ops-agent/

├── backend/          # FastAPI backend

│   ├── routes/       # API endpoints

│   ├── services/     # Business logic

│   ├── schemas/      # Pydantic models

│   ├── dependencies/ # Auth middleware

│   └── tasks.py      # Celery tasks

├── frontend/         # Next.js dashboard

│   └── app/

│       ├── components/

│       ├── services/

│       ├── types/

│       └── lib/

└── ai-ops-docs/             # Docusaurus documentation

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Supabase account
- Upstash Redis account
- Groq API key

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install pip-tools
pip-compile requirements.in
pip-sync requirements.txt
```

Create `.env` file:

DATABASE_URL=your_supabase_connection_string
GROQ_API_KEY=your_groq_api_key
REDIS_URL=your_upstash_redis_url
SLACK_WEBHOOK_URL=your_slack_webhook_url

Run backend:
```bash
uvicorn main:app --reload
```

Run Celery worker:
```bash
celery -A celery_app worker --loglevel=info --pool=solo
```

### Frontend Setup

```bash
cd frontend
npm install
```

Create `.env.local`:

NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

Run frontend:
```bash
npm run dev
```

### Docs Setup

```bash
cd docs
npm install
npx docusaurus start --port 3001
```

## 🔑 API Usage

Send logs from your production app:

```python
import requests

requests.post(
    "http://localhost:8000/api/logs",
    headers={"X-API-Key": "your_api_key"},
    json={
        "level": "ERROR",
        "service": "payment-service",
        "message": "Database connection failed"
    }
)
```

## 📊 Dashboard

| Page | Description |
|------|-------------|
| `/` | Incidents dashboard with AI-grouped logs |
| `/metrics` | CPU, memory, response time charts |
| `/chat` | Ask questions about your logs |
| `/settings/api-keys` | Generate and manage API keys |

## 🗺️ Roadmap

- [ ] Python SDK (pip installable)
- [ ] Deploy to cloud
- [ ] Docusaurus full content
- [ ] OpenTelemetry integration
- [ ] Elasticsearch support
- [ ] Multi-tenancy

## 📄 License

MIT License