import redis,json,os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis.from_url(REDIS_URL)

def publish_incident(incident:dict):
    """Publish a new incident to redis channel"""
    message = {
        'type':'new_incident',
        'data':incident
    }

    redis_client.publish('incidents_channel',json.dumps(message))
    print(f"📡 Published incident to Redis: {incident.get('cluster_id')}")