import threading
import time
import psutil
import requests
from .config import Config

class MetricsCollector:
    def __init__(self,interval=30):
        self.interval = interval
        self.running = False

    def start(self):
        """Start  background metrics collection"""

        self.running = True
        thread = threading.Thread(target=self._collect_loop,daemon=True)
        thread.start()

    def _collect_loop(self):
        """Runs in background forever"""

        while self.running:
            try:

                metrics = {
                    'metric_name':'cpu_usage',
                    'value':psutil.cpu_percent(interval=1),
                    'service':'system'
                }

                requests.post(
                    f"{Config.API_URL}/metrics",
                    json=metrics,
                    headers={"X-API-KEY":Config.API_KEY},
                    timeout=5
                )

                memory = psutil.virtual_memory()
                metrics = {
                    'metric_name':'memory_usage',
                    'value':memory.percent,
                    'service':'system',
                }

                requests.post(
                    f"{Config.API_URL}/metrics",
                    json=metrics,
                    headers={"X-API-KEY":Config.API_KEY},
                    timeout=5
                )

                disk = psutil.disk_usage('/')
                metrics = {
                    'metric_name':'disk_usage',
                    'value':disk.percent,
                    'service':'system',
                }

                requests.post(
                    f"{Config.API_URL}/metrics",
                    json=metrics,
                    headers={"X-API-KEY":Config.API_KEY},
                    timeout=5
                )
            except Exception as e:
                print(f"[AIOps] Metrics collection failed: {e}")

            time.sleep(self.interval)
    def stop(self):
        """Stops."""
        self.running = False