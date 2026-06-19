from .config import Config
from .client import AIOpsClient
from .metrics import MetricsCollector
from .exceptions import enable_auto_capture
_metrics_collector = None

def init(api_key:str,api_url:str=None,collect_metrics:bool = True,metrics_interval:int = 30,auto_capture_errors:bool = True):

    Config.init(api_key,api_url)

    if collect_metrics:
        global _metrics_collector
        _metrics_collector = MetricsCollector(interval=metrics_interval)
        _metrics_collector.start()
    if auto_capture_errors:
        enable_auto_capture()
    print('[AIOps] SDK Initialized')
    
def shutdown():
    global _metrics_collector
    if _metrics_collector:
        _metrics_collector.stop()
        _metrics_collector = None
        print(f"[AIOps] SDK shutdown complete")

def log(message:str,level:str = 'INFO',service:str = 'default'):
    AIOpsClient.send_log(message,level,service)

def capture_exception(exception:Exception,service:str = 'default'):
    AIOpsClient.send_exception(exception,service)