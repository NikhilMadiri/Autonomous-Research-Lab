import logging, time
from starlette.middleware.base import BaseHTTPMiddleware
logger = logging.getLogger("request")
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        started = time.perf_counter(); response = await call_next(request); logger.info("%s %s %s %.3fs", request.method, request.url.path, response.status_code, time.perf_counter() - started); return response

