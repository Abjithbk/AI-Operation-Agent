import sys
import traceback
from .client import AIOpsClient

_original_excepthook = None

def _custom_excepthook(exc_type,exc_value,exc_traceback):

    """Global exception that catches unhandled errors"""

    if issubclass(exc_type,KeyboardInterrupt):
        return
    
    tb_text = "".join(traceback.format_exception(exc_type,exc_value,exc_traceback))

    try:
        AIOpsClient.send_log(
            message=f"Unhandled Exception : {exc_type.__name__}: {exc_value}\n{tb_text}",
            level='CRITICAL',
            service='auto-capture'
        )
    except Exception:
        pass

    sys.__excepthook__(exc_type,exc_value,exc_traceback)


def enable_auto_capture():
    global _original_excepthook
    if _original_excepthook is None:
        _original_excepthook = sys.excepthook
        sys.excepthook = _custom_excepthook
        print('[AIOps] Auto-exception capture enabled')