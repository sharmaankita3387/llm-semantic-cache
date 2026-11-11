from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    prompt: str = Field(
        ..., min_length=1, description="The user prompt sent to the LLM proxy."
    )


class QueryResponse(BaseModel):
    response: str
    cache_hit: bool
    similarity_score: float
    latency_ms: float
    total_cache_entries: int