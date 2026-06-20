import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .config import Config
from .batch import batch_processor

class AIOpsMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request:Request, call_next):

        start_time = time.time()
        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000

        if Config.API_KEY:
            batch_processor.add(
                endpoint='/metrics',
                data= {
                    "metric_name": "http_response_time",
                    "value": process_time,
                    # We use "GET /api/users" as the service name so it's easy to read
                    "service": f"{request.method} {request.url.path}",
                }
            )
        return response
        