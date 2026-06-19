import logging
from .client import AIOpsClient

class AIOpsLogHandler(logging.Handler):
    """
    Custom logging handler that sends logs to AIOps backend.
    Only sends WARNING and above (not INFO/DEBUG to avoid spam).
    """

    def emit(self,record):
        """Called automatically by pythons logging system for every log"""

        try:
            if record.levelno < logging.WARNING:
                return
            level_map = {
                logging.WARNING:"WARNING",
                logging.ERROR:"ERROR",
                logging.CRITICAL:'CRITICAL',
            }
            level = level_map.get(record.levelno,'ERROR')

            message = self.format(record)

            if record.exc_info and record.exc_info[0] is not None:
                import traceback
                tb_text = "".join(traceback.format_exception(*record.exc_info))
                message = f"{message}\n{tb_text}"
            AIOpsClient.send_log(
                message=message,
                level=level,
                service=record.name or 'default'
            )
        except Exception:
            self.handleError(record)

_handler = None

def enable_log_capture(min_level=logging.WARNING):
    """
    Enable automatic log capture.
    All logs at min_level or above will be sent to backend.
    """
    global _handler
    
    if _handler is not None:
        return  # Already enabled
    
    # Create and configure the handler
    _handler = AIOpsLogHandler()
    _handler.setLevel(min_level)
    
    # Simple format
    formatter = logging.Formatter('%(message)s')
    _handler.setFormatter(formatter)
    
    # Add to root logger (captures ALL logs)
    root_logger = logging.getLogger()
    root_logger.addHandler(_handler)
    
    print(f"[AIOps] Log capture enabled (level: {logging.getLevelName(min_level)}+)")