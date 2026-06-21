import requests

API_URL = "http://localhost:8000"

# Send a single critical error
response = requests.post(
    f"{API_URL}/api/logs",
    headers={
        "X-API-Key": "aiops_Iy3WlgrKZarSqDqsMRdJrk-ZHWFsmiM71ZiNEEP58Z0",  # Replace with your API key
        "Content-Type": "application/json"
    },
    json={
        "level": "CRITICAL",
        "service": "test-service",
        "message": "WebSocket test - critical error detected"
    }
)

print(f"Log sent: {response.status_code}")
print("\nNow go to your dashboard and click 'Analyse Logs' to see WebSocket in action!")