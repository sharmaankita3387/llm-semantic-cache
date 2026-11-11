from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import proxy

app = FastAPI(title="LLM Semantic Caching Proxy")

# Enable CORS so your GitHub Pages frontend can talk to this Render backend without restrictions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any frontend (GitHub Pages)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(proxy.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "LLM Semantic Caching Proxy API is running.",
    }