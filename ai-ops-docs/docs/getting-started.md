---
sidebar_position: 2
---

# Getting Started

Get up and running with AI Ops Agent in 5 minutes.

## Step 1 — Create an Account

Visit the [AI Ops Agent Dashboard](https://your-vercel-url.vercel.app) and click **Sign Up**.

Enter your email and password to create your account. You'll be redirected to the dashboard automatically.

## Step 2 — Explore the Dashboard

Once logged in you'll see 3 main pages:

| Page | What it shows |
|---|---|
| **Incidents** | AI-grouped error logs with severity and suggestions |
| **Metrics** | CPU, memory, response time charts with anomaly markers |
| **Chat** | Ask questions about your logs in plain English |

## Step 3 — Generate Mock Data

Since V1 uses a mock log generator, click the **"Generate Mock Logs"** button on the Incidents page to populate the dashboard with 1000 realistic logs.

This simulates:
- Database connection failures
- Payment gateway timeouts
- NullPointerExceptions
- Slow DB queries
- Memory warnings

## Step 4 — See AI Analysis in Action

After generating logs:

1. Wait a few seconds for Celery to run the analysis automatically
2. Refresh the Incidents page
3. You'll see AI-grouped incident cards with:
   - Severity badges (CRITICAL/HIGH/MEDIUM/LOW)
   - Plain English summaries
   - Suggested fixes

## Step 5 — Explore Metrics

Go to the **Metrics** page and click **"Generate Mock Metrics"** to see:
- CPU usage chart with anomaly markers
- Memory usage chart
- Response time chart
- Anomalies detected table with pagination

## Step 6 — Chat with Your Logs

Go to the **Chat** page and ask questions like:
- *"Why did checkout fail?"*
- *"Which service has the most errors?"*
- *"What database issues happened?"*
- *"Summarize the payment errors"*

The AI will analyze your logs and respond with a detailed explanation.

## Step 7 — Slack Alerts

Each incident card has a **"Slack Alert"** button. Click it to manually send that incident to your Slack channel.

Critical incidents are also **automatically sent to Slack** every 5 minutes via Celery Beat.

:::tip
The analysis runs automatically every 5 minutes via Celery Beat — no manual trigger needed in production!
:::