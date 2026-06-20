from pydantic import BaseModel

class SlackAlertRequest(BaseModel):
    group: str
    summary: str
    severity: str
    suggestion: str
    log_count: int

class SlackWebhookRequest(BaseModel):
    slack_webhook_url:str