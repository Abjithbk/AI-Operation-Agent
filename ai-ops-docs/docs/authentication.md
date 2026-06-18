---
sidebar_position: 3
---

# Authentication

AI Ops Agent uses **Supabase Auth** for user authentication and **API Keys** for secure log ingestion.

## User Authentication

### Sign Up
Visit the dashboard and click **Sign Up**:
- Enter your email and password
- You'll be redirected to the dashboard automatically
- No email confirmation required in V1

### Login
Visit `/login` and enter your credentials. Your session stays active for 60 days automatically.

### Logout
Click your profile icon in the top right navbar → click **Logout**.

---

## API Keys (Coming in V2)

:::caution Coming in V2
API key management with full multi-tenancy is coming in V2. Each user will have isolated data and secure API keys for their production apps.
:::

In V2, API keys will work like this:

**Generate a key:**
1. Go to **Settings → API Keys**
2. Enter a name for your key (e.g. "My E-commerce App")
3. Click **Generate**
4. Copy the key immediately — it won't be shown again

**Use the key in your app:**
```python
requests.post(
    "https://your-agent.com/api/logs",
    headers={"X-API-Key": "aiops_your_key_here"},
    json={
        "level": "ERROR",
        "service": "payment-service",
        "message": "Database connection failed"
    }
)
```

**Security rules:**
- Never commit your API key to GitHub
- Store it in your `.env` file
- Each key belongs to one user account
- Keys can be revoked anytime from the settings page