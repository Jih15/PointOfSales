from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.security.security_config import ALLOWED_ORIGINS, IS_PRODUCTION, ALLOWED_HOSTS
from app.core.security.middleware import (
    SecurityHeadersMiddleware,
    RequestLoggingMiddleware,
    BodySizeLimitMiddleware
)

from app.database.connection import init_db
from app.route.api import api_router

# DB INIT
init_db()

# APP   
app = FastAPI(
    title="Point Of Sales API",
    version="0.1.0",
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None if IS_PRODUCTION else "/redoc",
    openapi_url=None if IS_PRODUCTION else "/openapi.json",
)

# RATE LIMITER
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request:Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail" : "Too much request. Try again later!"},
        headers={"Retry-After":"60"}
    )

# MIDDLEWARE
app.add_middleware(BodySizeLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization","Content-Type"],
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=ALLOWED_HOSTS
)

app.include_router(api_router)


@app.get("/", tags=["Health"])
def health():
    return {"status": "ok"}
