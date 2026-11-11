from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import proxy
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production-grade low-latency semantic caching proxy for LLM applications.",
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(proxy.router)

# Mount the static web dashboard UI
app.mount("/", StaticFiles(directory="static", html=True), name="static")