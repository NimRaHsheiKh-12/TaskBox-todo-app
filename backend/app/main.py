from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time

# Absolute imports from app folder
from .config import settings
from .middleware.error_handler import http_exception_handler, general_exception_handler
from .middleware.rate_limiter import check_rate_limit
from .api import auth, todo, chat
from .database.database import create_db_and_tables
from .utils.logging import logger, log_security_event

# ---------------------------
# Create FastAPI app instance
# ---------------------------
app = FastAPI(
    title=settings.app_name,
    description="API for Todo Fullstack Application",
    version="1.0.0"
)

# ---------------------------
# Startup / Shutdown Events
# ---------------------------
@app.on_event("startup")
async def startup_event():
    """Initialize app on startup"""
    try:
        create_db_and_tables()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Startup error: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    logger.info("Application shutting down")

# Initialize database tables once on module import (for Vercel compatibility)
try:
    create_db_and_tables()
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")

# ---------------------------
# CORS Middleware
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Rate Limiter
# ---------------------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)
    if request.url.path.startswith("/auth"):
        check_rate_limit(request)
    return await call_next(request)

# ---------------------------
# Request Logging Middleware
# ---------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(f"{request.method} {request.url.path} - {request.client.host} - {process_time:.2f}s - {response.status_code}")

    if request.url.path.startswith("/auth"):
        log_security_event(
            event_type="auth_request",
            ip_address=request.client.host,
            details={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": process_time
            }
        )
    return response

# ---------------------------
# Exception Handlers
# ---------------------------
app.add_exception_handler(401, http_exception_handler)
app.add_exception_handler(404, http_exception_handler)
app.add_exception_handler(405, http_exception_handler)
app.add_exception_handler(500, general_exception_handler)

# ---------------------------
# Include Routers
# ---------------------------
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(todo.router, prefix="/todos", tags=["todos"])
app.include_router(chat.router, tags=["chat"])

# ---------------------------
# Root Endpoint
# ---------------------------
@app.get("/")
def read_root():
    return {"message": "Welcome to Todo Fullstack App API"}
