import random 
from datetime import datetime,timedelta
from schemas.metric import MetricCreate
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

def generate_mock_metrics(count: int = 200):
    metrics = []
    base_time = datetime.now() - timedelta(minutes=count)

    for i in range(count):
        timestamp = base_time + timedelta(minutes=i)

        # Normal CPU between 40-60% but spike at reading 150-160
        if 150 <= i <= 160:
            cpu = random.uniform(85, 95)   # SPIKE!
        else:
            cpu = random.uniform(40, 60)   # Normal

        # Normal memory between 55-70% but spike at reading 150-160
        if 150 <= i <= 160:
            memory = random.uniform(85, 95)  # SPIKE!
        else:
            memory = random.uniform(55, 70)  # Normal

        # Normal response time 100-200ms but spike at reading 150-160
        if 150 <= i <= 160:
            response_time = random.uniform(800, 1200)  # SPIKE!
        else:
            response_time = random.uniform(100, 200)   # Normal

        metrics.append(MetricCreate(
            service=random.choice(SERVICES),
            metric_name="cpu_usage",
            value=round(cpu, 2)
        ))
        metrics.append(MetricCreate(
            service=random.choice(SERVICES),
            metric_name="memory_usage",
            value=round(memory, 2)
        ))
        metrics.append(MetricCreate(
            service=random.choice(SERVICES),
            metric_name="response_time",
            value=round(response_time, 2)
        ))

    return metrics
