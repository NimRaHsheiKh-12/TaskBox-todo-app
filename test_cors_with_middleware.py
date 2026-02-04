from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()

# Add CORS middleware FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3002", "http://127.0.0.1:3002", "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

from fastapi import Request

# Add rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    print(f"Processing request: {request.method} {request.url.path}")
    response = await call_next(request)
    return response

# Add a test route
@app.post("/auth/register")
def register_user():
    return {"message": "User registered successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)