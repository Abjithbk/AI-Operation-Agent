import requests
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(group: str, summary: str, severity: str, 
                     suggestion: str, log_count: int,user_slack_webhook_url:str = None):
    
    target_url = user_slack_webhook_url if user_slack_webhook_url else ADMIN_SLACK_WEBHOOK_URL
    
    # Color based on severity
    color_map = {
        "CRITICAL": "#FF0000",
        "HIGH": "#FF6600", 
        "MEDIUM": "#FFAA00",
        "LOW": "#00AA00"
    }
    color = color_map.get(severity, "#FF0000")
    
    # Severity emoji
    emoji_map = {
        "CRITICAL": "🚨",
        "HIGH": "⚠️",
        "MEDIUM": "🟡",
        "LOW": "🟢"
    }
    emoji = emoji_map.get(severity, "🚨")

    payload = {
        "attachments": [
            {
                "color": color,
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"{emoji} {severity} INCIDENT DETECTED"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Incident:*\n{group}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Occurrences:*\n{log_count}"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*AI Summary:*\n{summary}"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Suggested Fix:*\n{suggestion}"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "AI Ops Agent • Automated Alert"
                            }
                        ]
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(target_url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Slack alert failed: {str(e)}")
        return False