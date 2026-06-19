import threading,time,requests
from .config import Config

class BatchProcessor:
    def __init__(self,flush_interval = 5,max_batch_size=50):
        self.queue = []
        self.lock = threading.Lock()
        self.flush_interval = flush_interval
        self.max_batch_size = max_batch_size
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the background flush thread"""

        self.running = True
        self.thread = threading.Thread(target=self._flush_loop,daemon=True)
        self.thread.start()
    def stop(self):
        """Stop the thread and flush remaining items"""

        self.running = False
        if self.thread:
            self.thread.join()
        self.flush()
    def add(self,endpoint:str,data:dict):
        """Add an item to the queue"""

        with self.lock:
            self.queue.append({'endpoint':endpoint,"data":data})
            #flush immediately
            if len(self.queue) >= self.max_batch_size:
                self.flush()
    def flush(self):
        """Send all queued items to the backend"""
        with self.lock:
            if not self.queue:
                return
            batch = self.queue.copy()
            self.queue.clear()

        for item in batch:
            try:
                requests.post(
                    f"{Config.API_URL}{item['endpoint']}",
                    json=item['data'],
                    headers={"X-API-Key": Config.API_KEY},
                    timeout=5
                )
            except Exception as e:
                print(f"[AIOps] Failed to send batch item: {e}")
    def _flush_loop(self):
        #Runs in background forever

        while self.running:
            time.sleep(self.flush_interval)
            self.flush()

batch_processor = BatchProcessor()