from .config import Config
from .client import AIOpsClient

def init(api_key:str,api_url:str=None):

    Config.init(api_key,api_url)

def log(message:str,level:str = 'INFO',service:str = 'default'):
    AIOpsClient.send_log(message,level,service)

def capture_exception(exception:Exception,service:str = 'default'):
    AIOpsClient.send_exception(exception,service)