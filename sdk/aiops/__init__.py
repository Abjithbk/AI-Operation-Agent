from .config import Config
from .client import AIOpsClient
from .metrics import MetricsCollector
from .exceptions import enable_auto_capture
from .log_handler import enable_log_capture
from .batch import batch_processor
from.middleware import AIOpsMiddleware
_metrics_collector = None

def init(api_key:str,api_url:str=None,collect_metrics:bool = True,metrics_interval:int = 30,auto_capture_errors:bool = True,capture_logs:bool = True,log_min_level:str = 'WARNING',batch_flush_interval:int = 5):

    Config.init(api_key,api_url)

    #Start Batch processor
    batch_processor.flush_interval = batch_flush_interval
    batch_processor.start()

    #Metrics collection
    if collect_metrics:
        global _metrics_collector
        _metrics_collector = MetricsCollector(interval=metrics_interval)
        _metrics_collector.start()

    #Enable auto exception capture
    if auto_capture_errors:
        enable_auto_capture()

    #Enable log capture
    if capture_logs:
        import logging
        level_map ={
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        min_level = level_map.get(log_min_level.upper(),logging.WARNING)
        enable_log_capture(min_level=min_level)
    print('[AIOps] SDK Initialized')

def shutdown():
    global _metrics_collector
    if _metrics_collector:
        _metrics_collector.stop()
        _metrics_collector = None

    batch_processor.stop()
    print(f"[AIOps] SDK shutdown complete")

def log(message:str,level:str = 'INFO',service:str = 'default'):
    AIOpsClient.send_log(message,level,service)

def capture_exception(exception:Exception,service:str = 'default'):
    AIOpsClient.send_exception(exception,service)