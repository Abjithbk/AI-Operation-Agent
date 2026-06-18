---
sidebar_position: 6
---

# Python Integration

Learn how to send logs from your Python application to AI Ops Agent.

:::caution V1 Manual Integration
This guide shows manual integration for V1. A Python SDK (`pip install aiops-agent`) is coming in V2 that handles everything automatically with one line of code.
:::

## Prerequisites

- AI Ops Agent account ([Sign up here](https://your-vercel-url.vercel.app/signup))
- API Key from Settings page (coming in V2)
- Python 3.8+
- `requests` library

## Installation

```bash
pip install requests
```

---

## Basic Integration

Add this helper function to your app:

```python
import requests
import os

AIOPS_API_URL = "https://your-render-url.onrender.com/api/logs"
AIOPS_API_KEY = os.getenv("AIOPS_API_KEY")

def send_log(level: str, service: str, message: str):
    try:
        requests.post(
            AIOPS_API_URL,
            headers={"X-API-Key": AIOPS_API_KEY},
            json={
                "level": level,
                "service": service,
                "message": message
            },
            timeout=3
        )
    except Exception:
        pass  # Never let logging break your app
```

---

## Usage Examples

**Log an error:**
```python
try:
    process_payment(order_id)
except Exception as e:
    send_log("ERROR", "payment-service", str(e))
```

**Log a warning:**
```python
if response_time > 800:
    send_log("WARNING", "api-service", f"Slow response: {response_time}ms")
```

**Log info:**
```python
send_log("INFO", "auth-service", f"User {user_id} logged in")
```

---

## Django Integration

Add to your Django middleware:

```python
# middleware.py
from your_app.logging import send_log

class AIOpsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code >= 500:
            send_log(
                "ERROR",
                "django-app",
                f"{request.method} {request.path} → {response.status_code}"
            )
        return response
```

Add to `settings.py`:
```python
MIDDLEWARE = [
    ...
    'your_app.middleware.AIOpsMiddleware',
]
```

---

## FastAPI Integration

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000

    if response.status_code >= 500:
        send_log(
            "ERROR",
            "fastapi-app",
            f"{request.method} {request.url.path} → {response.status_code}"
        )
    elif duration > 1000:
        send_log(
            "WARNING",
            "fastapi-app",
            f"Slow request: {request.url.path} took {duration:.0f}ms"
        )

    return response
```

---

## Environment Setup

Add to your `.env` file:

AIOPS_API_KEY=aiops_your_key_here

:::tip Coming in V2
The Python SDK will make this even simpler:
```python
pip install aiops-agent

import aiops
aiops.init(api_key="aiops_xxx")
# Done! All errors captured automatically
```
:::