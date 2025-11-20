import uvicorn
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.routes import ai_content
from app.core.database import Base, engine
from app.core.logger import logger


app = FastAPI(title="AI Content Detection API")

# Rate limits: 10 requests/min
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Include Routes
app.include_router(ai_content.router, prefix="/api", tags=["AI Content"])


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database initialized successfully")


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    logger.info(f"📥 Incoming → {request.method} {request.url}")
    response = await call_next(request)
    return response

@app.get("/")
def welcome():
    return "Welcome to our AI Content Detection APPlication!"

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)