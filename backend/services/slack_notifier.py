import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(__name__)

# Get the URL from the .env file
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(incident_title: str, severity: str, summary: str, incident_count: int = 1):
    """
    Sends a formatted alert to Slack using Block Kit.
    """
    if not SLACK_WEBHOOK_URL:
        logger.warning("SLACK_WEBHOOK_URL not set. Skipping Slack alert.")
        return False

    # Color coding based on severity for the Slack message border
    color_map = {
        "critical": "#ff0000",
        "high": "#ff9900",
        "medium": "#ffcc00",
        "low": "#36a64f"
    }
    color = color_map.get(severity.lower(), "#36a64f")

    # Slack Block Kit payload for a rich, readable message
    payload = {
        "attachments": [
            {
                "color": color,
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"🚨 AI Ops Alert: {incident_title}",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Severity:*\n{severity.upper()}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Incidents Grouped:*\n{incident_count}"
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
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "Posted by AI Operations Agent 🤖"
                            }
                        ]
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        logger.info("✅ Slack alert sent successfully.")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to send Slack alert: {e}")
        return False