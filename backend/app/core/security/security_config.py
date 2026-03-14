import os
import secrets
from typing import List

# APP
APP_ENV: str = os.getenv("APP_ENV", "development")
IS_PRODUCTION: bool = APP_ENV == "production"

# JWT Config
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY",default=secrets.token_hex(32))
JWT_ALGORITHM: str = "HS256"
JWT_ACCESS_TOKEN_EXPIRES_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

# CORS Config
ALLOWED_ORIGINS: List[str] = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000, http://localhost:8080"
).split(",")

# Rate Limiting Config
RATE_LIMIT_CREATE: str = os.getenv("RATE_LIMIT_CREATE", "10/minute")
RATE_LIMIT_READ: str = os.getenv("RATE_LIMIT_READ", "60/minute")
RATE_LIMIT_DEFAULT: str = os.getenv("RATE_LIMIT_DEFAULT", "30/minute")

# Max Body Size
MAX_BODY_SIZE_BYTES: int = int(os.getenv("MAX_BODY_SIZE_BYTES", str(1*1024*1024)))

# Dangerous Pattern Config
DANGEROUS_PATTERN: List[str] = [
    "<script",
    "javascript:",
    "onclick",
    "--",
    "/*",
    "xp_",
    "exec(",
    "drop table",
    "union select",
    "\x00",
    "../",
    "..\\"
]

# Security Headers Config
SECURITY_HEADERS: dict = {
    "X-Content-Type-Options" : "nosniff",
    "X-XSS-Protection" : "1; mode=block",
    "X-Frame-Options" : "DENY",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
    "Server": "WebServer",
    "X-Powered-By": "",
}