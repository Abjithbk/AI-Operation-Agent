import requests
import traceback
from .config import Config
from .batch import batch_processor
class AIOpsClient:

    @staticmethod
    def send_log(message:str,level:str = 'INFO',service:str = 'default'):

        if not Config.API_KEY:
            return
        
        batch_processor.add(
            endpoint='/logs',
            data={
                "message": message,
                "level": level,
                "service": service
            }
        )
        
    
    @staticmethod
    def send_exception(exception:Exception,service:str = 'default'):
        if not Config.API_KEY:
            return
        error_message = "{type(exception).__name__}: {str(exception)}\n{traceback.format_exc()}"
        
        batch_processor.add(
            endpoint='/logs',
            data= {
                "message": error_message,
                "level": "ERROR",
                "service": service
            }
        )