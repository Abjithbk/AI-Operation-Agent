import random 
from datetime import datetime,timedelta

SERVICES = [
    "payment-service",
    "auth-service", 
    "checkout-service",
    "user-service",
    "notification-service"
]

INFO_MESSAGES = [
    "User logged in successfully",
    "GET /api/products - 200 OK - 45ms",
    "Cache hit for product",
    "User session refreshed",
    "Health check passed",
]

WARNING_MESSAGES = [
    "Slow DB query detected: 850ms",
    "Memory usage at 75%",
    "Retry attempt 1 for payment",
    "Response time above threshold: 600ms",
    "Connection pool running low",
]

ERROR_MESSAGES = [
    "Database connection failed: db-prod-1",
    "Payment gateway timeout: Stripe API",
    "NullPointerException in checkout.py line 84",
    "Cannot reach database at db-prod-1:5432",
    "Failed to execute query - connection refused",
]

def generate_mock_logs(count:int = 1000):
    logs = []
    for _ in range(count):

        rand = random.random()

        if rand < 0.70:
            level = "INFO"
            message = random.choice(INFO_MESSAGES)
        elif rand < 0.90:
            level = "WARNING"
            message = random.choice(WARNING_MESSAGES)
        else:
            level = "ERROR"
            message = random.choice(ERROR_MESSAGES)

        log = {
            "level":level,
            "service":random.choice(SERVICES),
            "message":message
        }
        logs.append(log)
    return logs
