# PROJECT_RULES.md

## Stack Rules
- Backend: Python 3.12, FastAPI, SQLAlchemy, Pydantic
- Frontend: Next.js 16, TypeScript, Tailwind CSS, Geist font
- DB: PostgreSQL via Supabase (pooler URL port 6543 only)
- Queue: Celery + Redis (Upstash, SSL with ssl.CERT_NONE)
- LLM: Groq (llama-3.3-70b-versatile)
- Auth: Supabase Auth via @supabase/ssr (NOT @supabase/supabase-js createClient)

## Coding Standards
- Python: schemas in schemas/, services in services/, routes in routes/
- All Pydantic schemas in separate schema files (never inline in routes)
- Frontend: components in app/components/, services in app/services/, types in app/types/
- Use @/ alias for imports (not relative ../)
- UUID for all primary keys (not integer)
- pip-tools for dependency management (requirements.in → requirements.txt)

## Critical Constraints
- Never use sentence-transformers (too heavy for deployment, pulls torch 800MB)
- Always use Supabase pooler URL (port 6543), never direct (port 5432)
- Supabase anon key only in frontend (never service_role key)
- celerybeat-schedule files must be in .gitignore
- Redis SSL: use ssl.CERT_NONE (Python constant, not string)
- Next.js middleware file is now called proxy.ts (not middleware.ts) in Next.js 16
- Environment variables: NEXT_PUBLIC_ prefix required for browser access

## Git Rules
- Commit format: "type: description" (feat/fix/docs/chore/style/deploy)
- Never commit .env files
- Never commit celerybeat-schedule.bak/dat/dir files