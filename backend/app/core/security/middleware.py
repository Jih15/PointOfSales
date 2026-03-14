import time
import logging
import ipaddress
from typing import Callable

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.security.security_config import SECURITY_HEADERS, MAX_BODY_SIZE_BYTES

# Logger
logger = logging.getLogger("api")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Security Headers
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)

        for key, value in SECURITY_HEADERS.items():
            if value:
                response.headers[key]=value
            elif key in response.headers:
                del response.headers[key]

        return response
    
# Request Logging
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    SKIP_PATHS = {"/", "/docs", "/redoc", "/openapi.json", "/favicon.ico"}

    async def dispatch(self, request: Request, call_next: Callable):
        start       = time.time()
        client_ip   = self._get_client_ip(request)
        response    = await call_next(request)
        duration    = round((time.time()- start) * 1000, 2)

        if request.url.path not in self.SKIP_PATHS:
            msg = f"{client_ip} {request.method} {request.url.path} → {response.status_code} ({duration}ms)"

            if response.status_code >= 500:
                logger.error(msg)
            elif response.status_code >= 400:
                logger.warning(msg)
            else:
                logger.info(msg)

        return response
    
    @staticmethod
    def _get_client_ip(request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            raw = forwarded.split(",")[0].strip()
            try:
                ipaddress.ip_address(raw)
                return raw
            except ValueError:
                pass
        
        return request.client.host if request.client else "unknown"
    
# Body Size Limit
class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next:Callable):
        content_length = request.headers.get("content-length")

        if content_length and int(content_length) > MAX_BODY_SIZE_BYTES:
            return JSONResponse(
                status_code=413,
                content={"detail":"Request body too large."}
            )
        
        return await call_next(request)