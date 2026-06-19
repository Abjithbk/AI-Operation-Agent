import requests
import traceback
from .config import Config

class AIOpsClient:

    @staticmethod
    def send_log(message:str,level:str = 'INFO',service:str = 'default'):

        if not Config.API_KEY:
            raise ValueError("SDK not initialized. Call aiops.init(api_key='...')")
        
        try:
            response = requests.post(
                 f"{Config.API_URL}/logs",
                json={
                    "message": message,
                    "level": level,
                    "service": service
                },
                headers={
                    "X-API-Key": Config.API_KEY
                },
                timeout=5
            )
            response.raise_for_status()
        except Exception as e:
            print(f"[AIops] failed to send log:{e}")
    
    @staticmethod
    def send_exception(exception:Exception,service:str = 'default'):
        if not Config.API_KEY:
            raise ValueError("SDK not initialized. Call aiops.init(api_key='...') first")
        
        try:
            error_message = f"{type(exception).__name__}: {str(exception)}\n{traceback.format_exc()}"

            response = requests.post(
                f"{Config.API_URL}/logs",
                json={
                    "message": error_message,
                    "level": "ERROR",
                    "service": service
                },
                headers={
                    "X-API-Key": Config.API_KEY
                },
                timeout=5
            )
            response.raise_for_status()
        except Exception as e:
            print(f"[AIOps] Failed to send exception: {e}")