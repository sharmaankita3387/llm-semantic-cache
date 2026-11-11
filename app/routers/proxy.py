from fastapi import APIRouter, HTTPException
from app.schemas.payload import QueryRequest, QueryResponse
from app.services.cache_service import cache_service

router = APIRouter(prefix="/api/v1", tags=["Semantic Proxy"])


@router.post("/generate", response_model=QueryResponse)
async def generate(payload: QueryRequest):
    try:
        result = cache_service.process_query(payload.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def stats():
    return cache_service.get_stats()